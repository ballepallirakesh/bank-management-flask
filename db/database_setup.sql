CREATE DATABASE IF NOT EXISTS bank_db;
USE bank_db;

CREATE TABLE IF NOT EXISTS accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    pin_hash VARCHAR(255) NOT NULL,
    balance DECIMAL(10, 2) DEFAULT 0.00
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20) NOT NULL,
    type ENUM('deposit', 'withdrawal') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
