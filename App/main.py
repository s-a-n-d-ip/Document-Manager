import streamlit as st
import os
import sys
from dotenv import load_dotenv


#Setup the base directory and add it to the system path to import the database module,here we are getting main.py directory and then going one level up to access the db folder and database.py file. This allows us to call the init_db function to set up our database when the app starts.
BASE_DIR=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

# Load environment variables from .env file to access the sensitive data
load_dotenv(os.path.join(BASE_DIR, '.env'))
ADMIN_PASSWORD=os.getenv("ADMIN_PASSWORD")

from db.database import init_db
from core.services import DocumentService
from core.analytics import AnalyticsService


# search result session state variable is used to store the results of the search query so that we can display them after the search button is clicked.
if "search_result" not in st.session_state:
    st.session_state.search_result = []

# reader_mode session state variable is used to track whether the user is currently in the PDF reader view. This allows us to conditionally render the search results or the PDF reader based on the user's interaction.
if "reader_mode" not in st.session_state:
    st.session_state.reader_mode = False

# selected_doc session state variable is used to store the currently selected document when the user clicks on the "View PDF" button.
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

# current_page session state variable is used to track the current page number when the user is viewing a PDF in the reader mode.
if "current_page" not in st.session_state:
    st.session_state.current_page = 1

# show_reset_button session state variable is used to track whether the user is currently in the process of resetting the application state.
if "show_reset_button" not in st.session_state:
    st.session_state.show_reset_button = False

document_service = DocumentService()
analytics_service = AnalyticsService()

init_db()

st.set_page_config(page_title="PDF Manager", page_icon="📚",layout="wide")
st.title("📚 Modern PDF Manager")
st.divider()

# Admin Control section provides a button to clean the database and reset the application state. 
st.subheader("⚙️ Admin Control")

if st.button("🧹 Clean Database"):
    st.session_state.show_reset_button = True

if st.session_state.show_reset_button:
    password=st.text_input("Enter admin password to reset analytics data:", type="password")

    if st.button("Confirm Reset"):
        if password == ADMIN_PASSWORD:
            import shutil
            # Remove the existing database file
            data_path=os.path.join("Data","documents.db")

            if os.path.exists(data_path):
                os.remove(data_path)

            # Remove the existing PDF images
            pdf_path=os.path.join("storage","pdfs")
            thumbnail_path=os.path.join("storage","thumbnail")

            # Remove the existing PDF images and thumbnails directories and their contents
            shutil.rmtree(pdf_path, ignore_errors=True)
            shutil.rmtree(thumbnail_path, ignore_errors=True)

            # Recreate the directories after deletion
            os.makedirs(pdf_path, exist_ok=True)
            os.makedirs(thumbnail_path, exist_ok=True) 

            st.success("✅ System reset successfully. Restart app.")
            st.session_state.show_reset_button = False
            st.session_state.search_result = []
            st.session_state.selected_doc = None
            st.session_state.current_page = 0
            st.session_state.reader_mode = False
            st.rerun()
        else:
            st.error("❌ Incorrect password")
            st.session_state.show_reset_button = False
            st.rerun()

tabs=st.tabs(["Upload","Search & View","Anyalitcs"])

with tabs[0]:
    st.header("Upload PDF")

    upload_file=st.file_uploader("Upload your PDF files here",type=["pdf"])
    tags=st.text_input("Enter tags for the PDF (comma-separated):")
    description=st.text_area("Enter a description for the PDF:")
    lecturer_date=st.date_input("Select the lecture date(Optional):")

    if st.button("Upload",on_click=lambda: st.success("PDF Uploaded Successfully!")):
        analytics_service.record_app_visit("upload click")
        if upload_file and tags and description:
            # Here we add the logic to save the PDF file, its metadata, and thumbnail to the database and file system.
            # For example, we could save the file to a specific directory, generate a thumbnail, and then insert a record into the database with the file path, tags, description, etc.
            document_service.upload_document(upload_file, tags, description, lecturer_date)
        else:
            st.error("Please fill in all the required fields and upload a PDF file.")

with tabs[1]:
    st.header("Search & View")

    col1,col2=st.columns(2)

    with col1:
        search_tag=st.text_input("Search by tags:")

    with col2:
        search_date=st.date_input("Search by date:",value=None)

    if st.button("Search"):
        analytics_service.record_app_visit("search click")
        # Here we would implement the logic to search the database for PDFs matching the search criteria (tags and/or date) and display the results.
        st.session_state.search_result = document_service.search_documents(search_tag=search_tag if search_tag else None, search_date=str(search_date) if search_date else None)
    
    result=st.session_state.search_result
    # checks search results and reader mode to conditionally render the search results or the PDF reader view.

    if result and not st.session_state.reader_mode:
        st.subheader({f"Found {len(result)} matching documents:"})
        container=st.container(height=500)
        with container:
            for doc in result:
                col1,col2=st.columns([1,3])

                with col1:
                    if doc.thumbnail_path and os.path.exists(doc.thumbnail_path):
                        st.image(doc.thumbnail_path, width=100)

                with col2:
                    st.write(f"**Filename:** {doc.filename}")
                    st.write(f"**Tags:** {doc.tags}")
                    st.write(f"**Description:** {doc.description}")
                    st.write(f"**Lecture Date:** {doc.lecturer_date}")
                    if st.button("View PDF", key=doc.id):
                        analytics_service.record_app_visit("view click")
                        st.session_state.selected_doc = doc
                        st.session_state.current_page = 1
                        st.session_state.reader_mode = True
                        st.rerun()

    # checks if the user has clicked on a document to view and if the reader mode is activated. If so, it renders the PDF reader interface
    if st.session_state.reader_mode and st.session_state.selected_doc:
            st.write("Reader mode activated")

            doc=st.session_state.selected_doc

            st.subheader(f"** 📖 Filename:** {doc.filename}")
            folder_name=os.path.basename(doc.path).replace(".pdf","")
            images_folder=os.path.join("storage","pdfs",folder_name)
            st.write("Images folder:", images_folder)
            st.write("Files :", os.listdir(images_folder) if os.path.exists(images_folder) else "Folder not found")

            if not os.path.exists(images_folder):
                st.error("PDF images not found. Please check the file path and ensure the PDF was processed correctly.")
            else:
                images=sorted(os.listdir(images_folder))
                total_pages=doc.total_pages
                current_page=st.session_state.current_page
                col1,col2,col3=st.columns([1,2,1])
                # The Previous and Next buttons allow the user to navigate through the pages of the PDF.
                with col1:
                    if st.button("⬅ Previous Page") and current_page > 1:
                        analytics_service.record_app_visit("previous page")
                        st.session_state.current_page -= 1
                        st.rerun()
                with col3:
                    if st.button("Next Page ➡") and current_page < total_pages:
                        analytics_service.record_app_visit("next page")
                        st.session_state.current_page += 1
                        st.rerun()

                image_path=os.path.join(images_folder, images[current_page-1])
                st.image(image_path, width="stretch")

                #record page visit
                analytics_service.record_page_visit(doc.id, st.session_state.current_page)

                unique_pages=analytics_service.get_page_visits(doc.id)

                progress=(unique_pages/total_pages)*100 if doc.total_pages else 0

                st.write(f"Page {current_page} of {total_pages}")

                st.progress(progress/100)

                st.write(f"File name: {doc.filename}   [Completed page {unique_pages} of {doc.total_pages} ({progress:.2f}%)]")

            if(st.button("Close PDF Reader")):
                analytics_service.record_app_visit("close reader")
                st.session_state.reader_mode=False
                st.rerun()
                

with tabs[2]:
    st.header("Analytics")

    if st.button("Reset Analytics Data"):
        analytics_service.reset_analytics()
        st.success("Analytics data reset successfully!")

    #The analytics tab displays the app visits and document reading progress. 
    st.subheader("App Visits")
    app_visits=analytics_service.get_app_visits()
    import pandas as pd

    app_visits_df=pd.DataFrame(app_visits,columns=["Event Type","Visit Count"])

    if app_visits_df.empty:
        st.write("No app visits recorded yet.")
    else:
        st.bar_chart(app_visits_df.set_index("Event Type"))

    doc=DocumentService().get_all_documents()

    data=[]

    # For each document, we retrieve the number of unique pages visited and calculate the reading progress as a percentage. We then create a DataFrame to display this information in a tabular format.
    for doc in doc:
        unique_pages=analytics_service.get_page_visits(doc.id)
        progress=(unique_pages/doc.total_pages)*100 if doc.total_pages else 0
        data.append({
            "Filename": doc.filename,
            "Pages Read": unique_pages,
            "Total Pages": doc.total_pages,
            "Progress (%)": f"{progress:.2f}%"
        })
    
    analytics_df=pd.DataFrame(data)
    st.subheader("Document Reading Progress")
    
    if analytics_df.empty:
        st.write("No document visits recorded yet.")
    else:
        st.dataframe(analytics_df)