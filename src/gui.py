import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QVariant

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal, QTimer
from PyQt5.QtGui import QDesktopServices
from pdf_extractor import PDFTextExtractor, extract_pdf_to_string
from integrated_regex import IntegratedCVProcessor, CVInfo

# import mysql.connector
# Import your KMP and BM implementations
from kmp import kmp_search
from boyer_moore import boyer_moore_search
from db import get_paths
from LevenshteinDistance import fuzzy_search
        
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
            html_file_path = os.path.abspath("gui.html")
            with open(html_file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            base_url = QUrl.fromLocalFile(html_file_path)
            self.browser.setHtml(html_content, base_url)
        except FileNotFoundError:
            print("Error: gui.html not found.")


class Backend(QObject):
    def __init__(self):
        super().__init__()
        self.processor = IntegratedCVProcessor()
        
    @pyqtSlot(str, str, int, result=list)
    def searchCVs(self, keywords: str, algorithm: str, top_n: int):        
        def match(text, keyword):
            if algorithm.upper() == "KMP":
                count =  kmp_search(keyword, text)
            elif algorithm.upper() == "BM":
                count = len(boyer_moore_search(text, keyword))
            else:
                count = 0

            if count > 0:
                return count, False
            
            return fuzzy_search(text, keyword), True

        rows = get_paths()
        print(rows[0])

        results = []

        for row in rows:
            fuzzy_used = False
            applicant_id = row["applicant_id"]
            first_name = row["first_name"]
            last_name = row["last_name"]
            cv_path = row["cv_path"]
            cv_path_dotdot = "..\\" + cv_path
            print(cv_path_dotdot)
            if not os.path.isfile(cv_path_dotdot):
                print("cont")
                continue
            
            if not cv_path.split("/")[1] == "INFORMATION-TECHNOLOGY":
                continue
            with open(cv_path_dotdot, "r", encoding="utf-8", errors="ignore") as file:
                print(cv_path_dotdot)
                content = extract_pdf_to_string(cv_path_dotdot, True)

            keyword_list = [kw.strip().lower() for kw in keywords.split(",")]
            keyword_matches = []
            total_matches = 0

            for keyword in keyword_list:
                count, fuzzy = match(content, keyword)
                if fuzzy:
                    fuzzy_used = True
                if count > 0:
                    keyword_matches.append({"keyword": keyword, "count": count})
                    total_matches += count

            if total_matches > 0:
                print("Name: ", first_name, last_name)
                print("Matches: ", total_matches)
                results.append({
                    "applicant_id" : applicant_id,
                    "name": f"{first_name} {last_name}",
                    "matches": total_matches,
                    "keywords": keyword_matches,
                    "cv_path" : f"{cv_path_dotdot}",
                    "fuzzy" : fuzzy_used
                })

        sorted_results = sorted(results, key=lambda x: -x["matches"])[:top_n]
        return sorted_results
    
    @pyqtSlot(str)
    def openFile(self, path):
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))


    @pyqtSlot(str, result='QVariant')
    def getCVSummary(self, cv_path):
        try:
            cv_info = self.processor.process_pdf(cv_path)
            return {
                "name": getattr(cv_info, "name", "N/A"),
                "birthdate": getattr(cv_info, "birthdate", "-"),
                "address": getattr(cv_info, "address", "-"),
                "phone": getattr(cv_info, "phone", "-"),
                "skills": getattr(cv_info, "skills", []),
                "education": getattr(cv_info, "education", []),
                "job_history": getattr(cv_info, "job_history", [])
            }
        except Exception as e:
            return {"error": str(e)}



    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JuliusCVApp()
    window.show()
    sys.exit(app.exec_())