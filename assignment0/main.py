
import argparse
import sqlite3
import requests
from pypdf import PdfReader  # Importing PdfReader from PyPDF2 for PDF processing
import os

# Database functions

def database_creation_sqlite(db_path):
    """
    # Creates a SQLite database with an 'incidents' table if it doesn't exist.

    Args:
    - db_path (str): Path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS incidents (
                   date_time TEXT, 
                   incident_number TEXT, 
                   location TEXT, 
                   nature TEXT, 
                   incident_ori TEXT)''')
    conn.commit()
    conn.close()

def incidents_insertion(db_path, incidents):
    """
    Inserts incident data into the 'incidents' table in the SQLite database.

    Args:
    - db_path (str): Path to the SQLite database file.
    - incidents (list): List of incident data to be inserted into the database.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM incidents")  # Clear the existing data in the table before inserting new data
    for incident in incidents:
        non_empty_fields = sum(1 for field in incident if field.strip())
        if non_empty_fields != 1:
            # Using parameterized query to prevent SQL injection vulnerabilities
            query = "INSERT INTO incidents (date_time, incident_number, location, nature, incident_ori) " \
                    "VALUES (?, ?, ?, ?, ?)"
            cur.execute(query, incident)
    conn.commit()
    conn.close()

# Download function

def pdf_file_download(url):
    """
    Downloads a PDF file from the given URL and saves it locally.

    Args:
    - url (str): URL of the PDF file to be downloaded.
    """
    save_path="./docs/incident_report.pdf"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)

# Extract function

def incidents_extractions_db(pdf_path):
    """
    Extracts incident data from a PDF file.

    Args:
    - pdf_path (str): Path to the PDF file containing incident data.

    Returns:
    - incidents (list): List of incident data extracted from the PDF.
    """
    reader = PdfReader(pdf_path)
    incidents = []
    start_indices = []
    found_indices = False
    
    for page in reader.pages:
        text = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False)
        lines = text.split('\n')
        incidents.extend(lines)
        
    # Remove unwanted lines
    del incidents[:3]
    del incidents[-1]

    # Find starting indices of each column by analyzing the first 10 lines
    for line in incidents[:10]:
        if not found_indices:
            start_indices = [0] if not line[0].isspace() else []  # Start with 0 if the first character is non-space
            space_count = 0
            
            for i in range(1, len(line)):  # Start from the second character
                if line[i].isspace():
                    space_count += 1
                else:
                    if space_count > 2:  # More than two spaces indicate a new column
                        start_indices.append(i)
                    space_count = 0  # Reset space count after a non-space character
                    
                if len(start_indices) == 5:  # Found all start indices
                    found_indices = True
                    break

    if not found_indices:
        raise ValueError("Unable to determine column start indices from the PDF.")

    newincidents = []

    # Now, use the detected start_indices to split the incidents
    for row in incidents:
        # Initially split the row based on your existing logic
        row_data = [cell.strip() for cell in row.split('  ') if cell.strip()]
        
        # If there are less than 5 columns, check for missing columns using start_indices
        if len(row_data) < 5:
            corrected_row = []
            for index, start in enumerate(start_indices):
                if index < len(row_data):
                    # Check if the current segment starts at the expected index
                    if row.find(row_data[index]) >= start:
                        corrected_row.append(row_data[index])
                    else:
                        corrected_row.append("")  # Insert empty string for missing column
                        row_data.insert(index, "")  # Adjust row_data to align with remaining columns
                else:
                    corrected_row.append("")  # Append empty strings for completely missing columns at the end
            newincidents.append(corrected_row)
        else:
            newincidents.append(row_data)
    
    return newincidents

# Status function 

def actions_data(db_path):
    """
    Summarizes incident data stored in the SQLite database.

    Args:
    - db_path (str): Path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Select non-empty natures
    cur.execute('''SELECT nature, COUNT(*) as count FROM incidents WHERE nature != '' GROUP BY nature ORDER BY count DESC, nature''')
    rows = cur.fetchall()
    # Select empty natures
    cur.execute('''SELECT nature, COUNT(*) as count FROM incidents WHERE nature = '' GROUP BY nature''')
    empty_rows = cur.fetchall()
    
    # Print non-empty natures
    for row in rows:
        print(f"{row[0]}|{row[1]}")
    # Print empty natures at the end
    for row in empty_rows:
        print(f"|{row[1]}")
   
    conn.close()

def database_output(db_path):
    """
    Prints all incident data stored in the SQLite database.

    Args:
    - db_path (str): Path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM incidents")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()

# Main function

def main(url):
    """
    Main function to orchestrate the process of downloading, extracting, storing, and summarizing incident data.

    Args:
    - url (str): URL of the PDF file containing incident data.
    """
    pdf_path = "docs/incident_report.pdf"
    pdf_file_download(url)   
    incidents = incidents_extractions_db(pdf_path)
    db_path = "resources/normanpd.db"
    database_creation_sqlite(db_path)
    incidents_insertion(db_path, incidents)
    actions_data(db_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary url.")
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)


