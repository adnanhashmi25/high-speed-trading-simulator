# High-Speed Trading Simulator  

🚀 **Overview:**  
This project is a **trading simulator** that tests a **momentum & mean reversion strategy** based on weekly stock price changes.  
- **Buy:** If a stock drops **5% or more** in a week, it's considered undervalued.  
- **Short:** If a stock rises **10% or more** in a week, it's considered overvalued.  
- **Track Performance:** All trades are **logged** in a database and displayed on an **Excel dashboard**.  

🔒 **Note:**  
- **This is a simulator.** No real money is involved.  
- **Stock data is retrieved via an API (Yahoo Finance).**  
- **Users can modify thresholds** to test different trading strategies.  

---

## 📌 Installation & Setup  

### 1️⃣ Prerequisites  
Ensure you have the following installed:  
- **Python 3.11**  
- **MySQL or PostgreSQL** (for trade logging)  
- **Pandas, yfinance, SQLAlchemy** (Install below)  

### 2️⃣ Clone the Repository  
git clone https://github.com/adnanhashmi25/high-speed-trading-simulator.git
cd high-speed-trading-simulator

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Set Up Database
Modify config/database_config.py to match your database credentials.

### 5️⃣ Run the Simulator
python main.py

### 📈 Features
✔ Stock market simulator using real-time data
✔ Momentum & mean reversion strategy testing
✔ Tracks all trades in a structured database
✔ Excel dashboard for performance analysis
✔ Adjustable thresholds for strategy testing

### 📜 Detailed Documentation
For a full project breakdown, visit the docs folder.
- Project Summary
