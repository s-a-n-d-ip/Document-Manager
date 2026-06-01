from db.database import create_connection
from core.models import Document
class DocumentRepository:
    
    def add_document(self, document:Document):
        conn=create_connection()
        cursor=conn.cursor()
        cursor.execute('''
            INSERT INTO documents (name, path, thumbnail_path, tags, description, upload_date, lecturer_date, total_pages)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)            
        ''', (
            document.filename, 
            document.path, 
            document.thumbnail_path, 
            document.tags, 
            document.description, 
            document.upload_date, 
            document.lecturer_date, 
            document.total_pages
            ))
        conn.commit()
        conn.close()
