import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal, QTimer
# import mysql.connector
# Import your KMP and BM implementations
from kmp import kmp_search
from boyer_moore import boyer_moore
        
class JuliusCVApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JULIUSCV - Applicant Tracking System (PyQt)")
        self.setGeometry(100, 100, 1200, 800) # Ukuran jendela utama

        self.browser = QWebEngineView()
        
        self.channel = QWebChannel()
        self.backend = Backend()
        self.channel.registerObject("backend", self.backend)
        self.browser.page().setWebChannel(self.channel)

        self.load_html_content()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.browser)

    def load_html_content(self):
        try:
            with open("gui.html", "r", encoding="utf-8") as f:
                html_content = f.read()
            self.browser.setHtml(html_content, QUrl.fromLocalFile(QUrl.fromLocalFile(__file__).fileName()))
        except FileNotFoundError:
            print("Error: gui.html not found. Please create 'gui.html' with your provided HTML code.")
            self.browser.setHtml(self.get_inline_html_content())

class Backend(QObject):
    @pyqtSlot(str, str, int, result=list)
    def searchCVs(self, keywords: str, algorithm: str, top_n: int):

        def match(text, keyword):
            if algorithm.upper() == "KMP":
                return kmp_search(keyword, text)
            elif algorithm.upper() == "BM":
                # return bm_search(keyword, text)
            return 0

        # Connect to database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Tubes3Stima"
        )
        cursor = db.cursor()
        cursor.execute("""
            SELECT first_name, last_name, cv_path 
            FROM ApplicantProfile 
            JOIN ApplicantDetail 
            ON ApplicantProfile.applicant_id = ApplicantDetail.applicant_id
        """)
        rows = cursor.fetchall()

        results = []

        for first_name, last_name, cv_path in rows:
            if not os.path.isfile(cv_path):
                continue  # skip if file doesn't exist

            with open(cv_path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read().lower()

            keyword_list = [kw.strip().lower() for kw in keywords.split(",")]
            keyword_matches = []
            total_matches = 0

            for keyword in keyword_list:
                count = match(content, keyword)
                if count > 0:
                    keyword_matches.append({"keyword": keyword, "count": count})
                    total_matches += count

            if total_matches > 0:
                results.append({
                    "name": f"{first_name} {last_name}",
                    "matches": total_matches,
                    "keywords": keyword_matches
                })

        sorted_results = sorted(results, key=lambda x: -x["matches"])[:top_n]
        return sorted_results


    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JuliusCVApp()
    window.show()
    sys.exit(app.exec_())