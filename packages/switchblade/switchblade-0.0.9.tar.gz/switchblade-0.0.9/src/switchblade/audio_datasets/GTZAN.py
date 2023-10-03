'''
The GTZAN dataset class, which extends the AudioDataset class
'''

from .Dataset import Dataset
import os
import json
from typing import Callable, Optional, Union

class GTZANDataset(Dataset):
    subsets = ['train', 'valid', 'test']
    
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
        self.labels = labels # UNNECESSARY
        self.n_samples = n_samples
        self.sr = sr
        self.transform = transform
        self.do_preprocessing = do_preprocessing
        self.preprocess_path = preprocess_path or os.path.join(dataroot, 'gtzan','preprocessed')
        self.preprocessed = os.path.exists(self.preprocess_path)
        self.filenames = []

        self.classes = [
            'pop', 'metal', 'disco', 'blues', 
            'reggae', 'classical', 'rock', 'hiphop', 
            'country', 'jazz'
        ]

        SPLIT_PATH = os.path.join(dataroot,'gtzan','gtzan_ff.json')
        MUSIC_PATH = os.path.join(dataroot,'gtzan','genres_original')
        
        with open(SPLIT_PATH, 'r') as file:
            data = json.load(file)
              
        self.labels = {}
        for entry in data.values():
            if entry.get('split') == subset:
                genre = entry.get('y')
                song = entry.get('extra').get('id') + '.wav'
                self.filenames.append(os.path.join(MUSIC_PATH,genre,song))
                self.labels[os.path.join(MUSIC_PATH,genre,song)] = genre 
                
        # sanity check
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
        if self.labels:
            self.n_outputs = len(set(labels.values()))

    def get_signal(self, i):
        filename = self.filenames[i]
        try:
            return self.load_signal(filename)
        except Exception:
            print(f'Error loading {filename}; returning next index to avoid crashing')
            return self.get_signal((i+1) % len(self))

    def get_label(self, i):
        return self.labels[self.filenames[i]]

    def __len__(self):
        return len(self.filenames)
