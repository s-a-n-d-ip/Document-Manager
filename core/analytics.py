from datetime import datetime
from db.database import create_connection
class AnalyticsService:
    def record_page_visit(self, document_id, page_number):
        conn = create_connection()
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO page_visits (document_id, page_number, timestamp)
            VALUES (?, ?, ?)
        ''', (document_id, page_number, timestamp))
        conn.commit()
        conn.close()

    def get_page_visits(self, document_id):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT count(distinct page_number) from page_visits where document_id=?
        ''', (document_id,))
        visits = cursor.fetchone()[0]
        conn.close()
        return visits if visits else 0
    
    def record_app_visit(self, event_type):
        conn = create_connection()
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO App_Visit (event_type, timestamp)
            VALUES (?, ?)
        ''', (event_type, timestamp))
        conn.commit()
        conn.close()    

    def get_app_visits(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT event_type, count(*) as visit_count FROM App_Visit GROUP BY event_type
        ''')
        visits = cursor.fetchall()
        conn.close()
        return visits 
    
    def reset_analytics(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM page_visits')
        cursor.execute('DELETE FROM App_Visit')
        conn.commit()
        conn.close()