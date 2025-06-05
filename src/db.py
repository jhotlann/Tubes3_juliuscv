import mysql.connector

def get_db_connection():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "julius"
    )
    return db


# cursor = db.cursor()

# cursor.execute("CREATE DATABASE IF NOT EXISTS Tubes3Stima")

# print("Database Tubes3Stima created successfully")

# cursor.execute("USE Tubes3Stima")

# cursor.execute("CREATE TABLE IF NOT EXISTS ApplicantProfile (" \
# "applicant_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY," \
# "first_name VARCHAR(50) DEFAULT NULL," \
# "last_name VARCHAR(50) DEFAULT NULL," \
# "date_of_birth DATE DEFAULT NULL," \
# "address VARCHAR(2550) DEFAULT NULL," \
# "phone_number VARCHAR(20) DEFAULT NULL)")

# cursor.execute("CREATE TABLE IF NOT EXISTS ApplicantDetail (" \
# "detail_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY," \
# "applicant_id INT NOT NULL, " \
# "applicant_role VARCHAR(100) DEFAULT NULL," \
# "cv_path TEXT," \
# "FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id))")