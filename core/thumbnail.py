import os
import pymupdf
THUMBNAIL_PATH=os.path.join("storage","thumbnail") 

class ThumbnailGenerator:

    # Initialize the class and ensure the thumbnail directory exists
    def __init__(self):
        os.makedirs(THUMBNAIL_PATH, exist_ok=True)

    # Logic to convert the first page of the PDF to an image and save it as a thumbnail
    def generate_thumbnail(self, file_path):
        # This is a placeholder implementation. You can use libraries like PyMuPDF or pdf2image to achieve this.
        doc=pymupdf.open(file_path)
        page=doc.load_page(0)
        pix=page.get_pixmap()
        basepath=os.path.basename(file_path).replace('.pdf', '.png')
        thumbnail_path=os.path.join(THUMBNAIL_PATH, basepath)
        pix.save(thumbnail_path)

        doc.close()
        # Code to generate thumbnail and save to thumbnail_path
        return thumbnail_path
    
    # Logic to get the total number of pages in the PDF
    def get_total_pages(self, file_path):
        doc=pymupdf.open(file_path)
        total_pages=doc.page_count
        doc.close()
        return total_pages