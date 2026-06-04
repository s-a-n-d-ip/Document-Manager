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
    def search_documents(self, search_tag=None, search_date=None):
        conn=create_connection()
        cursor=conn.cursor()
        params=[]
        conditions=[]
        if search_tag:
            conditions.append("tags LIKE ?")
            params.append(f"%{search_tag}%")
        if search_date:
            conditions.append("lecturer_date = ?")
            params.append(search_date.strftime("%Y-%m-%d"))

        if conditions:
            query="SELECT * FROM documents WHERE "
            query += "or".join(conditions)
        cursor.execute(query, params)
        results=cursor.fetchall()
        conn.close()
        for row in results:
            print(row)
        return [Document(*rows)for rows in results] # returning list of Document objects created from the query results