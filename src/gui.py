import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer

class JuliusCVApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JULIUSCV - Applicant Tracking System (PyQt)")
        self.setGeometry(100, 100, 1200, 800) # Ukuran jendela utama

        self.browser = QWebEngineView()
        
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JuliusCVApp()
    window.show()
    sys.exit(app.exec_())