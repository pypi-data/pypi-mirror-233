'''
Loading mp3 files usually takes up the majority of training time, leading to extremely low GPU
utilization. This ParallelDataLoader class is a simple way to greatly ameliorate this.
'''

from concurrent.futures import ThreadPoolExecutor
from dataset.Dataset import Dataset
import torch
import random

class ParallelDataLoader:
    def __init__(self, dataset: Dataset, batch_size: int, num_workers: int, shuffle: bool = False):
        self.dataset = dataset
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.shuffle = shuffle
        self.indices = list(range(len(self.dataset)))

        # sanity check
        assert not dataset.return_labels, 'ParallelDataLoader does not support returning labels as well!'

    def _fetch_data(self, index):
        # Fetch data given an index
        return self.dataset.__getitem__(index)

    def __iter__(self):
        # Shuffle data indices if required
        if self.shuffle:
            random.shuffle(self.indices)

        # This function yields batches of data
        self.executor = ThreadPoolExecutor(max_workers=self.num_workers)
        self.iterable_data = iter(self.indices)
        return self

    def __next__(self):
        # Fetch the next batch
        indices_batch = [next(self.iterable_data) for _ in range(self.batch_size)]
        futures = [self.executor.submit(self._fetch_data, index) for index in indices_batch]

        # results is of 'shape' (batch_size, n_views + optional[label, index], ...) 
        # and we need (n_views + ..., batch_size, ...)
        results = [future.result() for future in futures]

        if self.dataset.return_index:
            results = [result for result, _ in results]

        results_permuted = [
            torch.stack([results[j][i] for j in range(self.batch_size)]) for i in range(self.dataset.n_views)
        ]

        if self.dataset.return_index:
            results_permuted.append(indices_batch)

        return results_permuted

    def __len__(self):
        return len(self.dataset) // self.batch_size
