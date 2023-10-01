from flask import request

import os
import traceback
import json


"""Methods that are useful across multiple architecture servers"""


def clean_up(files_to_delete):
    if files_to_delete:
        for path in files_to_delete:
            os.remove(path)


def construct_full_error_message(architecture_root_dir, files_to_delete):
    message = construct_error_message(architecture_root_dir)
    try:
        clean_up(files_to_delete)
    except Exception:
        message += '\n\n...and failed to clean output directory, due to: \n' + traceback.format_exc(chain=False) + '\n'
    return message


def construct_error_message(architecture_root_dir):
    input_files = get_file_list(architecture_root_dir)
    return 'An error occurred while generating the output: \n' + traceback.format_exc() + \
           '\n\nPayload:\n' + json.dumps(request.json) + \
           '\n\nInput Audio Dir Listing: \n' + input_files


def get_file_list(folder):
    if os.path.exists(folder):
        return ', '.join(os.listdir(folder))
    else:
        return folder + ' does not exist'


def select_hardware(gpu_id):
    """Select which GPU will be used by setting the CUDA_VISIBLE_DEVICES environment variable. gpu_id can be an integer
    or a string. A typical values is '0', which will select the first CUDA-capable device. And empty string is also an
    acceptable value and will cause the CPU to be used instead of the GPU."""
    env = os.environ.copy()
    env['CUDA_VISIBLE_DEVICES'] = str(gpu_id)
    return env
