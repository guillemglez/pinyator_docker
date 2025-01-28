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

    # Skip if empty
    if len("".join([nom, cognom_1, cognom_2])) == 0:
        return

    sobrenom = row["Sobrenom"] if row["Sobrenom"] else f"{nom} {cognom_1}"
    altura = str_to_int(row["Alçada (cm)"]) if row["Alçada (cm)"] else 0
    altura_troncs = altura
    forca = (
        str_to_int(row["Pes"]) if row["Pes"] else 0
    )  # Assuming weight approximates strength; customize if needed

    # Position mappings
    posicio_map = {
        "Baix": 9,
        "Segon": 21,
        "Quart": 19,
        "Terç": 18,
        "Dosos": 20,
        "Acotxador": 22,
        "Enxaneta": 12,
        "Crossa": 5,
        "Contrafort": 6,
        "Lateral": 4,
        "Agulla": 7,
        "Primeres": 2,
        "Dau/Vent": 3,
    }

    assert len(posicio_map.values()) == len(
        set(posicio_map.values())
    ), "posicions no úniques"

    # Determine POSICIO_PINYA_ID and POSICIO_TRONC_ID
    posicio_1 = row["Posició 1"] if "Posició 1" in row else None
    posicio_2 = row["Posició 2"] if "Posició 2" in row else None

    pinya_positions = {
        "Crossa",
        "Contrafort",
        "Lateral",
        "Agulla",
        "Primeres",
        "Dau/Vent",
    }
    tronc_positions = {
        "Baix",
        "Segon",
        "Quart",
        "Terç",
        "Dosos",
        "Acotxador",
        "Enxaneta",
    }

    posicio_pinya_id = 0
    posicio_tronc_id = None

    if posicio_1 in pinya_positions and posicio_2 in tronc_positions:
        posicio_pinya_id = posicio_map.get(posicio_1, 0)
        posicio_tronc_id = posicio_map.get(posicio_2, None)
    elif posicio_1 in tronc_positions and posicio_2 in pinya_positions:
        posicio_pinya_id = posicio_map.get(posicio_2, 0)
        posicio_tronc_id = posicio_map.get(posicio_1, None)
    else:
        # If both are of the same type or undefined, assign based on order
        posicio_pinya_id = posicio_map.get(posicio_1, 0)
        posicio_tronc_id = posicio_map.get(posicio_2, None)

    estat = (
        1 if row["BAIXA"].upper() != "TRUE" else 2
    )  # Default state for "Engrescout/Actiu" toggle
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
