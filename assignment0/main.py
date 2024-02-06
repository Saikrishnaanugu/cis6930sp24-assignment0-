
# import argparse
# import sqlite3
# import requests
# from pypdf import PdfReader  

# def download_pdf(url, filename):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             with open(filename, 'wb') as file:
#                 file.write(response.content)
#         else:
#             print(f"Failed to download the PDF. Status code: {response.status_code}")
#             return False
#     except requests.RequestException as e:
#         print(f"Request failed: {e}")
#         return False
#     return True

# def extract_incidents(pdf_path):
#     incidents = []
#     try:
#         with open(pdf_path, 'rb') as file:
#             reader = PdfReader(file)  # Assuming PdfReader is the correct class name in pypdf
#             for page in reader.pages:  # Assuming pypdf has a similar pages iterable
#                 text = page.extract_text()  # Assuming pypdf pages have an extract_text() method
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
#         for incident in incidents:
#             query = "INSERT INTO incidents (date_time, incident_number, location, nature, incident_ori) VALUES (?, ?, ?, ?, ?)"
#             cur.execute(query, incident)
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
#                        ORDER BY count DESC, nature''')
#         rows = cur.fetchall()
#         for row in rows:
#             print(f"{row[0]}|{row[1]}")
#     except sqlite3.DatabaseError as e:
#         print(f"Failed to summarize data: {e}")
#     finally:
#         conn.close()

# def main(incidents_url, db_path):
#     if download_pdf(incidents_url, "incident_report.pdf"):
#         incidents = extract_incidents("incident_report.pdf")
#         create_db(db_path)
#         insert_incidents(db_path, incidents)
#         summarize_data(db_path)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--incidents", type=str, required=True, help="Incident summary URL")
#     parser.add_argument("--db", type=str, required=True, help="Database path")
#     args = parser.parse_args()

#     main(args.incidents, args.db)

import argparse
import sqlite3
import requests
from pypdf import PdfReader

def download_pdf(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download the PDF. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False
    return True

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

def create_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS incidents (
                       date_time TEXT, 
                       incident_number TEXT, 
                       location TEXT, 
                       nature TEXT, 
                       incident_ori TEXT)''')
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def insert_incidents(db_path, incidents):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        for incident in incidents:
            query = "INSERT INTO incidents (date_time, incident_number, location, nature, incident_ori) VALUES (?, ?, ?, ?, ?)"
            cur.execute(query, incident)
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Failed to insert incidents: {e}")
    finally:
        conn.close()

def summarize_data(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('''SELECT nature, COUNT(*) as count 
                       FROM incidents 
                       GROUP BY nature 
                       ORDER BY count DESC, nature''')
        rows = cur.fetchall()
        for row in rows:
            print(f"{row[0]}|{row[1]}")
    except sqlite3.DatabaseError as e:
        print(f"Failed to summarize data: {e}")
    finally:
        conn.close()

def main(incidents_url, db_path="normanpd.db"):  # Set a default database path
    if download_pdf(incidents_url, "incident_report.pdf"):
        incidents = extract_incidents("incident_report.pdf")
        create_db(db_path)
        insert_incidents(db_path, incidents)
        summarize_data(db_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary URL")
    parser.add_argument("--db", type=str, help="Database path (optional)", default="normanpd.db")  # Make --db optional
    args = parser.parse_args()

    main(args.incidents, args.db)
