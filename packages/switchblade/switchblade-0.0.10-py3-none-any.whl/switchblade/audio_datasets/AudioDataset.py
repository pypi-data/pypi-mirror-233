import os
from pathlib import Path
import random
import soundfile as sf
import torch
import torchaudio
from typing import Callable, Optional, Union

from .Dataset import Dataset

class AudioDataset(Dataset):
    '''
    A generic audio dataset.

    dataroot: where the data exists; will recursively traverse
    return_labels: should labels be returned?
    labels: (filename : label) pairs or None if unlabeled
    n_samples: number of samples to return
    sr: which sample rate to use? will resample if necessary
    transform: optional transform to signal
    preprocess_path: path to store preprocessed data
    do_preprocessing: should we eagerly preprocess?
        'auto' = preprocess if necessary
    cap_at: should the dataset be 'capped' at a certain length? 
        Useful for testing data efficiency (i.e., sub-sampling data)
        So if cap_at is 100, this dataset will contain a random subset 
        of 100 audio files
    '''
    def __init__(
        self, 
        dataroot: str, 
        return_labels: Optional[bool] = False, 
        labels: Optional[dict] = None,
        n_samples: Optional[int] = 50000, 
        sr: Optional[int] = 44100, 
        transform: Optional[Callable] = None, 
        preprocess_path: Optional[str] = None,
        do_preprocessing: Union[str, bool] = False,
        cap_at: Union[None, int] = None,
        **kwargs
    ):
        super().__init__()
        assert do_preprocessing in ['auto', True, False]
        self.subsets = ['all'] # ignore 'subset' arg if passed

        self.dataroot = dataroot
        self.return_labels = return_labels
        self.labels = labels
        self.n_samples = n_samples
        self.sr = sr
        self.transform = transform
        self.do_preprocessing = do_preprocessing
        self.preprocess_path = preprocess_path or os.path.join(dataroot, 'preprocessed')
        self.preprocessed = os.path.exists(self.preprocess_path)
        self.cap_at = cap_at

        # collect a list of all filenames:
        self.filenames = []
        extensions = ['mp3', 'wav']
        for extension in extensions:
            for filename in Path(dataroot).rglob(f'*.{extension}'):
                self.filenames.append(str(filename))
        random.shuffle(self.filenames)

        if self.labels:
            assert len(self.labels) == len(self.filenames)
            for filename in self.filenames:
                assert filename in self.labels

        preprocess_needed = (
            (self.do_preprocessing == True) or 
            (self.do_preprocessing == 'auto' and not self.preprocessed)
        )
        if preprocess_needed:
            self.preprocess_all()

        self.n_outputs = None
        if labels:
            self.n_outputs = len(set(labels.values()))

    def get_signal(self, i):
        try:
            filename = self.filenames[i]
            return self.load_signal(filename)
        except:
            return self.get_signal((i+1) % len(self))

    def get_label(self, i):
        if self.labels is None:
            return None
        return self.labels[self.filenames[i]]

    def __len__(self):
        return len(self.filenames) if self.cap_at is None else self.cap_at