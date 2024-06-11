import csv
import os
import sqlite3

from sqlalchemy import create_engine

from jobify.firebase import write_to_firebase

DBPATH = "sqlite/jobs.db"


def get_database():
    return create_engine(f"sqlite:///{DBPATH}")


def connect_to_database():
    try:
        if not os.path.exists("sqlite"):
            os.makedirs("sqlite")
        conn = sqlite3.connect(DBPATH)
        print("Database connection initialized")
    except sqlite3.Error as error:
        conn = None
        print("Error occurred: ", error)
    return conn


def query_database(conn, type, query=None, company=None):
    if conn is None:
        print("No database connection available.")
        return
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                role TEXT,
                location TEXT,
                category TEXT,
                url TEXT,
                permanency TEXT,
                qualify_for BOOLEAN,
                company TEXT
            )
        """
        )
        conn.commit()
        print("Jobs table created successfully.")
        cursor.execute(query)
        cursor.execute("SELECT * FROM jobs")

        os.makedirs("extracted", exist_ok=True)
        csv_file_path = f"extracted/{company}.csv"
        with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Role", "Location", "Category", "URL"])
            csv_writer.writerows(cursor)

        print(f"Exported data from jobs table to {company}.csv successfully.")
        if type in ("insert", "update"):
            conn.commit()

        else:
            result = cursor.fetchall()
            return result

    except Exception as error:
        if conn:
            conn.close()
            print("Database connection closed")
        raise error


def update_qualified_jobs(conn, keywords, company):
    keyword_clause = " AND ".join([f"role LIKE '%{keyword}%'" for keyword in keywords])
    main_query = f"""
            UPDATE
                jobs
            SET
                qualify_for = True
            WHERE
                {keyword_clause}
                AND company = '{company}'
            """

    if company == "special":
        exp_keywords = ("Apprenticeship", "Graduate", "Entry", "Intern", "Trainee")
        exp_keyword_clause = " OR ".join([f"experience_level LIKE '%{exp_keyword}%'" for exp_keyword in exp_keywords])

        modify_query = f"""
            {main_query}
                AND ({exp_keyword_clause})
            """
        query_database(conn=conn, type="update", query=modify_query, company=company)

    else:
        modify_query = main_query
        query_database(conn=conn, type="update", query=modify_query, company=company)
    return


def insert_jobs_to_db(job_dict, conn, company):

    columns = ", ".join(job_dict.keys())
    values = [
        f"""({', '.join(
            (f'"{str(job_dict[key][i])}"'
                for key in job_dict.keys())
            )})"""
        for i in range(len(list(job_dict.values())[0]))
    ]

    insert_query = f"""
        INSERT OR IGNORE INTO
            jobs ({columns})
        VALUES
            {', '.join(values)}
        """
    print(f"Inserting jobs to database ...")
    query_database(conn=conn, type="insert", query=insert_query, company=company)
    print("Insertion completed... 100%")
    write_to_firebase(job_dict, company)
    return
