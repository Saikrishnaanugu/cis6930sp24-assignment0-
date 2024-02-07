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
import os
from pypdf import PdfReader

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
        query = "INSERT INTO incidents (date_time, incident_number, location, nature, incident_ori) VALUES (?, ?, ?, ?, ?)"
        cur.executemany(query, incidents)
    conn.commit()
    conn.close()

# Download function
def download_pdf(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        with open(filename, 'wb') as file:
            file.write(response.content)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False
    return True

# Extract function
def extract_incidents(pdf_path):
    incidents = []
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    lines = text.split('\n')
                    for line in lines:
                        data = line.split()
                        if len(data) >= 5:
                            incident_time = data[0]
                            incident_number = data[1]
                            incident_location = " ".join(data[2:-2])
                            nature = data[-2]
                            incident_ori = data[-1]
                            incidents.append((incident_time, incident_number, incident_location, nature, incident_ori))
    except Exception as e:
        print(f"Failed to extract incidents from PDF: {e}")
    return incidents

# Status function 
def summarize_data(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        cur.execute('''SELECT nature, COUNT(*) as count 
                       FROM incidents 
                       GROUP BY nature 
                       ORDER BY count DESC, nature ASC''')
        rows = cur.fetchall()
        for row in rows:
            print(f"{row[0]}|{row[1]}")  
    except sqlite3.DatabaseError as e:
        print(f"Failed to summarize data: {e}")
    finally:
        conn.close()

# Main function
def main(incidents_url, db_path="resources/normanpd.db"):
    if download_pdf(incidents_url, "incident_report.pdf"):
        incidents = extract_incidents("incident_report.pdf")
        if incidents:
            create_db(db_path)
            insert_incidents(db_path, incidents)
            summarize_data(db_path)
        else:
            print("No incidents found in the PDF.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary URL")
    parser.add_argument("--db", type=str, help="Database path (optional)", default="resources/normanpd.db")
    args = parser.parse_args()

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(args.db), exist_ok=True)

    main(args.incidents, args.db)
