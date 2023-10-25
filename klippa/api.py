import requests
import json
import os
from rich import print

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class KlippaAPI:
    def __init__(self, api_key: str, template: str, file_path: str, fast: bool = False, save_json: str = None):
        self.api_key = api_key
        self.template = template
        self.file_path = file_path
        self.fast = fast
        self.save_json = save_json
        self.scanned_documents = []

    def scan(self):
        """
        Scan the contents of a folder (concurrently) or a single file
        """
        if os.path.isdir(self.file_path):
            # If file_path is a directory, scan all files in the directory concurrently (or subdirectories)
            for filename in os.listdir(self.file_path):
                file_full_path = os.path.join(self.file_path, filename)
                self.scan_document(file_full_path)
                
            self.monitor_folder()

        elif os.path.isfile(self.file_path):
            # If file_path is a single file, scan it
            self.scan_document(self.file_path)
        else:
            print(f"Invalid file path: {self.file_path}")


    def scan_document(self, single_file_path: str):
        """
        Scan a file and call the appropriate API requests
        """
        # Parameters for the request
        base_url = "https://custom-ocr.klippa.com/api/v1"
        extraction_mode = "fast" if self.fast else "full" 
        url = f"{base_url}/parseDocument/{self.template}"

        # Prepare request headers
        headers = {"X-Auth-Key": self.api_key}
        files = {"document": open(single_file_path, "rb")}
        data = {"pdf_text_extraction": extraction_mode}

        try:
            response = requests.post(url=url, headers=headers, files=files, data=data)
        except requests.exceptions.ConnectionError as e:
            print("error", str(e))
        
        if response.status_code == 200:
            data = response.content.decode()
            dict_data = json.loads(data)

            if self.save_json:
                json_object = json.dumps(dict_data, indent=4)
                output_path = self.sanitize_file_path(self.save_json)

                with open(output_path, "w") as outfile:
                    outfile.write(json_object)
            else:
                print(dict_data)

            self.scanned_documents.append(dict_data) 
            self.print_folder_totals()
        else:
            error_message = f"Error: {response.status_code} - {response.reason}"
            print(error_message)


    def sanitize_file_path(self, single_file_path: str) -> str:
        """
        Sanitize the file path to avoid overwriting existing files
        """
        file_path_sanitized = single_file_path
        if not single_file_path.endswith(".json"):
            file_path_sanitized = f"{single_file_path}.json"

        if os.path.exists(file_path_sanitized):
            cnt = 1
            tmp = file_path_sanitized.split(".json")[0]
            while os.path.exists(f"{tmp}({cnt}).json"):
                cnt += 1

            file_path_sanitized = f"{tmp}({cnt}).json"
        return file_path_sanitized
        
    def monitor_folder(self):
        """
        Monitor a folder for new files and scan them
        """

        event_handler = Handler(api=self)
        observer = Observer()
        observer.schedule(event_handler, path=self.file_path, recursive=True)
        observer.start()
        try:
            while True:
                pass
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def print_folder_totals(self):
        total_amount = 0
        total_vat = 0
        for doc in self.scanned_documents:
            if not "data" in doc:
                continue
            if not doc["data"]["parsed"]:
                continue
            if not "amount" in doc["data"]["parsed"] or not "vatamount" in doc["data"]["parsed"]:
                continue
            total_amount += doc["data"]["parsed"]["amount"]
            total_vat += doc["data"]["parsed"]["vatamount"]
        if total_amount == 0:
            return
        print(f"Total amount: {total_amount}")
        print(f"Total VAT: {total_vat}")
        print(f"Vat percentage: {total_vat / total_amount * 100}")



class Handler(FileSystemEventHandler):
    
    def __init__(self, api: KlippaAPI):
        self.api = api

    def on_created(self, event):
        if event.is_directory:
            return None
 
        print("New file added to folder- % s." % event.src_path)
        print("Scanning file...")
        self.api.scan_document(event.src_path)