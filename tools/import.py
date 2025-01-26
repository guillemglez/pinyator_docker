import csv
import os
import uuid
from pathlib import Path

import pymysql
from dotenv import load_dotenv

load_dotenv()

# Database connection details from .env
DB_HOST = "127.0.0.1"
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE")

# CSV file path
CSV_FILE_PATH = "pinyator.csv"


# Function to insert data into the CASTELLER table
def insert_casteller(row, cursor):

    def str_to_int(str):
        return int(float(str.replace(",", ".")))

    # Mapping CSV columns to database fields
    nom = row["Nom"] if row["Nom"] else ""
    cognoms = row["Cognoms"].split(" ", 1) if row["Cognoms"] else ["", ""]
    cognom_1 = cognoms[0]
    cognom_2 = cognoms[1] if len(cognoms) > 1 else ""
    sobrenom = row["Sobrenom"] if row["Sobrenom"] else f"{nom} {cognom_1}"
    altura = str_to_int(row["Alçada (cm)"]) if row["Alçada (cm)"] else 0
    altura_troncs = altura
    forca = (
        str_to_int(row["Pes"]) if row["Pes"] else 0
    )  # Assuming weight approximates strength; customize if needed
    posicio_pinya_id = 0  # Default to NULL
    posicio_tronc_id = None  # Default to NULL
    estat = 1  # Default state for "Engrescout/Actiu" toggle
    lesionat = False  # Default to NULL
    portar_peu = 1  # Default value; toggle assumed checked
    novell = 0  # Default value; "Novell/a" toggle unchecked
    vacuna_covid = 0  # Default value; "Vacuna COVID" toggle unchecked
    codi = str(uuid.uuid4())  # Generate a unique identifier

    # SQL query for insertion
    query = """
    INSERT INTO CASTELLER (
        MalNom, Altura, Forca, POSICIO_PINYA_ID, Nom, Cognom_1, Cognom_2, Codi, Familia_ID, Estat,
        Lesionat, Portar_Peu, FAMILIA2_ID, POSICIO_TRONC_ID, NOVELL, ALTURA_TRONCS, VACUNA_COVID
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s
    )
    """

    # Data to be inserted
    data = (
        sobrenom,
        altura,
        forca,
        posicio_pinya_id,
        nom,
        cognom_1,
        cognom_2,
        codi,
        0,
        estat,
        lesionat,
        portar_peu,
        None,
        posicio_tronc_id,
        novell,
        altura_troncs,
        vacuna_covid,
    )

    try:
        cursor.execute(query, data)
    except Exception as e:
        print(row)
        raise e


# Main script
def main():
    # Connect to the database
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=3306,
        charset="utf8mb4",
    )

    csvfile = Path(CSV_FILE_PATH)
    if not csvfile.exists():
        raise FileNotFoundError(f"{csvfile.resolve()} not found")

    try:
        with connection.cursor() as cursor:
            with csvfile.open(mode="r", encoding="utf-8") as csvcontext:
                reader = csv.DictReader(csvcontext)

                for row in reader:
                    insert_casteller(row, cursor)

            # Commit the transaction
            connection.commit()

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()

    finally:
        connection.close()


if __name__ == "__main__":
    main()
