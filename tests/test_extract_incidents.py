import os
from tempfile import TemporaryDirectory
import pytest
from assignment0.main import extract_incidents




@pytest.fixture
def pdf_path_with_data():
    # Create a temporary directory and generate a test PDF file with sample incident data.
    with TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, 'test_incidents.pdf')
        with open(pdf_path, 'w', encoding='utf-8') as pdf_file:
            pdf_file.write("""
            2022-01-01 12:00:00 Incident1 Location1 Nature1 ORI1
            2022-01-02 13:00:00 Incident2 Location2 Nature2 ORI2
            2022-01-03 14:00:00 Incident3 Location3 Nature3 ORI3
            """)
        yield pdf_path

# def test_extract_incidents(pdf_path_with_data):
#     # Test extracting incidents from a sample PDF file.
#     incidents = extract_incidents(pdf_path_with_data)
    
#     assert len(incidents) == 3
    
#     # Verify the extracted data for each incident.
#     assert incidents[0] == ('2022-01-01 12:00:00', 'Incident1', 'Location1', 'Nature1', 'ORI1')
#     assert incidents[1] == ('2022-01-02 13:00:00', 'Incident2', 'Location2', 'Nature2', 'ORI2')
#     assert incidents[2] == ('2022-01-03 14:00:00', 'Incident3', 'Location3', 'Nature3', 'ORI3')

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
