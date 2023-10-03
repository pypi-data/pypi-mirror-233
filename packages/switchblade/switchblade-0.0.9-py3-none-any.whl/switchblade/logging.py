'''
all logging-related utilities
'''

import os

def setup_logging(run_name, rootdir):
    '''
    set up logging for this run
    '''
    os.makedirs(os.path.join(rootdir, 'models'), exist_ok=True)
    os.makedirs(os.path.join(rootdir, 'logs'), exist_ok=True)
    os.makedirs(os.path.join(rootdir, 'models', run_name), exist_ok=True)
    os.makedirs(os.path.join(rootdir, 'logs', run_name), exist_ok=True)

def get_model_path(run_name, rootdir):
    return os.path.join(rootdir, 'models', run_name)

def get_logs_path(run_name, rootdir):
    return os.path.join(rootdir, 'logs', run_name)