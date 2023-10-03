from concurrent.futures import ThreadPoolExecutor
import random
import torch


class ParallelDataLoader:
    def __init__(self, dataset, batch_size: int, num_workers: int, shuffle: bool = False):
        self.dataset = dataset
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.shuffle = shuffle
        self.indices = list(range(len(self.dataset)))


    def _fetch_data(self, index):
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

        # results is a list of tuples, each containing multiple items
        results = [future.result() for future in futures]

        # Initialize lists to hold batches of each item
        batches = [[] for _ in range(len(results[0]))]

        # Iterate over the results and separate each item, stacking them if they are torch tensors
        for result in results:
            for i, item in enumerate(result):
                if isinstance(item, torch.Tensor):
                    batches[i].append(item)
                else:
                    batches[i].append(torch.tensor(item))

        # Stack the batches into tensors
        batches = [torch.stack(batch) for batch in batches]

        return batches


    def __len__(self):
        return len(self.dataset) // self.batch_size