import os
from datetime import datetime
STORAGE_PATH=os.path.join("storage","pdfs")

class FileManager:
    # This method initializes the FileManager class by creating the storage directory if it does not already exist.
    def __init__(self):
        os.makedirs(STORAGE_PATH, exist_ok=True)
        
    # method saves the uploaded file to the specified storage path with a unique filename   that includes a timestamp to avoid conflicts.
    # returns the file path where the document is stored.
    def save_file(self, file):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename=f"{timestamp}_{file.name}"
        filepath=os.path.join(STORAGE_PATH, filename)

        with open(filepath, "wb") as f:
            f.write(file.read())
            
        return filepath
        

        