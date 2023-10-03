import json
import os
from pathlib import Path
import random
import tarfile
from typing import Callable, Optional, Union

import torchaudio

from .Dataset import Dataset
from .utils import download_file

URLS = {
    'train' : 'http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-train.jsonwav.tar.gz',
    'valid' : 'http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-valid.jsonwav.tar.gz',
    'test'  : 'http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-test.jsonwav.tar.gz'
}

class NSynthDataset(Dataset):
    # subsets = ['train', 'valid', 'test']
    subsets = ['train', 'test']
    
    '''
    The NSynth Dataset class.

    dataroot: where the data exists/where to download it
    subset: train/test/valid
    download: should the dataset be downloaded?
    return_labels: should labels be returned?
    label_type: which label type should be returned?
    n_samples: number of samples to return
    sr: which sample rate to use? will resample if necessary
    transform: optional transform to signal
    preprocess_path: path to store preprocessed data
    do_preprocessing: should we eagerly preprocess?
        'auto' = preprocess if necessary
    classes: 'any' or int between 1-11
    '''
    def __init__(
        self, 
        dataroot: str, 
        subset: str, 
        download: Optional[bool] = False, 
        return_labels: Optional[bool] = True, 
        label_type: Optional[bool] = 'instrument_family',
        n_samples: Optional[int] = 50000, 
        sr: Optional[int] = 44100, 
        transform: Optional[Callable] = None, 
        preprocess_path: Optional[str] = None,
        do_preprocessing: Union[str, bool] = 'auto',
        classes: Union[str, int] = 'all',
        **kwargs
    ):
        super().__init__()
        # assert subset in self.subsets
        assert label_type in ['instrument_family', 'qualities', 'instrument_source']
        assert do_preprocessing in ['auto', True, False]

        self.dataroot = dataroot
        self.subset = subset
        self.download = download
        self.return_labels = return_labels
        self.label_type = label_type
        self.n_samples = n_samples
        self.sr = sr
        self.transform = transform
        self.do_preprocessing = do_preprocessing
        self.preprocess_path = preprocess_path or os.path.join(dataroot, 'preprocessed')
        self.preprocessed = os.path.exists(self.preprocess_path)
        self.n_outputs = 11 if classes == 'all' else classes

        # use validation set as training set to save memory
        if self.subset == 'train':
            self.subset = 'valid'
            subset = 'valid'

        path = os.path.join(dataroot, f'nsynth-{subset}')
        if download and not os.path.exists(path):
            print('downloading dataset...')
            Path(dataroot).mkdir(parents=True, exist_ok=True)
            filename = os.path.basename(URLS[subset])
            filename = download_file(URLS[subset], os.path.join(dataroot, filename))

            print('downloaded dataset. unzipping...')
            with tarfile.open(filename) as f:
                f.extractall(dataroot)
            os.remove(filename)

        # get a list of all filenames:
        self.filenames = os.listdir(os.path.join(path, 'audio'))
        self.filenames = list(filter(lambda x: x.endswith('wav'), self.filenames))
        self.filenames = [os.path.join(path, 'audio', filename) for filename in self.filenames]

        # get the labels:
        self.labels = json.load(open(os.path.join(path, 'examples.json')))
        assert len(self.labels) == len(self.filenames)

        # if we only want a subset of the classes, filter the data:
        if classes != 'all':
            all_labels = list(set(e['instrument_family'] for e in self.labels.values()))
            label_subset = set(random.sample(all_labels, classes))
            
            filenames = []
            self.indices = [] # mapping from old index (full dataset) --> new index (subset)
            for i, filename in enumerate(self.filenames):
                label = self.get_label(i)
                if label in label_subset:
                    filenames.append(filename)
                    self.indices.append(i)
            self.filenames = filenames

            # overwrite parent's preprocess_filename function, which maps indices to 
            # their new filenames
            def preprocess_filename(i):
              return os.path.join(self.preprocess_path, f'{self.indices[i]:07}.p')
            self.preprocess_filename = preprocess_filename

            print(f'only using classes: {sorted(list(label_subset))}')

        # preprocess if necessary:
        preprocess_needed = (
            (self.do_preprocessing == True) or 
            (self.do_preprocessing == 'auto' and not self.preprocessed)
        )
        if preprocess_needed:
            self.preprocess_all()

    def get_signal(self, i):
        filename = self.filenames[i]
        signal, sr = torchaudio.load(filename)
        signal = self.make_mono_if_necessary(signal)
        signal = self.resample_if_necessary(signal, sr)
        return signal

    def get_label(self, i):
        # get just the entry filename (without extension):
        filename = self.filenames[i]
        entry = os.path.basename(filename).rsplit('.', 1)[0]

        entry = self.labels[entry]
        label = entry[self.label_type]

        return label

    def __len__(self):
        return len(self.filenames)
    

class NSynthInstrument(NSynthDataset):
    def get_label(self, i):
        # get just the entry filename (without extension):
        filename = self.filenames[i]
        entry = os.path.basename(filename).rsplit('.', 1)[0]

        entry = self.labels[entry]
        label = entry['instrument_family']

        return label
    
class NSynthPitch(NSynthDataset):
    def get_label(self, i):
        # get just the entry filename (without extension):
        filename = self.filenames[i]
        entry = os.path.basename(filename).rsplit('.', 1)[0]

        entry = self.labels[entry]
        label = entry['pitch']

        return label