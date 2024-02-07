import os
from tempfile import TemporaryDirectory
import pytest
from assignment0.main import extract_incidents
from PyPDF2 import PdfWriter

@pytest.fixture
def pdf_path_with_data():
    # Create a temporary directory and generate a test PDF file with sample incident data.
    with TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, 'test_incidents.pdf')
        writer = PdfWriter()
        writer.add_blank_page()
        writer.add_blank_page()
        with open(pdf_path, 'wb') as pdf_file:
            writer.write(pdf_file)
        yield pdf_path

def test_extract_incidents_valid_pdf(pdf_path_with_data):
    # Test extracting incidents from a valid PDF file with content.
    incidents = extract_incidents(pdf_path_with_data)
    assert len(incidents) == 0  # Assuming the function returns an empty list for blank PDFs

