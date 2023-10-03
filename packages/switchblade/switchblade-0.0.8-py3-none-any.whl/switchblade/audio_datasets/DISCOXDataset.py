'''
The DISCO Dataset: the largest available music dataset to date.
'''

from concurrent.futures import ThreadPoolExecutor
from .Dataset import Dataset
from datasets import load_dataset
import hashlib
import os
import random
import re
import soundfile as sf
import torchaudio
from tqdm import tqdm
from urllib.request import urlretrieve
from typing import Callable, Optional, Union

from .AudioDataset import AudioDataset

class DISCOXDataset(Dataset):
    def __init__(
            self, 
            dataroot: str,
            subset: str = '10k-random', 
            max_workers: int = 20, 
            dir_depth: int = 3,

            download: bool = False,
            n_samples: Optional[int] = 50000, 
            sr: Optional[int] = 44100, 
            transform: Optional[Callable] = None, 
            preprocess_path: Optional[str] = None,
            do_preprocessing: Union[str, bool] = False,
            return_labels: Optional[bool] = False, 
            cap_at: Union[int, None] = None,
            chunk_dataset: bool = False,

            additional_audio_folder: Optional[str] = None
    ):
        super().__init__()

        self.n_views = 2
        self.return_same_slice = False
        self.return_same_slice_p = None
        self.subsets = ['10k-random', '200k-random', '200k-high-quality', '10m']
        self.dataset_name = {
            '10k-random' : 'DISCOX/DISCO-10K-random',
            '200k-random' : 'DISCOX/DISCO-200K-random',
            '200k-high-quality' : 'DISCOX/DISCO-200K-high-quality',
            '10m' : 'DISCOX/DISCO-10M'
        }[subset]
        self.dataroot = os.path.join(dataroot, 'DISCOX', subset)
        self.subset = subset
        self.max_workers = max_workers
        self.dir_depth = dir_depth
        self.n_outputs = None

        self.download_dataset = download
        self.return_labels = return_labels
        self.do_preprocessing = do_preprocessing
        self.n_samples = n_samples
        self.sr = sr
        self.transform = transform
        self.cap_at = cap_at
        self.chunk_dataset = chunk_dataset
        self.preprocess_path = preprocess_path or os.path.join(self.dataroot, 'preprocessed')
        self.preprocessed = os.path.exists(self.preprocess_path)

        self.additional_audio_folder = additional_audio_folder
        if additional_audio_folder:
            self.additional_audio_folder = AudioDataset(
                additional_audio_folder,
                self.return_labels,
                n_samples=self.n_samples,
                sr=self.sr,
                transform=self.transform
            )
            print(f'Processed additional AudioFolder of size {len(self.additional_audio_folder)}')

        # for grace:
        # if os.name != 'nt':
        #     torchaudio.set_audio_backend('sox_io')

        # Load the dataset
        self.ds = load_dataset(self.dataset_name)
        self.urls = self.ds['train']['preview_url_spotify']

        # Ensure data is downloaded
        if not os.path.exists(self.dataroot) or self.download_dataset:
            print('Downloading/Verifying dataset...')
            self._ensure_data_downloaded()

        # Split data if requested (idea: to speed up training time)
        filename = self.url2filename(self.urls[0])
        hash_name = hashlib.md5(filename.encode()).hexdigest()
        sub_dirs = [self.dataroot] + [hash_name[i:i+2] for i in range(0, 2*self.dir_depth, 2)]
        base_filename = filename.split('.')[0]
        is_split = [f for f in os.listdir(os.path.join(*sub_dirs)) if base_filename in f and 'split' in f]
        if chunk_dataset and not is_split:
            try:
                self._split_data()
            except:
                print('Splitting was unsuccessful (probably a problem with the SoundFile library)')

        # Preprocess if needed or requested
        preprocess_needed = (
            (self.do_preprocessing == True) or 
            (self.do_preprocessing == 'auto' and not self.preprocessed)
        )
        if preprocess_needed:
            self.preprocess_all()

    def _ensure_data_downloaded(self):
        os.makedirs(self.dataroot, exist_ok=True)

        def download_file(url):
            filename = self.url2filename(url)
            hash_name = hashlib.md5(filename.encode()).hexdigest()
            sub_dirs = [self.dataroot] + [
                hash_name[i:i+2] 
                for i in range(0, 2 * self.dir_depth, 2)
            ]
            sub_dir = os.path.join(*sub_dirs)
            os.makedirs(sub_dir, exist_ok=True)
            filename = os.path.join(sub_dir, filename)
            if not os.path.exists(filename) or (os.stat(filename).st_size == 0):
                try:
                    urlretrieve(url, filename)
                except Exception as e:
                    print(f'Failed to download: {url}\nError: {e}')

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            list(tqdm(executor.map(download_file, self.urls), total=len(self.urls)))

    def _split_file(self, url):
        '''
        Splits a single audio file into overlapping 2-second windows.
        '''
        window_size = self.sr * 2  # 2 seconds in samples
        hop_size = int(window_size / 2)  # 50% overlap

        filename = self.url2filename(url)
        hash_name = hashlib.md5(filename.encode()).hexdigest()
        sub_dirs = [self.dataroot] + [hash_name[i:i+2] for i in range(0, 2 * self.dir_depth, 2)]
        full_path = os.path.join(*sub_dirs, filename)
        
        signal, sr = sf.read(full_path)
        if len(signal.shape) > 1 and signal.shape[1] > 1:
            signal = signal.mean(axis=1)  # make mono

        # Calculate the number of splits based on hop size
        num_splits = int((len(signal) - window_size) / hop_size) + 1

        for i in range(num_splits):
            start_sample = i * hop_size
            end_sample = start_sample + window_size

            split_signal = signal[start_sample:end_sample]
            split_filename = f"{filename.split('.')[0]}_split_{i}.mp3"
            split_path = os.path.join(*sub_dirs, split_filename)

            sf.write(split_path, split_signal, sr)


    def _split_data(self):
        '''
        Splits each 30-second audio file into overlapping 2-second windows.
        '''
        print('Chunking dataset...')
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            list(tqdm(executor.map(self._split_file, self.urls), total=len(self.urls)))

    def get_signal(self, i: int):
        # if we have an additional audio folder:
        if self.additional_audio_folder and i >= len(self.urls):
            i -= len(self.urls)
            return self.additional_audio_folder.get_signal(i)

        # sanity check, to avoid potential errors :)
        if self.cap_at:
            i = i % self.cap_at

        filename = self.url2filename(self.urls[i])
        hash_name = hashlib.md5(filename.encode()).hexdigest()
        sub_dirs = [self.dataroot] + [hash_name[i:i+2] for i in range(0, 2*self.dir_depth, 2)]

        base_filename = filename.split('.')[0]
        all_files = [f for f in os.listdir(os.path.join(*sub_dirs)) if base_filename in f and 'split' in f]
        if all_files:
            filename = random.choice(all_files)
        
        filename = os.path.join(*sub_dirs, filename)
        signal, sr = torchaudio.load(filename)
        signal = self.make_mono_if_necessary(signal)
        signal = self.resample_if_necessary(signal, sr)

        # another sanity check / bug avoidance: 
        # some files are empty when loaded (torch.Size([0])). we'll simply return the next 
        # data sample instead; doesn't matter too much with a lot of data.
        if signal.numel() == 0:
            return self.get_signal((i+1) % len(self))

        return signal

    def get_label(self, i: int):
        # This is an unlabeled dataset
        return None

    def __len__(self):
        # return len(self.urls) if self.cap_at is None else self.cap_at
        self_length = len(self.urls) if self.cap_at is None else self.cap_at
        additional_length = len(self.additional_audio_folder) if self.additional_audio_folder else 0
        return self_length + additional_length
    
    @staticmethod
    def url2filename(url):
        filename = url.split('/')[-1] + '.mp3'

        '''
        On Windows machines, certain non-alphanumeric characters that appear in these URLs
        cause problems, so we must sanitize the filenames first.
        '''
        return re.sub(r'[^\w.]+', '', filename)