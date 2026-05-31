import os
from datetime import datetime
STORAGE_PATH=os.path.join("storage","pdfs")

class FileManager:
    def __init__(self):
        pass

    def save_file(self, file):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename=f"{timestamp}_{file.name}"
        filepath=os.path.join(STORAGE_PATH, filename)
        with open(filepath, "wb") as f:
            f.write(file.read())
        return filepath
        

        