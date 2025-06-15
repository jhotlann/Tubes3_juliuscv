<!-- Back to Top Link-->
<a name="readme-top"></a>

<br />
<div align="center">
  <h1 align="center">Tugas Besar 3 IF2211 Strategi Algoritma 2024/2025</h1>

  <p align="center">
    <h3>JULIUSCV - Applicant Tracking System</h3>
    <h4>CV Matching using String Pattern Algorithms</h4>
  </p>
</div>

<!-- CONTRIBUTOR -->
<div align="center" id="contributor">
  <strong>
    <h3>Made by:</h3>
    <table align="center">
       <tr>
        <td>13523025</td>
        <td>Joel Hotlan Haris Siahaan</td>
      </tr>
      <tr>
        <td>13523030</td>
        <td>Julius Arthur</td>
      </tr>
      <tr>
        <td>13622076</td>
        <td>Ziyan Agil Nur Ramadhan</td>
      </tr>
    </table>
  </strong>
  <br>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

JULIUSCV adalah aplikasi pelacak pelamar berbasis GUI PyQt. Aplikasi ini dapat mencari CV berdasarkan kata kunci menggunakan algoritma pencocokan string: **KMP**, **Boyer-Moore**, dan fallback ke **Levenshtein Distance**.  
CV dapat dicari berdasarkan keyword, dilihat detailnya, dan diurutkan berdasarkan relevansi hasil pencarian.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ALGORITHMS -->
## Algorithms

### 🔸 KMP (Knuth-Morris-Pratt)
Mencari pola dalam teks dengan menghindari pencocokan ulang karakter. Memanfaatkan prefix table (`lps` array) untuk pergeseran efisien.

### 🔸 Boyer-Moore (BM)
Mencari pola dari kanan ke kiri dan melakukan lompatan berdasarkan kemunculan terakhir karakter dalam pola.

### 🔸 Levenshtein Distance (Fuzzy Search)
Menghitung jumlah minimum operasi edit (insert, delete, replace) untuk mengubah satu string ke string lain. Digunakan sebagai backup saat KMP dan BM tidak menemukan hasil.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

- Python 3.9+
- MySQL Server (aktif dan berjalan)
- Pip

### Installation

1. Clone repositori:
   ```bash
   git clone https://github.com/jhotlann/Tubes3_juliuscv.git
   ```
2. Buat virtual environtment
   ```bash
   python -m venv venv
   ```
4. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
5. Buat file .env
   ```bash
   DB_HOST=localhost
   DB_USER= your_username
   DB_PASSWORD= your_password
   DB_NAME=Tubes3Stima
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<h3 align="center">THANK YOU!</h3> <!-- MARKDOWN LINKS & IMAGES -->
