import streamlit as st
import os
import sys
#Setup the base directory and add it to the system path to import the database module,here we are getting main.py directory and then going one level up to access the db folder and database.py file. This allows us to call the init_db function to set up our database when the app starts.
BASE_DIR=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)
from db.database import init_db
from core.services import DocumentService

document_service = DocumentService()

init_db()
st.set_page_config(page_title="PDF Manager", page_icon="📚",layout="wide")
st.title("📚 Modern PDF Manager")
st.divider()
tab1,tab2,tab3=st.tabs(["Upload","Search & View","Anyalitcs"])
with tab1:
    st.header("Upload PDF")
    upload_file=st.file_uploader("Upload your PDF files here",type=["pdf"])
    tags=st.text_input("Enter tags for the PDF (comma-separated):")
    description=st.text_area("Enter a description for the PDF:")
    lecturer_date=st.date_input("Select the lecture date(Optional):")

    if st.button("Upload",on_click=lambda: st.success("PDF Uploaded Successfully!")):
        if upload_file and tags and description:
            # Here we add the logic to save the PDF file, its metadata, and thumbnail to the database and file system.
            # For example, we could save the file to a specific directory, generate a thumbnail, and then insert a record into the database with the file path, tags, description, etc.
            document_service.upload_document(upload_file, tags, description, lecturer_date)
        else:
            st.error("Please fill in all the required fields and upload a PDF file.")
with tab2:
    st.write("Search & View")
with tab3:
    st.write("Analytics")
