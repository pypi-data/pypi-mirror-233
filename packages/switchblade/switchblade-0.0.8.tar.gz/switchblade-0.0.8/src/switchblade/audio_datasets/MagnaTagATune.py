'''
The MagnaTagATune dataset class, modified from 
https://github.com/Spijkervet/CLMR/blob/master/clmr/datasets/magnatagatune.py
'''

import os
import numpy as np
from typing import Callable, Optional, Union
import random
import torch
import soundfile as sf

# torchaudio.set_audio_backend('soundfile')
from torchvision.datasets.utils import (
    download_url,
    extract_archive,
)

from .Dataset import Dataset


FOLDER_IN_ARCHIVE = "magnatagatune"
_CHECKSUMS = {
    "http://mi.soi.city.ac.uk/datasets/magnatagatune/mp3.zip.001": "",
    "http://mi.soi.city.ac.uk/datasets/magnatagatune/mp3.zip.002": "",
    "http://mi.soi.city.ac.uk/datasets/magnatagatune/mp3.zip.003": "",
    "http://mi.soi.city.ac.uk/datasets/magnatagatune/annotations_final.csv": "",
    "https://github.com/minzwon/sota-music-tagging-models/raw/master/split/mtat/binary.npy": "",
    "https://github.com/minzwon/sota-music-tagging-models/raw/master/split/mtat/tags.npy": "",
    "https://github.com/minzwon/sota-music-tagging-models/raw/master/split/mtat/test.npy": "",
    "https://github.com/minzwon/sota-music-tagging-models/raw/master/split/mtat/train.npy": "",
    "https://github.com/minzwon/sota-music-tagging-models/raw/master/split/mtat/valid.npy": "",
    "https://github.com/jordipons/musicnn-training/raw/master/data/index/mtt/train_gt_mtt.tsv": "",
    "https://github.com/jordipons/musicnn-training/raw/master/data/index/mtt/val_gt_mtt.tsv": "",
    "https://github.com/jordipons/musicnn-training/raw/master/data/index/mtt/test_gt_mtt.tsv": "",
    "https://github.com/jordipons/musicnn-training/raw/master/data/index/mtt/index_mtt.tsv": "",
}


def get_file_list(root, subset, split):
    if subset == "train":
        if split == "pons2017":
            fl = open(os.path.join(root, "train_gt_mtt.tsv")).read().splitlines()
        else:
            fl = np.load(os.path.join(root, "train.npy"))
    elif subset == "valid":
        if split == "pons2017":
            fl = open(os.path.join(root, "val_gt_mtt.tsv")).read().splitlines()
        else:
            fl = np.load(os.path.join(root, "valid.npy"))
    else:
        if split == "pons2017":
            fl = open(os.path.join(root, "test_gt_mtt.tsv")).read().splitlines()
        else:
            fl = np.load(os.path.join(root, "test.npy"))

    if split == "pons2017":
        binary = {}
        index = open(os.path.join(root, "index_mtt.tsv")).read().splitlines()
        fp_dict = {}
        for i in index:
            clip_id, fp = i.split("\t")
            fp_dict[clip_id] = fp

        for idx, f in enumerate(fl):
            clip_id, label = f.split("\t")
            fl[idx] = "{}\t{}".format(clip_id, fp_dict[clip_id])
            clip_id = int(clip_id)
            binary[clip_id] = eval(label)
    else:
        binary = np.load(os.path.join(root, "binary.npy"))

    return fl, binary


class MagnaTagATune(Dataset):
    """Create a Dataset for MagnaTagATune.
    Args:
        root (str): Path to the directory where the dataset is found or downloaded.
        folder_in_archive (str, optional): The top-level directory of the dataset.
        download (bool, optional):
            Whether to download the dataset if it is not found at root path. (default: ``False``).
        subset (str, optional): Which subset of the dataset to use.
            One of ``"training"``, ``"validation"``, ``"testing"`` or ``None``.
            If ``None``, the entire dataset is used. (default: ``None``).
    """

    _ext_audio = ".wav"
    subsets = ["train", "valid", "test"]

    def __init__(
        self,
        root: str,
        folder_in_archive: Optional[str] = FOLDER_IN_ARCHIVE,
        download: Optional[bool] = False,
        subset: Optional[str] = None,
        split: Optional[str] = 'pons2017',
        return_labels: Optional[bool] = True,
        n_samples: Optional[int] = 50000, 
        sr: Optional[int] = 44100, 
        transform: Optional[Callable] = None, 
        preprocess_path: Optional[str] = None,
        do_preprocessing: Union[str, bool] = 'auto',
        cap_at: Optional[int] = None,
        **kwargs
    ) -> None:

        super().__init__()
        self.root = root
        self.folder_in_archive = folder_in_archive
        self.download = download
        self.subset = subset
        self.split = split
        self.return_labels = return_labels
        self.n_samples = n_samples
        self.sr = sr
        self.transform = transform
        self.preprocess_path = preprocess_path or os.path.join(self.root, 'magnatagatune', 'preprocessed')
        self.do_preprocessing = do_preprocessing
        self.cap_at = cap_at
        self.preprocessed = os.path.exists(self.preprocess_path)

        assert do_preprocessing in ['auto', True, False]
        assert subset is None or subset in self.subsets, (
            "When `subset` not None, it must take a value from "
            + "{'train', 'valid', 'test'}."
        )

        self._path = os.path.join(root, folder_in_archive)

        if download:
            if not os.path.isdir(self._path):
                os.makedirs(self._path)

            zip_files = []
            for url, checksum in _CHECKSUMS.items():
                target_fn = os.path.basename(url)
                target_fp = os.path.join(self._path, target_fn)
                if ".zip" in target_fp:
                    zip_files.append(target_fp)

                if not os.path.exists(target_fp):
                    download_url(
                        url,
                        self._path,
                        filename=target_fn,
                        # md5=checksum # introduces some error?
                    )

            if not os.path.exists(
                os.path.join(
                    self._path,
                    "f",
                    "american_bach_soloists-j_s__bach_solo_cantatas-01-bwv54__i_aria-30-59.mp3",
                )
            ):
                merged_zip = os.path.join(self._path, "mp3.zip")
                print("Merging zip files...")
                with open(merged_zip, "wb") as f:
                    for filename in zip_files:
                        with open(filename, "rb") as g:
                            f.write(g.read())

                extract_archive(merged_zip)

        if not os.path.isdir(self._path):
            raise RuntimeError(
                "Dataset not found. Please use `download=True` to download it."
            )

        self.fl, self.binary = get_file_list(self._path, self.subset, self.split)
        self.n_outputs = 50  # self.binary.shape[1]

        # if we only want self.cap_at samples, get them randomly:
        if self.cap_at:
            random.shuffle(self.fl)

        # preprocess if necessary:
        preprocess_needed = (
            (self.do_preprocessing == True) or 
            (self.do_preprocessing == 'auto' and not self.preprocessed)
        )
        if preprocess_needed:
            self.preprocess_all()

    def file_path(self, n: int) -> str:
        _, fp = self.fl[n].split("\t")
        return os.path.join(self._path, fp)
    
    def get_signal(self, i):
        target_fp = self.target_file_path(i)
        # try:
        # signal, sr = torchaudio.load(target_fp)
        signal, sr = sf.read(target_fp)
        signal = torch.tensor(signal, dtype=torch.float32).T # (n_channels, n_samples)
        # except OSError as e:
        #     raise OSError('File not found')
        
        signal = self.make_mono_if_necessary(signal)
        signal = self.resample_if_necessary(signal, sr)

        return signal

    def get_label(self, i):
        clip_id, _ = self.fl[i].split("\t")
        label = self.binary[int(clip_id)]
        return torch.FloatTensor(label)

    def __len__(self) -> int:
        return len(self.fl) if self.cap_at is None else self.cap_at

    def target_file_path(self, n: int) -> str:
        fp = self.file_path(n)
        file_basename, _ = os.path.splitext(os.path.normpath(fp))
        return file_basename + '.mp3' # self._ext_audio