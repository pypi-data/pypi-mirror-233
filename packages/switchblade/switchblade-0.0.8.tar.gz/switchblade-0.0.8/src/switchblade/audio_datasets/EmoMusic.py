from .Dataset import Dataset
import os
import torch
from typing import Callable, Optional, Union
import json

class EmoMusic(Dataset):
    
    '''
    Makes the assumption that all dataset audio files are in their respective audio folders.
    This Dataset consists Specifically of mp3 files. There should be 1000 audio files,
    although only 744 as there are duplicates.
    '''
    subsets = ['train', 'valid', 'test']
    
 
    def __init__(
        self,
        dataroot: str,
        folder_in_archive: Optional[str] = 'emomusic', 
        subset: Optional[str] = None,
        return_labels: bool = False,
        labels: Optional[dict] = None,
        n_samples: Optional[int] = 50000, 
        sr: Optional[int] = 44100, 
        transform: Optional[Callable] = None, 
        preprocess_path: Optional[str] = None,
        do_preprocessing: Union[str, bool] = 'auto',
        **kwargs
    ):
        super().__init__()
        self.dataroot = dataroot
        self.subset = subset
        self.return_labels = return_labels
        self.n_samples = n_samples
        self.sr = sr
        self.transform = transform
        self.preprocess_path = preprocess_path or os.path.join(dataroot, 'emomusic','preprocessed')
        self.preprocessed = os.path.exists(self.preprocess_path)
        self.n_outputs = 2
        self.do_preprocessing = do_preprocessing
        self._path = os.path.join(dataroot, folder_in_archive) 
        self.filenames = [] 
        self.labels = {}
        if preprocess_path:
            self.preprocess_path = preprocess_path
        else:
            self.preprocess_path = os.path.join(self.dataroot, 'emomusic', 'preprocessed')
        
        assert do_preprocessing in ['auto', True, False]
        if not os.path.isdir(self._path):
            raise RuntimeError(
                "Dataset not found. Please go to https://cvml.unige.ch/databases/emoMusic/ and fill out the google doc to get access"
            )
            
        SPLIT_PATH = os.path.join(self._path,'emomusic.json')
        MUSIC_PATH = os.path.join(self._path, 'clips_45seconds')
        
        with open(SPLIT_PATH, 'r') as file:
            data = json.load(file)

        for key, entry in data.items():
            if isinstance(entry, dict) and entry['split'] == subset:
                song = str(int(key))
                self.labels[song] = entry['y']
                self.filenames.append(os.path.join(MUSIC_PATH, song + '.mp3'))
        
        preprocess_needed = (
            (self.do_preprocessing == True) or 
            (self.do_preprocessing == 'auto' and not self.preprocessed)
        )
        if preprocess_needed:
            self.preprocess_all()
        
    def get_signal(self, i: int):
        filename = self.filenames[i]
        return self.load_signal(filename)

    def get_label(self, i):
        song_key = os.path.basename(self.filenames[i]).split('.')[0]  # gets the filename without extension
        return torch.FloatTensor(self.labels[song_key])

    def __len__(self):
        return len(self.filenames)