'''
Utility to retrieve a dataset, given ArgumentParser args
'''


from .AudioDataset import AudioDataset
from .DISCOXDataset import DISCOXDataset
from .EmoMusic import EmoMusic
from .GiantSteps import GiantStepsDataset
from .GTZAN import GTZANDataset
from .MagnaTagATune import MagnaTagATune
from .NSynth import NSynthDataset, NSynthInstrument, NSynthPitch

def get_dataset(args, transform=None):
    '''
    Returns a dataset of the given type
    '''

    if args.dataset.lower().startswith('nsynth'):
        # error detection
        assert args.subset is not None, 'Error: --subset arg must be provided for NSynth dataset!'
        
        dataset_class = {
            '' : NSynthDataset,
            'instrument' : NSynthInstrument,
            'pitch' : NSynthPitch
        }[args.dataset.lower()[6:]]

        dataset = dataset_class(
            args.dataroot, 
            subset=args.subset, 
            download=args.download_dataset, 
            return_labels=args.return_labels,
            n_samples=args.n_samples,
            sr=args.sr,
            preprocess_path=args.preprocess_path, 
            do_preprocessing=args.preprocess,
            label_type=args.label_type,
            classes=args.classes,
            transform=transform
        )
        print(f'Processed NSynth dataset of size {len(dataset)}')
    elif args.dataset.lower() == 'audio':
        dataset = AudioDataset(
            dataroot=args.dataroot, 
            return_labels=False, 
            labels=None,
            n_samples=args.n_samples, 
            sr=args.sr, 
            preprocess_path=args.preprocess_path,
            do_preprocessing=args.preprocess,
            transform=transform,
            cap_at=args.cap_at
        )
        print(f'Processed audio dataset of size {len(dataset)}')
    elif args.dataset.lower() == 'magnatagatune':
        dataset = MagnaTagATune(
            root=args.dataroot,
            download=args.download_dataset,
            subset=args.subset,
            split='pons2017',
            return_labels=args.return_labels,
            n_samples=args.n_samples,
            sr=args.sr,
            preprocess_path=args.preprocess_path,
            do_preprocessing=args.preprocess,
            cap_at=args.cap_at,
            transform=transform
        )
        print(f'Processed MagnaTagATune dataset of size {len(dataset)}')
    elif args.dataset.lower() == 'gtzan':
        dataset = GTZANDataset(
            dataroot=args.dataroot,
            subset=args.subset,
            return_labels=args.return_labels, 
            n_samples=args.n_samples,
            sr=args.sr,
            transform=transform,
            preprocess_path=args.preprocess_path,
            do_preprocessing=args.preprocess
        )
        print(f'Processed the GTZAN dataset of size {len(dataset)}')
    elif args.dataset.lower() == 'emomusic':
        dataset = EmoMusic(
            dataroot=args.dataroot,
            subset=args.subset,
            return_labels=args.return_labels,
            n_samples=args.n_samples,
            sr=args.sr,
            preprocess_path=args.preprocess_path,
            transform=transform,
            do_preprocessing=args.preprocess
        )
        print(f'Processed EmoMusic dataset of size {len(dataset)}')
    elif args.dataset.lower() == 'giantsteps':
        dataset = GiantStepsDataset(
            dataroot=args.dataroot,
            subset=args.subset,
            return_labels=args.return_labels, 
            n_samples=args.n_samples,
            sr=args.sr,
            transform=transform,
            preprocess_path=args.preprocess_path,
            do_preprocessing=args.preprocess
        )
        print(f'Processed the giantsteps dataset of size {len(dataset)}')
    elif args.dataset.lower() == 'discox':
        dataset = DISCOXDataset(
            dataroot=args.dataroot,
            subset=args.subset,
            max_workers=args.max_workers,
            dir_depth=args.dir_depth,

            download=args.download_dataset,
            n_samples=args.n_samples,
            sr=args.sr,
            transform=transform,
            preprocess_path=args.preprocess_path,
            do_preprocessing=args.preprocess,
            return_labels=args.return_labels,
            cap_at=args.cap_at,
            chunk_dataset=args.chunk_dataset,

            additional_audio_folder=args.additional_audio_folder
        )
        print(f'Processed the DISCOX dataset of total size {len(dataset)}')
    else:
        raise NotImplementedError
    
    dataset.n_views = args.n_views
    dataset.return_same_slice_p = args.return_same_slice_p
    
    return dataset