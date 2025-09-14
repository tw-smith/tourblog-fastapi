import os
import re
import json
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import io
import csv

# Load environment variables from .env file for database credentials
load_dotenv()

# --- Database Configuration ---
# Make sure you have a .env file in the same directory with these variables,
# or replace the os.getenv calls with your actual credentials.
DB_NAME = "tourblog-fastapi"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"

# --- File Paths ---
SQL_DUMP_FILE = '001_toby_backup.up.sql'

def parse_all_copy_data(sql_content):
    """
    Parses an entire SQL dump file by iterating line-by-line to find all
    COPY blocks, making it robust against formatting variations.
    """
    lines = sql_content.splitlines()
    all_data = {'posts': [], 'files': [], 'files_related_morphs': []}
    
    # State machine variables
    current_table = None
    columns = []
    
    # Regex to extract table name and columns from a COPY line
    copy_header_regex = re.compile(r"COPY public\.(\w+) \((.*?)\) FROM stdin;")

    for line in lines:
        if current_table:
            # If we are currently reading data for a table
            if line.strip() == '\\.':
                # End of the data block
                current_table = None
                columns = []
            else:
                # This is a data line, parse it with the CSV reader
                data_io = io.StringIO(line)
                reader = csv.reader(data_io, dialect='excel-tab')
                for row in reader:
                    cleaned_values = [None if val == '\\N' else val for val in row]
                    all_data[current_table].append(dict(zip(columns, cleaned_values)))
        else:
            # If we are looking for the start of a new COPY block
            match = copy_header_regex.match(line)
            if match:
                table_name = match.group(1)
                if table_name in all_data:
                    current_table = table_name
                    columns = [col.strip().strip('"') for col in match.group(2).split(',')]
                    
    return all_data

def main():
    """
    Main function to connect to the DB, parse the SQL dump, and insert data.
    """
    conn = None
    try:
        print("Connecting to the database...")
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        cur = conn.cursor()
        print("Connection successful.")

        print(f"Reading and parsing SQL dump file: {SQL_DUMP_FILE}...")
        with open(SQL_DUMP_FILE, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Extract all data in one pass
        all_raw_data = parse_all_copy_data(sql_content)
        posts_raw_data = all_raw_data['posts']
        photos_raw_data = all_raw_data['files']
        relations_raw_data = all_raw_data['files_related_morphs']

        # --- Data Transformation ---
        print("Transforming extracted data...")

        #
        # --- THIS IS THE CORRECTED SECTION ---
        #

        # 1. Create sets of all valid IDs from the posts and photos data for fast lookups.
        valid_post_ids = {int(d['id']) for d in posts_raw_data}
        valid_photo_ids = {int(d['id']) for d in photos_raw_data}
        
        posts_to_insert_raw = [
            (
                int(d['id']), d.get('title'), d.get('content'), d.get('subtitle'),
                d.get('tag'), d.get('slug'), d.get('created_at'), d.get('updated_at'),
                d.get('published_at'), d.get('display_date')
            ) for d in posts_raw_data
        ]
        
        # Map of post ID to cover photo ID
        post_cover_photo_map = {
            "1": 1,
            "2": 19,
            "3": 20,
            "4": 52,
            "5": 75,
            "6": 95,
            "7": 103,
            "8": 135,
            "10": 141,
            "11": 178,
            "12": 183,
            "13": 204,
            "14": 236,
            "15": 281,
            "16": 299,
            "17": 321,
            "18": 356,
            "19": 408,
            "20": 421,
            "21": 475,
            "22": 505,
            "23": 580,
            "24": 588,
            "25": 656,
            "26": 689,
            "27": 740,
            "28": 710,
            "30": 752,
            "31": 753,
            "32": 769,
            "33": 822,
            "34": 830,
            "35": 871,
      #      "3": 37,
            "38": 939,
            "39": 961,
            "41": 1031,
            "42": 1054,
            "43": 1114,
            "44": 1175,
            "45": 1245,
            "46": 1272,
            "47": 1315,
            "48": 1369,
            "49": 1410
        }
            
        posts_to_insert = []
        for post in posts_to_insert_raw:
            post_id = post[0]
            print(post_id)
            if str(post_id) in post_cover_photo_map:
                photo_id = post_cover_photo_map[str(post_id)]
            else:
                photo_id = 0

            post_to_insert = post + (photo_id,)
            posts_to_insert.append(post_to_insert)


        photos_to_insert = [
            (
                int(d['id']), d.get('name'), d.get('alternative_text'), d.get('caption'),
                int(d['width']) if d.get('width') else None,
                int(d['height']) if d.get('height') else None,
                d.get('formats'),
                d.get('url'), d.get('created_at'), d.get('updated_at')
            ) for d in photos_raw_data
        ]

        # 2. Filter the relationships to only include ones where BOTH the post_id and photo_id are valid.
        relations_to_insert = [
            (int(d['related_id']), int(d['file_id']))
            for d in relations_raw_data
            if d.get('related_type') == 'api::post.post'
            and int(d.get('related_id')) in valid_post_ids
            and int(d.get('file_id')) in valid_photo_ids
        ]
        
        # --- End of corrected section ---

        print(f"Extraction complete. Found: {len(posts_to_insert)} posts, {len(photos_to_insert)} photos, and {len(relations_to_insert)} valid relationships.")

        # --- Data Insertion ---
        print("Inserting data into the new database...")
        if posts_to_insert:
            execute_values(cur, "INSERT INTO posts (id, title, content, subtitle, tag, slug, created_at, updated_at, published_at, display_date, cover_photo_id) VALUES %s ON CONFLICT (id) DO NOTHING", posts_to_insert)
            print(f"-> Successfully processed {len(posts_to_insert)} records for 'posts'.")
        
        if photos_to_insert:
            execute_values(cur, "INSERT INTO photos (id, name, alternative_text, caption, width, height, formats, url, created_at, updated_at) VALUES %s ON CONFLICT (id) DO NOTHING", photos_to_insert)
            print(f"-> Successfully processed {len(photos_to_insert)} records for 'photos'.")

        if relations_to_insert:
            execute_values(cur, "INSERT INTO post_photos (post_id, photo_id) VALUES %s ON CONFLICT (post_id, photo_id) DO NOTHING", relations_to_insert)
            print(f"-> Successfully processed {len(relations_to_insert)} records for 'post_photos'.")
        


        conn.commit()
        print("\nData migration completed successfully! ✅")

    except FileNotFoundError:
        print(f"Error: The file {SQL_DUMP_FILE} was not found.")
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn: conn.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()