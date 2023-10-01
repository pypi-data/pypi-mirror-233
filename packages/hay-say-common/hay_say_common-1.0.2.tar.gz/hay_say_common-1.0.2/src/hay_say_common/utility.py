import librosa

import base64
import io
import os

"""Methods that are useful across multiple Hay Say coding projects and are not necessarily related to file integration, 
caching, or specific to servers"""


def create_link(existing_path, desired_link_path):
    """Guarantees the existence of a symlink file at desired_link_path pointing at existing_path. If a file already
    exists at desired_link_path, it will be replaced if it is not already a link file that is pointing at
    existing_path. existing_path must exist, and the directory name of desired_link_path must exist."""
    # Check if link file does not exist yet.
    if not os.path.lexists(desired_link_path):
        os.symlink(existing_path, desired_link_path)
    else:
        # Check if link file is pointing at a nonexistent file OR is pointing at the wrong file.
        # This condition also returns true if desired_link_path is an ordinary (non-link) file and existing_path != desired_link_path
        if not os.path.exists(desired_link_path) or not os.path.samefile(existing_path, desired_link_path):
            os.remove(desired_link_path)
            os.symlink(existing_path, desired_link_path)


def get_audio_from_src_attribute(src, encoding):
    _, raw = src.split(',')
    b64_output_bytes = raw.encode(encoding)
    output_bytes = base64.b64decode(b64_output_bytes)
    buffer = io.BytesIO(output_bytes)
    return librosa.load(buffer, sr=None)


def read_audio(path):
    return librosa.load(path, sr=None)


def get_singleton_file(folder):
    """Given a folder, return the full path of the single file within that folder. If there is no file in that folder,
    or if there is more than one file in that folder, raise an Exception."""
    potential_filenames = [file for file in os.listdir(folder)]
    if len(potential_filenames) > 1:
        raise Exception('more than one file was found in the indicated folder. Only one was expected.')
    elif len(potential_filenames) == 0:
        raise Exception('No file was found in the indicated folder.')
    return os.path.join(folder, potential_filenames[0])


def get_single_file_with_extension(directory, extension):
    """Finds the single file with the given extension in the specified directory. If there is no such file or if there
    is more than one file with the extension, throw an Exception. Otherwise, return the path to the file."""
    all_files = get_files_with_extension(directory, extension)
    if len(all_files) > 1:
        raise Exception('More than one file with the extension ' + extension + ' was found in ' + directory)
    elif len(all_files) == 0:
        raise Exception('file with extension ' + extension + ' not found in ' + directory)
    return all_files[0]


def get_files_with_extension(directory, extension):
    """Find all files with the given extension in the specified directory. Returns a list of paths."""
    extension = ('.' + extension) if extension[0] != '.' else extension
    return get_files_ending_with(directory, extension)


def get_files_ending_with(directory, endswith):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(endswith)]


def get_full_file_path(folder, filename_sans_extension):
    """Given a folder and a filename without an extension, find the full path of that file with the extension.
    Assumption: there should only be one file in the folder whose name without the extension is
    filename_sans_extension."""
    potential_filenames = [file for file in os.listdir(folder) if file.split('.')[0] == filename_sans_extension]
    if len(potential_filenames) > 1:
        raise Exception('more than one file with the same hash found')
    elif len(potential_filenames) == 0:
        raise Exception('file with name ' + filename_sans_extension + ' not found')
    return os.path.join(folder, potential_filenames[0])