import os
import tempfile
import sqlite3
import pytest
from unittest.mock import patch
from assignment0.main import create_db, insert_incidents, download_pdf, extract_incidents, summarize_data, main

# Create a temporary directory for testing
TEMP_DIR = tempfile.gettempdir()

# Test create_db function
def test_create_db():
    db_path = os.path.join(TEMP_DIR, 'test.db')
    create_db(db_path)
    assert os.path.exists(db_path)

# Test insert_incidents function
def test_insert_incidents():
    db_path = os.path.join(TEMP_DIR, 'test.db')
    create_db(db_path)
    incidents = [('2024-01-01 12:00', '1', 'Location 1', 'Nature 1', 'Ori 1'),
                 ('2024-01-02 13:00', '2', 'Location 2', 'Nature 2', 'Ori 2')]
    insert_incidents(db_path, incidents)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM incidents")
    count = cur.fetchone()[0]
    conn.close()
    assert count == len(incidents)

# Test download_pdf function
@patch('main.requests.get')
def test_download_pdf(mock_get):
    mock_response = mock_get.return_value
    mock_response.content = b'test pdf content'
    url = 'http://example.com/incident_report.pdf'
    save_path = os.path.join(TEMP_DIR, 'incident_report.pdf')
    download_pdf(url)
    assert os.path.exists(save_path)

# Test extract_incidents function
def test_extract_incidents():
    pdf_path = os.path.join(TEMP_DIR, 'test.pdf')
    with open(pdf_path, 'w') as f:
        f.write('''
            Date/Time  Incident Number  Location  Nature  Incident ORI
            2024-01-01 12:00 1 Location 1 Nature 1 Ori 1
            2024-01-02 13:00 2 Location 2 Nature 2 Ori 2
        ''')
    incidents = extract_incidents(pdf_path)
    assert len(incidents) == 2
    assert incidents[0] == ['2024-01-01 12:00', '1', 'Location 1', 'Nature 1', 'Ori 1']
    assert incidents[1] == ['2024-01-02 13:00', '2', 'Location 2', 'Nature 2', 'Ori 2']

# Test summarize_data function
def test_summarize_data():
    db_path = os.path.join(TEMP_DIR, 'test.db')
    create_db(db_path)
    incidents = [('2024-01-01 12:00', '1', 'Location 1', 'Nature 1', 'Ori 1'),
                 ('2024-01-02 13:00', '2', 'Location 2', 'Nature 2', 'Ori 2')]
    insert_incidents(db_path, incidents)
    summary = summarize_data(db_path)
    assert summary == [('Nature 1', 1), ('Nature 2', 1)]

# Test main function
@patch('main.download_pdf')
@patch('main.extract_incidents')
@patch('main.summarize_data')
def test_main(mock_summarize_data, mock_extract_incidents, mock_download_pdf):
    mock_download_pdf.return_value = None
    mock_extract_incidents.return_value = [
        ('2024-01-01 12:00', '1', 'Location 1', 'Nature 1', 'Ori 1'),
        ('2024-01-02 13:00', '2', 'Location 2', 'Nature 2', 'Ori 2')
    ]
    db_path = os.path.join(TEMP_DIR, 'test.db')
    main('http://example.com/incident_report.pdf')
    assert mock_summarize_data.called

