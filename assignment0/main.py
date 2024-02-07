# import argparse
# import sqlite3
# import requests
# from pypdf import PdfReader

# def download_pdf(url, filename):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  
#         with open(filename, 'wb') as file:
#             file.write(response.content)
#     except requests.RequestException as e:
#         print(f"Request failed: {e}")
#         return False
#     return True

# def extract_incidents(pdf_path):
#     incidents = []
#     try:
#         with open(pdf_path, 'rb') as file:
#             reader = PdfReader(file)
#             for page in reader.pages:
#                 text = page.extract_text()
#                 if text:
#                     lines = text.split('\n')
#                     for line in lines:
#                         data = line.split()
#                         if len(data) >= 5:
#                             incident_time = data[0]
#                             incident_number = data[1]
#                             incident_location = " ".join(data[2:-2])
#                             nature = data[-2]
#                             incident_ori = data[-1]
#                             incidents.append((incident_time, incident_number, incident_location, nature, incident_ori))
#     except Exception as e:
#         print(f"Failed to extract incidents from PDF: {e}")
#     return incidents

# def create_db(db_path):
#     try:
#         conn = sqlite3.connect(db_path)
#         cur = conn.cursor()
#         cur.execute('''CREATE TABLE IF NOT EXISTS incidents (
#                        date_time TEXT, 
#                        incident_number TEXT, 
#                        location TEXT, 
#                        nature TEXT, 
#                        incident_ori TEXT)''')
#         conn.commit()
#     except sqlite3.DatabaseError as e:
#         print(f"Database error: {e}")
#     finally:
#         conn.close()


# def insert_incidents(db_path, incidents):
#     try:
#         conn = sqlite3.connect(db_path)
#         cur = conn.cursor()
#         query = "INSERT INTO incidents (date_time, incident_number, location, nature, incident_ori) VALUES (?, ?, ?, ?, ?)"
#         cur.executemany(query, incidents)
#         conn.commit()
#     except sqlite3.DatabaseError as e:
#         print(f"Failed to insert incidents: {e}")
#     finally:
#         conn.close()

# def summarize_data(db_path):
#     try:
#         conn = sqlite3.connect(db_path)
#         cur = conn.cursor()
        
#         cur.execute('''SELECT nature, COUNT(*) as count 
#                        FROM incidents 
#                        GROUP BY nature 
#                        ORDER BY count DESC, nature ASC''')
#         rows = cur.fetchall()
#         for row in rows:
#             print(f"{row[0]}|{row[1]}")  
#     except sqlite3.DatabaseError as e:
#         print(f"Failed to summarize data: {e}")
#     finally:
#         conn.close()


# def main(incidents_url, db_path="resources/normanpd.db"):
#     if download_pdf(incidents_url, "incident_report.pdf"):
#         incidents = extract_incidents("incident_report.pdf")
#         if incidents:
#             create_db(db_path)
#             insert_incidents(db_path, incidents)
#             summarize_data(db_path)
#         else:
#             print("No incidents found in the PDF.")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--incidents", type=str, required=True, help="Incident summary URL")
#     parser.add_argument("--db", type=str, help="Database path (optional)", default="resources/normanpd.db")
#     args = parser.parse_args()

#     main(args.incidents, args.db)


# import argparse
# import sqlite3
# import requests
# from pdfminer.high_level import extract_pages
# from pdfminer.layout import LTTextContainer

# def download_pdf(url, filename):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         with open(filename, 'wb') as file:
#             file.write(response.content)
#     except requests.RequestException as e:
#         print(f"Request failed: {e}")
#         return False
#     return True

# def extract_incidents(pdf_path):
#     incidents = []
#     max_columns = 0  # Track the maximum number of columns found on a page
#     for page_layout in extract_pages(pdf_path):
#         column_texts = {}  # Dictionary to hold column data
#         for element in page_layout:
#             if isinstance(element, LTTextContainer):
#                 x, y = int(element.x0), int(element.y0)  # Get the x-coordinate of the text element
#                 text = element.get_text()
#                 column = x // 100  # Group by every 100 pixels on the x-axis
#                 if column in column_texts:
#                     column_texts[column].append((y, text))  # Append text along with its y-coordinate
#                 else:
#                     column_texts[column] = [(y, text)]
        
#         # Update the maximum number of columns found on a page
#         max_columns = max(max_columns, len(column_texts))

#         # Sort texts in each column by y-coordinate (top to bottom)
#         for column, texts in column_texts.items():
#             column_texts[column] = sorted(texts, key=lambda x: -x[0])

#         # Extract data assuming a variable number of columns
#         for i in range(len(column_texts[0])):  # Use the maximum number of columns found
#             incident_data = [""] * max_columns  # Initialize with empty strings for all columns
#             for column in range(max_columns):  # Iterate through all columns
#                 if column in column_texts:
#                     try:
#                         text = column_texts[column][i][1].strip()  # Get the text for each column
                        
#                         # Handle cases for mapping data to columns
#                         if column == 3:
#                             if text == "Location" or not text:  # Handle "Location" or empty in nature column
#                                 incident_data[2] = text  # Map to location or empty
#                             else:
#                                 incident_data[3] = text  # Map to nature column
#                         elif column == 4:
#                             if not text:  # Handle empty incident_ori
#                                 incident_data[4] = "Empty"  # Or provide a default value
#                             else:
#                                 incident_data[4] = text  # Map to incident_ori column
#                         else:
#                             incident_data[column] = text  # Map to other columns
#                     except IndexError:
#                         pass  # Handle cases where a column might have fewer entries
            
#             # Swap the data in nature and incident_ori columns
#             incident_data[3], incident_data[4] = incident_data[4], incident_data[3]

#             incidents.append(incident_data[:5])  # Append only the first five columns to match the database schema

#     return incidents





# def create_db(db_path):
#     try:
#         conn = sqlite3.connect(db_path)
#         cur = conn.cursor()
#         cur.execute('''CREATE TABLE IF NOT EXISTS incidents (
#                        date_time TEXT, 
#                        incident_number TEXT, 
#                        location TEXT, 
#                        nature TEXT, 
#                        incident_ori TEXT)''')
#         conn.commit()
#     except sqlite3.DatabaseError as e:
#         print(f"Database error: {e}")
#     finally:
#         conn.close()

# def insert_incidents(db_path, incidents):
#     try:
#         conn = sqlite3.connect(db_path)
#         cur = conn.cursor()
#         query = "INSERT INTO incidents (date_time, incident_number, location, nature, incident_ori) VALUES (?, ?, ?, ?, ?)"
#         cur.executemany(query, incidents)
#         conn.commit()
#     except sqlite3.DatabaseError as e:
#         print(f"Failed to insert incidents: {e}")
#     finally:
#         conn.close()

# def summarize_data(db_path):
#     try:
#         conn = sqlite3.connect(db_path)
#         cur = conn.cursor()
#         cur.execute('''SELECT nature, COUNT(*) as count 
#                        FROM incidents 
#                        GROUP BY nature 
#                        ORDER BY count DESC, nature ASC''')
#         rows = cur.fetchall()
#         for row in rows:
#             print(f"{row[0]}|{row[1]}")
#     except sqlite3.DatabaseError as e:
#         print(f"Failed to summarize data: {e}")
#     finally:
#         conn.close()

# def main(incidents_url, db_path="resources/normanpd.db"):
#     if download_pdf(incidents_url, "incident_report.pdf"):
#         incidents = extract_incidents("incident_report.pdf")
#         if incidents:
#             create_db(db_path)
#             insert_incidents(db_path, incidents)
#             summarize_data(db_path)
#         else:
#             print("No incidents found in the PDF.")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--incidents", type=str, required=True, help="URL of the incident summary PDF")
#     parser.add_argument("--db", type=str, help="Path for the SQLite database (optional)", default="resources/normanpd.db")
#     args = parser.parse_args()

#     main(args.incidents, args.db)


import argparse
import sqlite3
import requests
from pypdf import PdfReader
import os

# from PyPDF2 import PdfReader


# Database functions
def create_db(db_path):
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

def insert_incidents(db_path, incidents):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM incidents")
    for incident in incidents:
        query = f"INSERT INTO incidents (date_time, incident_number, location, nature, incident_ori) " \
                f"VALUES ('{incident[0]}', '{incident[1]}', '{incident[2]}', '{incident[3]}', '{incident[4]}')"
        cur.execute(query)
    conn.commit()
    conn.close()

# Download function
def download_pdf(url):
    save_path="./docs/incident_report.pdf"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)

# Extract function
def extract_incidents(pdf_path):
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
    # print("\n")
    # print("The split new incidents list:")
    # print(newincidents)
    # print("\n")
    return newincidents

# Status function 
def summarize_data(db_path):
    # conn = sqlite3.connect(db_path)
    # cur = conn.cursor()
    # cur.execute('''SELECT nature, COUNT(*) as count 
    #                FROM incidents 
    #                GROUP BY nature 
    #                ORDER BY count DESC, nature''')
    # rows = cur.fetchall()
    # for row in rows:
    #     print(f"{row[0]}|{row[1]}")
    # conn.close()
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

def print_database(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM incidents")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()

# Main function
def main(url):
    # Download data
    pdf_path = "docs/incident_report.pdf"
    download_pdf(url)

    # Extract data
    incidents = extract_incidents(pdf_path)

    # Create a new database
    db_path = "resources/normanpd.db"
    create_db(db_path)

    # Insert data into the database
    insert_incidents(db_path, incidents)

    # Print incident counts
    summarize_data(db_path)

# Entry point of the script
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary url.")
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)