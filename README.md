
# 🏦 Bank Management Web Application

A secure and functional **Bank Management System** built using **Python Flask** and **MySQL**, with support for user registration, login, deposits, withdrawals, balance checking, and transaction history.

---

## 🚀 Features

- 🔐 User Sign-up & Login (PIN-based with secure hashing)
- 💰 Deposit & Withdraw money
- 📊 Check current balance
- 📄 View transaction history (last 5 transactions)
- 🔁 Real-time session tracking
- ✅ Input validation and error handling
- 📦 Persistent data storage using MySQL
- ✨ Flash messages for feedback

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3 (optionally Bootstrap)
- **Backend:** Python 3, Flask
- **Database:** MySQL
- **Others:** Jinja2 Templates, Session Management, Flash Messaging

---

## 📂 Project Structure

bank-management-flask/
├── app.py # Main Flask application
├── db_connection.py # Database connection utility
├── templates/
│ ├── login.html
│ ├── signup.html
│ ├── dashboard.html
│ └── transactions.html
├── static/ # (Optional) CSS or JS files
├── requirements.txt # Python dependencies
└── README.md # Project documentation

---

## 🧪 Setup & Run Locally

### 1. Clone the Repository

git clone https://github.com/ballepallirakesh/bank-management-flask.git
cd bank-management-flask

2. Set Up Virtual Environment

python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Create the Database
In MySQL:


CREATE DATABASE bankdb;

USE bankdb;

CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    account_number VARCHAR(20) UNIQUE,
    pin_hash VARCHAR(64),
    balance DECIMAL(10, 2) DEFAULT 0.00
);

CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20),
    type ENUM('deposit','withdrawal'),
    amount DECIMAL(10,2),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

4. Run the App
python app.py
Then go to http://127.0.0.1:5000 in your browser.

 🙋‍♂️ Author
     Rakesh Ballepalli
    💼 Aspiring Python Backend Developer
    🌐 GitHub
    📫 Email: rakeshballepalli@gmail.com

