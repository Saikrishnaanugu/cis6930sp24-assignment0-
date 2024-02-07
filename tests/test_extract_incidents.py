import os
from tempfile import TemporaryDirectory
import pytest
from pypdf import PdfWriter
from assignment0.main import extract_incidents

@pytest.fixture
def pdf_path_with_data():
    # Create a temporary directory and generate a test PDF file with sample incident data.
    with TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, 'test_incidents.pdf')
        writer = PdfWriter()
        writer.add_blank_page(200, 200)  # Add a blank page with width and height
        with open(pdf_path, 'wb') as pdf_file:
            writer.write(pdf_file)
        yield pdf_path

def test_extract_incidents_empty_pdf():
    # Test extracting incidents from an empty PDF file.
    with TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, 'empty.pdf')
        open(pdf_path, 'w').close()
        incidents = extract_incidents(pdf_path)
    
    assert len(incidents) == 0

def test_extract_incidents_invalid_pdf():
    # Test extracting incidents from an invalid PDF file (non-PDF file).
    with TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, 'invalid.pdf')
        with open(pdf_path, 'w') as pdf_file:
            pdf_file.write("This is not a valid PDF file.")
        incidents = extract_incidents(pdf_path)
    
    assert len(incidents) == 0


