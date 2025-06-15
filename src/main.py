import db
import sys
from PyQt5.QtWidgets import QApplication
from gui import JuliusCVApp

def main():
    # db.create_db()
    # print("Database created successfully.")
    app = QApplication(sys.argv)
    window = JuliusCVApp()
    window.show()
    sys.exit(app.exec_())


    
    
    

if __name__ == "__main__":
    main()