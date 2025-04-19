import io
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_file(uploaded_file, st):
    file_extension = uploaded_file.name.split(".")[-1].lower()
    text = ""

    try:
        if file_extension == "txt":
            text = uploaded_file.getvalue().decode("utf-8")
        elif file_extension == "pdf":
            pdf_reader = PdfReader(io.BytesIO(uploaded_file.getvalue()))
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        elif file_extension in ["docx", "doc"]:
            doc = Document(io.BytesIO(uploaded_file.getvalue()))
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif file_extension in ["xlsx", "xls", "csv"]:
            if file_extension in ["xlsx", "xls"]:
                df = pd.read_excel(io.BytesIO(uploaded_file.getvalue()))
            else:
                df = pd.read_csv(io.BytesIO(uploaded_file.getvalue()))
            text = df.to_string()
        else:
            st.error(f"Unsupported file format: {file_extension}")
            return None

        return text
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None
