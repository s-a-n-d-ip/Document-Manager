from datetime import datetime

from db.repository import DocumentRepository
from core.filemanager import FileManager
from core.thumbnail import ThumbnailGenerator
from core.reader import Pdf_Reader
from core.models import Document
class DocumentService:
    #This method initializes the DocumentService class by creating instances of the DocumentRepository, FileManager, ThumbnailGenerator, and Pdf_Reader classes.
    def __init__(self):
        self.document_repository = DocumentRepository()
        self.file_manager = FileManager()
        self.thumbnail_generator = ThumbnailGenerator()
        self.pdf_reader = Pdf_Reader()
        
    # This method handles the entire process of uploading a PDF document, including saving the file, generating a thumbnail, extracting metadata, and storing the information in the database.
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
        document=Document(id=None,filename=upload_file.name,path=file_path,thumbnail_path=thumbnail_path, tags=tags, description=description, upload_date=datetime.now().strftime("%Y-%m-%d"), lecture_date=lecturer_date, total_pages=total_pages)
        self.document_repository.add_document(document)
        
    # This method allows searching for documents based on tags and/or lecture date by delegating the search operation to the DocumentRepository.
    def search_documents(self, search_tag=None, search_date=None):
        return self.document_repository.search_documents(search_tag, search_date)