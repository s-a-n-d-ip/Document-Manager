import pymupdf
import os

class Pdf_Reader:
    # This method converts a PDF file into a series of images, one for each page, and saves them in a folder named after the PDF file. It uses the PyMuPDF library to handle the PDF processing and image generation.
    def convert_pdf_to_images(self, file_path):
        folder_name=os.path.basename(file_path).replace('.pdf','')
        folder_path=os.path.join("storage","pdfs",folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        doc = pymupdf.open(file_path)

        images = []
        for i in range(len(doc)):
            page=doc.load_page(i)
            matrix=pymupdf.Matrix(2, 2)
            pix = page.get_pixmap(matrix=matrix)
            images_path=os.path.join(folder_path,f"page_{i+1}.png")
            pix.save(images_path)
            images.append(images_path)
            
        doc.close()
        return images