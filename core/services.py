from datetime import datetime

from db.repository import DocumentRepository
from core.filemanager import FileManager
from core.thumbnail import ThumbnailGenerator
from core.reader import Pdf_Reader
from core.models import Document
class DocumentService:
    def __init__(self):
        self.document_repository = DocumentRepository()
        self.file_manager = FileManager()
        self.thumbnail_generator = ThumbnailGenerator()
        self.pdf_reader = Pdf_Reader()
        

    def upload_document(self, upload_file, tags, description, lecturer_date=None):
        #save the file
        file_path=self.file_manager.save_file(upload_file)
        #generate thumbnail
        thumbnail_path=self.thumbnail_generator.generate_thumbnail(file_path)
        #get total pages
        total_pages=self.thumbnail_generator.get_total_pages(file_path)
        #convert pdf to images
        pdf_images=self.pdf_reader.convert_pdf_to_images(file_path)
        # name, path, thumbnail_path, tags, description, upload_date, lecturer_date, total_pages
        # document.append(upload_file.filename)
        # document.append(file_path)
        # document.append(thumbnail_path)
        # document.append(tags)
        # document.append(description)
        # document.append(datetime.now().strftime("%Y-%m-%d")) #upload date
        # document.append(lecturer_date)
        # document.append(total_pages)
        #save to db
        document=Document(upload_file.name,file_path,thumbnail_path, tags, description, datetime.now().strftime("%Y-%m-%d"), lecturer_date, total_pages)
        self.document_repository.add_document(document)
        