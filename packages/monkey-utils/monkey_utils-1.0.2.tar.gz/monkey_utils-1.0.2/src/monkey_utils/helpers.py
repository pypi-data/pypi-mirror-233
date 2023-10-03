import time
import requests
import logging
import random 
import base64
import json 
from functools import wraps

def timeit(func):
    """Decorator to cal time process a function"""
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logging.info(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


def random_string(length):
    """Generates a random string of the given length.
    Args:
    length: The length of the string to generate.

    Returns:
    A random string of the given length.
    """

    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(chars) for _ in range(length))


def covert_base64_to_bytes(base64_data):
    """
    Covert base64 into array data of audio
    Method:
        string base64 -> bytes -> array 
    Parameters: 
        base64_data: string base64 (Audio file with format base64)
    Returns:
       bytes data of audio
    """
    decode_string = base64.b64decode(base64_data)
    return decode_string

def push_data_s3(url, api_token, filename, data, media_type, bucket, folder):
    """
    Upload to save in S3 and get a path to read.
    """
    try:
        payload = {'description': '',
            'folder_path': folder,
            'bucket':  bucket}
        files=[
            ('file',(f"{filename}", data, media_type))
        ]
        headers = {
            'token': api_token
        }
        response = requests.request("POST", url, 
                    headers=headers, data=payload, files=files, timeout=2.5)
       
        json_response = json.loads(response.text)
        if response.status_code == 200 and json_response['status'] == "success":
            return json_response['data']['link']
    except Exception as e:
        logging.exception(f"Exception backup data into S3: {e}")
    return None