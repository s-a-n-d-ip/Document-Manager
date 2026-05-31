from db.repository import DocumentRepository
from core.filemanager import FileManager
from core.thumbnail import ThumbnailGenerator
class DocumentService:
    def __init__(self):
        self.document_repository = DocumentRepository()
        self.file_manager = FileManager()
        self.thumbnail_generator = ThumbnailGenerator()
        pass

    def upload_document(self, upload_file, tags, description, lecturer_date=None):
        document=[]
        #save the file
        file_path=self.file_manager.save_file(upload_file)
       
        thumbnail_path=self.thumbnail_generator.generate_thumbnail(file_path)
        total_pages=self.thumbnail_generator.get_total_pages(file_path)
        #generate thumbnail
        #get total pages
        #generate upload date
        #convert pdf to images
        #save to db
        #self.document_repository.add_document(document)
        