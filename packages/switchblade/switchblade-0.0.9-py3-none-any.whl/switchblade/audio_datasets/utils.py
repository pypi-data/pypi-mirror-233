'''
Dataset-related utilities
'''

import requests
from tqdm.auto import tqdm

def download_file(url, local_filename=None, chunk_size=32768):
    '''
    neat utility to download files using a stream
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