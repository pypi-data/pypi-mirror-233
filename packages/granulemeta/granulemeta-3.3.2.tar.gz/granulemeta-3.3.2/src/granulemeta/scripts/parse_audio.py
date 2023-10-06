#!/usr/bin/env python3
'''
|
|------------------------------------------------------------------------------
|
|  PARSE_AUDIO.PY
|
|  UPDATED:    2023-08-09
|  AUTHOR:     kent campbell
|  CONTACT:    campbellkb@ornl.gov
|
|  DESCRIPTION
|
|     This module provides functions for processing audio (wav, mp3) granules
|
|------------------------------------------------------------------------------
|
'''
# | Python 3 standard library |
from calendar import timegm
from os.path import sep, splitext, split as fsplit
from time import gmtime, strftime, strptime

# | Third party packages |
from tinytag import TinyTag

# | Local packages |
try:
    from utilities import datetime_override, file_checksum, get_file_size
except:
    from scripts.utilities import datetime_override, file_checksum, get_file_size

# |----------------------------------------------------------------------------
# | AUDIO granule functions
# |----------------------------------------------------------------------------
def audio_metadata(input_file: str, cfg_dict: dict = None):
    ''' Get metadata from an AUDIO granule
    
    Args:
        input_file (str): The path to an AUDIO granule.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.

    Returns:
        record (dict): Dictionary of metadata for the granule.
    '''
    try:
        metadata = {'filename': fsplit(input_file)[1],
                    'subdir': fsplit(input_file)[0].lstrip(sep)}

        # Add to metadata dictionary in stages
        metadata['attributes'] = audio_attributes(input_file)
        metadata['coordinates'] = audio_coordinates(input_file, cfg_dict)

        if not cfg_dict['no_stats']:
            metadata['statistics'] = audio_statistics(input_file)
        else:
            metadata['statistics'] = None

        metadata['variables'] = audio_variables(input_file)

        properties = audio_properties(input_file, cfg_dict)

        record = {'metadata': metadata,
                  'properties': properties
        }

        return record
    except:
        return None

def audio_attributes(input_file: str):
    '''Process an AUDIO granule's attributes.

    Args:
        input_file (str): The path to an AUDIO granule.
    
    Returns:
        dictionary of items for the attributes portion of the metadata
    '''
    try:
        dataset = TinyTag.get(input_file)

        attributes = {
            # Get some basic metadata about the audio dataset.
            'bitrate': dataset.bitrate,
            'duration': dataset.duration,
            'filesize': dataset.filesize,  # This is duplicating metadata already included when audio_properties() is run.
            'samplerate': dataset.samplerate
        }

        return attributes
    except:
        return None

def audio_coordinates(input_file: str, cfg_dict: dict = None):
    '''Process an AUDIO granule's coordinates.

    Args:
        input_file (str): The path to an AUDIO granule.
    
    Returns:
        None
    '''
    # This is mostly a function stub. It's here in case there becomes a 
    # way to get spatial data from an AUDIO file in the future. 

    temporal = audio_temporal(cfg_dict)

    coordinates = {
        'time': {'min': temporal['start_time'], 'max': temporal['end_time']},
    }

    return coordinates

def audio_temporal(cfg_dict: dict = None):
    '''Process an AUDIO granule's temporal extents.

    Args:
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.
    
    Returns:
        dictionary of items for the temporal extents of the metadata
    ''' 
    start_time, end_time = datetime_override(None, None, cfg_dict)

    temporal = {
        'start_time': start_time,
        'end_time': end_time,
    }

    return temporal

def audio_statistics(input_file: str):
    '''Process an AUDIO granule's statistics.

    Args:
        input_file (str): The path to an AUDIO granule.
    
    Returns:
        None
    '''
    # This is a function stub. It's here in case there becomes a way
    # to get statistics data from an AUDIO file in the future. 
    return None

def audio_variables(input_file: str):
    '''Process an AUDIO granule's variable list.

    Args:
        input_file (str): The path to an AUDIO granule.
    
    Returns:
        None
    '''
    # This is a function stub. It's here in case there becomes a way 
    # to get information on variables for an AUDIO file in the future. 
    return None

def audio_properties(input_file: str, cfg_dict: dict = None):
    '''Process an AUDIO granule's properties.

    Args:
        input_file (str): The path to an AUDIO granule.
    
    Returns:
        dictionary of items for the properties portion of the metadata
    '''
    if not cfg_dict['no_checksum']:
        checksum = file_checksum(input_file)
    else:
        checksum = None

    properties = {
        'format': 'audio',
        'size': get_file_size(input_file),
        'checksum': checksum,
    }

    return properties

def is_audio_granule(input_file: str):
    '''Determine if granule is an AUDIO granule.

    Args:
        input_file (str): The path to a granule.
    
    Returns:
        boolean indicating if it is an AUDIO granule.
    '''
    fext = splitext(input_file)[1]
    return fext in ['.wav', '.mp3']