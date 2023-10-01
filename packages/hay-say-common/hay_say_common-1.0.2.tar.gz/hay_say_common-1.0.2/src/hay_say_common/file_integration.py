import os

"""Constants and methods related to file integration between the UI container and the various AI Architecture 
containers"""


ROOT_DIR = os.path.join(os.path.expanduser('~'), 'hay_say')
CUSTOM_MODELS_DIR = os.path.join(ROOT_DIR, 'custom_models')
MODELS_DIR = os.path.join(ROOT_DIR, 'models')


if not os.path.exists(MODELS_DIR):
    # All Docker containers must have a shared volume mounted at MODELS_DIR. This is where character models are stored.
    raise Exception('"models" directory does not exist! Did you forget to mount the models volume?')


if not os.path.exists(CUSTOM_MODELS_DIR):
    # All Docker containers must have a shared volume mounted at CUSTOM_MODELS_DIR. This is where custom character
    # models were originally stored. This volume is no longer used, but it must still exist for backwards compatibility.
    raise Exception('custom_models directory does not exist! Did you forget to mount the custom_models volume?')


def get_model_path(architecture_name, character_name):
    """Deprecated. Use characters_dir instead.
    Returns the directory where the files for a given character model in a given architecture are stored."""
    character_dir = [os.path.join(model_dir, character_name)
                     for model_dir in model_dirs(architecture_name)
                     if os.path.exists(os.path.join(model_dir, character_name))]
    if len(character_dir) == 0:
        raise Exception('Character directory was not found! Expected to find a subdirectory named ' + character_name +
                        ' in one of these directories: ' + ', '.join(model_dirs(architecture_name)))
    elif len(character_dir) > 1:
        raise Exception('More than one character directory with the name ' + character_name + ' was found! Expected to '
                        'find only one subdirectory with that name among all of the following directories: ' +
                        ', '.join(model_dirs(architecture_name)) + '. Since more than one was found, it is '
                        'impossible to determine which one the user intended to use. All models must have unique '
                        'names.')
    else:
        return character_dir[0]


def model_dirs(architecture_name):
    """Deprecated. Use characters_dir or character_dir instead.
    Returns a list of all directories which may contain character subdirectories with model files for the given
    architecture."""
    return model_pack_dirs(architecture_name) \
        + [custom_model_dir(architecture_name)] \
        + [characters_dir(architecture_name)]


def model_pack_dirs(architecture_name):
    """Deprecated. Use characters_dir or character_dir instead.
    Returns a list of absolute paths to all the model pack directories for the given architecture."""
    return [directory for directory in possible_model_pack_dirs(architecture_name) if os.path.isdir(directory)]


def possible_model_pack_dirs(architecture_name):
    """A helper method for model_pack_dirs"""
    return [os.path.join(ROOT_DIR, architecture_name + '_model_pack_' + str(index)) for index in range(100)]


def custom_model_dir(architecture_name):
    """Deprecated. Use characters_dir or character_dir instead.
    Returns the directory containing custom models for the given architecture."""
    return guarantee_directory(os.path.join(CUSTOM_MODELS_DIR, architecture_name))


def characters_dir(architecture_name):
    """Returns the directory containing all the character model subdirectories for the given architecture."""
    return guarantee_directory(os.path.join(MODELS_DIR, architecture_name, 'characters'))


def guarantee_directory(directory):
    """Creates the directory if it does not exist and returns the path to the directory that now definitely exists"""
    if not os.path.isdir(directory):
        os.makedirs(directory)
    return directory


def character_dir(architecture_name, character_name):
    """Returns the directory where the files for a given character model in a given architecture are stored."""
    return os.path.join(MODELS_DIR, architecture_name, 'characters', character_name)


def multispeaker_model_dir(architecture_name, model_name):
    """Returns the directory where multi-speaker models are stored for the given architecture."""
    return os.path.join(MODELS_DIR, architecture_name, 'multispeaker_models', model_name)

