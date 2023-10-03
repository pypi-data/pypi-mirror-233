from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor
import hashlib
import math
import os
import pickle
import random

import numpy as np
import soundfile as sf
import torch
import torchaudio
from torchaudio import transforms
from torch.utils.data import Dataset as TorchDataset
from tqdm.auto import tqdm


class Dataset(TorchDataset):
    '''
    The abstract dataset class definition.
    All of these functions take 1d signal input (i.e., shape is (n,)) and 
    produce 1d output - including self.get_signal().
    '''
    @abstractmethod
    def __init__(self):
        '''
        the Dataset class should create the following:

        self.get_signal, self.get_label, and self.__len__ functions
        self.return_labels: bool
        self.n_samples: int
        self.sr: int
        self.transform: callable
        self.preprocess_path: str
        self.n_outputs: None if unlabeled, int otherwise (number of classes/outputs)
        self.n_views: int; default = 2
        self.return_same_slice: bool; default = False
        self.return_same_slice_p: float in [0, 1]; default = None
        self.subsets: list of strings of all subset names (ex. ['train', 'val', 'test'])
        '''
        
        self.return_labels = False # default; child instances can change this
        self.n_views = 2
        self.return_as_is = False
        self.return_same_slice = False
        self.return_same_slice_p = None
        self.dir_depth = 2
        self.return_index = False
        
    @abstractmethod
    def get_signal(self, i: int):
        '''
        returns signal for the ith datapoint. 
        should return a tensor of shape (n,) (i.e., no stereo -
        can use self.make_mono_if_necessary())
        '''
        pass

    @abstractmethod
    def get_label(self, i: int):
        '''
        returns the label for the ith datapoint
        '''
        pass

    @abstractmethod
    def __len__(self):
        pass

    def preprocess_filename(self, i: int):
        # return os.path.join(self.preprocess_path, f'{i:07}.p')
        filename = f'{i:07}.p'
        hash_name = hashlib.md5(filename.encode()).hexdigest()
        sub_dirs = [self.preprocess_path] + [
            hash_name[j:j+2] 
            for j in range(0, 2 * self.dir_depth, 2)
        ]
        sub_dir = os.path.join(*sub_dirs)
        os.makedirs(sub_dir, exist_ok=True)
        filename = os.path.join(sub_dir, filename)
        return filename

    def preprocess(self, i: int):
        data = self.__getitem__(i)
        filename = self.preprocess_filename(i)
        if not os.path.exists(filename):
            with open(filename, 'wb') as f:
                pickle.dump(data, f)

    def preprocess_all(self, num_threads=20): 
        original_return_as_is = self.return_as_is
        self.return_as_is = True
        self.preprocessed = False
        os.makedirs(self.preprocess_path, exist_ok=True)
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Instead of directly calling self.preprocess, submit it to the executor
            list(tqdm(executor.map(self.preprocess, range(len(self))), total=len(self)))

        self.preprocessed = True
        self.return_as_is = original_return_as_is

    def load_signal(self, filename):
        # torchaudio backend sometimes has trouble loading mp3 files so we directly use pysoundfile
        _, filetype = os.path.splitext(filename)
        
        signal, sr = torchaudio.load(filename)
        
        # error handling: in case torchaudio returns an empty file
        if signal.numel() == 0:
            signal, sr = sf.read(filename)
            signal = torch.tensor(signal, dtype=torch.float32) # (n_samples, n_channels)
            signal = signal.T # (n_channels, n_samples)
            
        signal = self.make_mono_if_necessary(signal)
        signal = self.resample_if_necessary(signal, sr)
        return signal

    def slice_sample(self, signal):
        assert len(signal.shape) == 1
        max_start_idx = len(signal) - self.n_samples

        if max_start_idx < 0:
            # how many times do we need to repeat the signal?
            n_repeat = math.ceil(self.n_samples / len(signal))
            signal = signal.repeat(n_repeat)
            max_start_idx = len(signal) - self.n_samples

        start_idx = random.randrange(max_start_idx) if max_start_idx != 0 else 0
        return signal[start_idx : start_idx + self.n_samples]
    
    def resample_if_necessary(self, signal, sr):
        if len(signal.shape) == 1: 
            signal = signal.unsqueeze(0)
        else: 
            raise ValueError('Signal must be one-dimensional')

        if (self.sr is not None) and (sr != self.sr):
            resampler = transforms.Resample(orig_freq=sr, new_freq=self.sr)
            signal = resampler(signal)
        return signal.squeeze()
    
    def make_mono_if_necessary(self, signal):
        # return shape: (n,)
        if signal.dim() == 1: return signal
        return signal.mean(axis=0)

    def __getitem__(self, i: int):
        if self.preprocessed:
            filename = self.preprocess_filename(i)
            with open(filename, 'rb') as f:
                data = pickle.load(f)

                # handling of special case in AudioDataset where there is no label
                if len(data) == 2:
                    signal, label = data
                else:
                    signal, label = data, self.get_label(i)
        else:
            signal = self.get_signal(i)
            label = self.get_label(i)

        if self.return_as_is:
            data = [signal]
            if self.return_labels:
                data.append(label)
            if self.return_index:
                data.append(i)
            return data if len(data) > 1 else data[0]

        # with probability p, return the same slice
        if self.return_same_slice_p:
            self.return_same_slice = np.random.random() < self.return_same_slice_p

        if self.return_same_slice:
            signal = self.slice_sample(signal)

        views = []
        for i in range(self.n_views):
            # signal already loaded on first iteration
            if i != 0 and not self.return_same_slice:
                signal = self.get_signal(i)

            view = self.slice_sample(signal).unsqueeze(0)
            if self.transform:
                view = self.transform(view)
            views.append(view)

        data = [views]
        if self.return_labels:
            data.append(label)
        if self.return_index:
            data.append(i)
        return data if len(data) > 1 else data[0]