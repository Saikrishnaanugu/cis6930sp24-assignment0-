import os
import tempfile
import sqlite3
from unittest.mock import patch
import pytest

from assignment0.main import create_db, insert_incidents, download_pdf, extract_incidents, summarize_data, main

# Create a temporary directory for testing
TEMP_DIR = tempfile.gettempdir()

# Test Case 1: Valid URL
def test_valid_url():
    # Define a valid URL
    valid_url = "https://www.normanok.gov/sites/default/files/documents/""2024-01/2024-01-01_daily_incident_summary.pdf"

    # Call the main function with the valid URL
    main(valid_url)

    # Check if the SQLite database and PDF file were created
    db_path = os.path.join("resources", "normanpd.db")
    pdf_path = os.path.join("docs", "incident_report.pdf")
    assert os.path.exists(db_path)
    assert os.path.exists(pdf_path)



