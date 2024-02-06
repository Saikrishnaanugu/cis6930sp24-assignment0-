import argparse
import sqlite3
from pypdf import PdfReader
import requests


def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)


def extract_incidents(pdf_path):
    incidents = []
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
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
    return incidents


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
    for incident in incidents:
        query = f"INSERT INTO incidents (date_time, incident_number, location, nature, incident_ori) " \
                f"VALUES (?, ?, ?, ?, ?)"
        cur.execute(query, incident)
    conn.commit()
    conn.close()


def summarize_data(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''SELECT nature, COUNT(*) as count 
                   FROM incidents 
                   GROUP BY nature 
                   ORDER BY count DESC, nature''')
    rows = cur.fetchall()
    for row in rows:
        print(f"{row[0]}|{row[1]}")
    conn.close()
def main(url, db_path):
    # Download PDF
    pdf_path = "incident_report.pdf"
    download_pdf(url, pdf_path)

    # Extract incidents from the PDF
    incidents = extract_incidents(pdf_path)

    # Create the database
    create_db(db_path)

    # Insert incidents into the database
    insert_incidents(db_path, incidents)

    # Print incident counts
    summarize_data(db_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True, help="Incident summary URL")
    parser.add_argument("--db", type=str, required=True, help="Database path")
    args = parser.parse_args()

    main(args.url, args.db)