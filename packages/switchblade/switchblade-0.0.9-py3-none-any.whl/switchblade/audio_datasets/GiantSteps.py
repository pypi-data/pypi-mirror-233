'''
The GTZAN dataset class, which extends the AudioDataset class
'''

from .Dataset import Dataset
import os
import torch
import soundfile as sf
from typing import Callable, Optional, Union
import json

class GiantStepsDataset(Dataset):
    subsets = ['train', 'valid', 'test']
    
    '''
    dataroot: where the data exists; will recursively traverse
    subset: the subset to load
    return_labels: should labels be returned?
    labels: (filename : label) pairs or None if unlabeled
    n_samples: number of samples to return
    sr: which sample rate to use? will resample if necessary
    transform: optional transform to signal
    preprocess_path: path to store preprocessed data
    do_preprocessing: should we eagerly preprocess?
        'auto' = preprocess if necessary
    '''
    def __init__(
        self, 
        dataroot: str, 
        subset: str,
        return_labels: Optional[bool] = False, 
        labels: Optional[dict] = None,
        n_samples: Optional[int] = 50000, 
        sr: Optional[int] = 44100, 
        transform: Optional[Callable] = None, 
        preprocess_path: Optional[str] = None,
        do_preprocessing: Union[str, bool] = 'auto',
        **kwargs
    ):
        super().__init__()
        assert subset in self.subsets
        assert do_preprocessing in ['auto', True, False]

        self.dataroot = dataroot 
        self.subset = subset
        self.return_labels = return_labels
        self.labels = labels
        self.n_samples = n_samples
        self.sr = sr
        self.transform = transform
        self.do_preprocessing = do_preprocessing
        self.preprocess_path = preprocess_path or os.path.join(dataroot, 'giantsteps','preprocessed')
        self.preprocessed = os.path.exists(self.preprocess_path)
        self.filenames = []
        
        '''
        Annotations have them in 'sharp' while 'y' in dataset has them in 'flat' measure
        # means sharp
        C# = Db, D# = Eb, F# = Gb, G# = Ab, A# = Bb
        C sharp = D flat, D sharp = E flat
        '''
        self.classes = ['C Major','C Minor','Db Major','Db Minor','D Major',
                        'D Minor','Eb Major','Eb Minor','E Major','E Minor',
                        'F Major','F Minor','Gb Major','Gb Minor','G Major',
                        'G Minor','Ab Major','Ab Minor','A Major','A Minor',
                        'Bb Major','Bb Minor','B Major','B Minor',
                        ]    

        SPLIT_PATH = os.path.join(dataroot,'giantsteps','giantsteps_clips.json')
        MUSIC_PATH = os.path.join(dataroot,'giantsteps','audio')
        
        with open(SPLIT_PATH, 'r') as file :
            data = json.load(file)
              
        self.labels = {}
        
        '''
        Giantsteps split file has an odd structure so 
        test must be read differently than valid and train
        
        test = 604 songs -> cut into 4 parts 2416
        train = 923 songs -> cut into 4 parts 3692
        valid = 236 songs -> cut into 4 parts 944
        
        Dataset has more songs than are actually used in the subsets
        '''
        
        i = 0
        if subset == 'test':
            for key, entry in data.items():
                if entry.get('split') == subset and key.endswith('-0'):
                    Note = entry.get('y')
                    song = entry.get('extra').get('jams').get('file_metadata').get('title')
                    song = song[:-3] + 'mp3'
                    self.filenames.append(os.path.join(MUSIC_PATH,song))
                    self.labels[i] = Note 
                    i+=1
        else:
            for key, entry in data.items():
                if entry.get('split') == subset and key.endswith('-0'):
                    Note = entry.get('y')
                    song = entry.get('extra').get('beatport_metadata').get('ID')
                    song =  song + '.LOFI.mp3'
                    self.filenames.append(os.path.join(MUSIC_PATH,song))
                    self.labels[i] = Note 
                    i+=1

        self.labels[i] = Note # error handling
        
        preprocess_needed = (
            (self.do_preprocessing == True) or 
            (self.do_preprocessing == 'auto' and not self.preprocessed)
        )
        if preprocess_needed:
            self.preprocess_all()

        self.n_outputs = None
        if self.labels:
            self.n_outputs = len(set(labels.values()))
            
    def get_signal(self, i):
        filename = self.filenames[i]
        _, filetype = os.path.splitext(filename)
        if filetype == '.mp3':
            signal, sr = sf.read(filename)
            signal = torch.tensor(signal, dtype=torch.float32) # (n_samples, n_channels)
            signal = signal.T # (n_channels, n_samples)
            
        signal = self.make_mono_if_necessary(signal)
        signal = self.resample_if_necessary(signal, sr)
        
        return signal
        
    def get_label(self, i):
        return self.labels[i]
        
    def __len__(self):
        return len(self.filenames)