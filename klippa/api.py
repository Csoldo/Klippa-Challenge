import requests
import json
import os
import threading
from rich import print

def scan(api_key: str, template: str, file_path: str, fast: bool = False, save_json: str = None):
    """
    Scan the contents of a folder (concurrently) or a single file
    """
    output_path = save_json
    if os.path.isdir(file_path):
        # If file_path is a directory, scan all files in the directory concurrently (or subdirectories)
        threads = []
        for filename in os.listdir(file_path):
            file_full_path = os.path.join(file_path, filename)
            thread = threading.Thread(target=scan, args=(api_key, template, file_full_path, fast, output_path))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    elif os.path.isfile(file_path):
        # If file_path is a single file, scan it
        scan_document(api_key, template, file_path, fast, save_json)
    else:
        print(f"Invalid file path: {file_path}")



def scan_document(api_key: str, template: str, file_path: str, fast: bool = False, save_json: str = None):
    """
    Scan a file and call the appropriate API requests
    """
    # Parameters for the request
    base_url = "https://custom-ocr.klippa.com/api/v1"
    extraction_mode = "fast" if fast else "full" 
    url = f"{base_url}/parseDocument/{template}"
            
    # Prepare request headers
    headers = {"X-Auth-Key": api_key}
    files = {"document": open(file_path, "rb")}
    data = {"pdf_text_extraction": extraction_mode}

    try:
        response = requests.post(url=url, headers=headers, files=files, data=data)
    except requests.exceptions.ConnectionError as e:
        print("error", str(e))
    
    if response.status_code == 200:
        data = response.content.decode()
        dict_data = json.loads(data)

        if save_json:
            json_object = json.dumps(dict_data, indent=4)
            output_path = sanitize_file_path(save_json)

            with open(output_path, "w") as outfile:
                outfile.write(json_object)
        else:
            print(dict_data)
    else:
        error_message = f"Error: {response.status_code} - {response.reason}"
        print(error_message)


def sanitize_file_path(file_path: str) -> str:
    """
    Sanitize the file path to avoid overwriting existing files
    """
    file_path_sanitized = file_path
    if not file_path.endswith(".json"):
        file_path_sanitized = f"{file_path}.json"

    if os.path.exists(file_path_sanitized):
        cnt = 1
        tmp = file_path_sanitized.split(".json")[0]
        while os.path.exists(f"{tmp}({cnt}).json"):
            cnt += 1

        file_path_sanitized = f"{tmp}({cnt}).json"
    return file_path_sanitized
    
