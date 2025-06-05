import db

def main():
    # Initialize database connection
    db_connection = db.get_db_connection()

    cursor = db_connection.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS Tubes3Stima")

    print("Database Tubes3Stima created successfully")

    cursor.execute("USE Tubes3Stima")

    print("Using database Tubes3Stima")
    cursor.execute("CREATE TABLE IF NOT EXISTS ApplicantProfile (" \
                    "applicant_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY," \
                    "first_name VARCHAR(50) DEFAULT NULL," \
                    "last_name VARCHAR(50) DEFAULT NULL," \
                    "date_of_birth DATE DEFAULT NULL," \
                    "address VARCHAR(2550) DEFAULT NULL," \
                    "phone_number VARCHAR(20) DEFAULT NULL)")

    cursor.execute("CREATE TABLE IF NOT EXISTS ApplicantDetail (" \
                    "detail_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY," \
                    "applicant_id INT NOT NULL, " \
                    "applicant_role VARCHAR(100) DEFAULT NULL," \
                    "cv_path TEXT," \
                    "FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id))")
    
    print("Tables created successfully")

    # Test insert
    applicant_profle = [("Mr", "Sir", "2023-10-01", "Jl. Contoh No. 123", "08123456789"),
                        ("Ms", "Example", "1990-05-15", "Jl. Contoh No. 456", "08234567890"),
                        ("Dr", "Sample", "1985-12-20", "Jl. Contoh No. 789", "08345678901")]
    cursor.executemany(
        "INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number) VALUES (%s, %s, %s, %s, %s)",
        applicant_profle
    )

    
    db_connection.commit()

    db_connection.close()

if __name__ == "__main__":
    main()