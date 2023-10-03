'''
useful utilities for deep learning stuff
'''

import json
import requests
from tqdm.auto import tqdm


def download_file(url, local_filename=None, chunk_size=32768):
    '''
    Utility to download files using a stream
    url: the url to download from
    local_filename: the filename (and path) to download file to
    chunk_size: size of data chunk to stream
    '''
    if local_filename is None:
        local_filename = url.split('/')[-1]

    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        # calculate byte size of file and open the progress bar:
        size = int(r.headers.get('content-length', 0))
        progress_bar = tqdm(total=size, unit='iB', unit_scale=True)

        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                progress_bar.update(len(chunk))

        progress_bar.close()

    return local_filename


def infinite_dataloader(dataloader):
    '''
    Makes any PyTorch dataloader 'infinite':
    simply use x = next(dataloader) to get the next batch!
    '''
    while True:
        for data in dataloader:
            yield data


def freeze(module):
    '''
    Freezes all module parameters
    '''
    for p in module.parameters():
        p.requires_grad = False


class ConfigFile:
    '''
    A class for convenient storage of configurations.
    '''
    def __init__(self, filename=None):
        '''
        filename: file to load from. If None, initializes a blank config
        '''
        self.__dict__['config'] = {}
        if filename:
            self.load(filename)

    def __getattr__(self, name):
        if name in self.config:
            return self.config[name]
        else:
            raise AttributeError(f'No such attribute: {name}')

    def __setattr__(self, name, value):
        if name == 'config':
            super().__setattr__(name, value)
        else:
            self.config[name] = value

    def load(self, filename):
        '''
        Loads a ConfigFile from JSON file
        '''
        with open(filename, 'r') as f:
            self.config = json.load(f)

    def save(self, filename):
        '''
        Saves the ConfigFile to JSON format
        '''
        with open(filename, 'w') as f:
            json.dump(self.config, f, indent=4)

    def __repr__(self):
        '''
        Provides a string representation of the ConfigFile
        '''
        return f'ConfigFile({json.dumps(self.config, indent=4)})'
