'''from services.account_service import create_account, verify_login
from services.transaction_service import deposit, withdraw, get_balance,get_transaction_history

def main():
    while True:
        print("\n🏦 Bank Management System")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            name = input("Enter your name: ")
            account_number = input("Enter a unique account number: ")
            pin = input("Set a 4-digit PIN: ")
            create_account(name, account_number, pin)

        elif choice == '2':
            account_number = input("Enter your account number: ")
            pin = input("Enter your PIN: ")
            if verify_login(account_number, pin):
                print("✅ Login successful.")
                while True:
                    print("\n--- Menu ---")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Transaction History")
                    print("5. Logout")

                    op = input("Enter choice: ")
                    if op == '1':
                        amt = float(input("Enter amount to deposit: "))
                        deposit(account_number, amt)
                    elif op == '2':
                        amt = float(input("Enter amount to withdraw: "))
                        withdraw(account_number, amt)
                    elif op == '3':
                        bal = get_balance(account_number)
                        print(f"💰 Current Balance: ₹{bal}")
                    elif op == '4':
                        history = get_transaction_history(account_number)
                        if not history:
                            print("📭 No transactions found.")
                        else:
                            print("\n📜 Transaction History:")
                            for tx in history:
                                print(f" - {tx[0].capitalize()} ₹{tx[1]} on {tx[2]}")

                    elif op == '5':
                        print("🔒 Logged out.")
                        break
                    else:
                        print("❌ Invalid option.")
            else:
                print("❌ Invalid login. Please check your account number or PIN.")

        elif choice == '3':
            print("👋 Thank you for using the system.")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()'''
from decimal import Decimal
import hashlib
from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils.db_connection import get_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account_number = request.form['account_number']
        pin = request.form['pin']
        pin_hash = hashlib.sha256(pin.encode()).hexdigest()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and user[3] == pin_hash:  # For now using plain PIN match (later hash)
            session['account_number'] = account_number
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid login details")
    return render_template('login.html')
'''@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        account_number = request.form['account_number']
        #pin = request.form['pin']
        pin = request.form['pin']
        pin_hash = hashlib.sha256(pin.encode()).hexdigest()


        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO accounts (name, account_number, pin_hash)
                VALUES (%s, %s, %s)
            """, (name, account_number, pin))  # (PIN hashing comes later)
            conn.commit()
            flash("✅ Account created. Please login.")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"❌ Error: {e}")
        finally:
            cursor.close()
            conn.close()
    return render_template('signup.html')'''
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        account_number = request.form['account_number']
        pin = request.form['pin']

        pin_hash = hashlib.sha256(pin.encode()).hexdigest()

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO accounts (name, account_number, pin_hash)
                VALUES (%s, %s, %s)
            """, (name, account_number, pin_hash))
            conn.commit()
            flash("✅ Account created. Please login.")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"❌ Error: {e}")
        finally:
            cursor.close()
            conn.close()
    return render_template('signup.html')
@app.route('/dashboard')
def dashboard():
    # ✅ Ensure user is logged in
    if 'account_number' not in session:
        return redirect(url_for('login'))

    account_number = session['account_number']

    conn = get_connection()
    cursor = conn.cursor()

    # ✅ Get account holder's name and balance
    cursor.execute("SELECT name, balance FROM accounts WHERE account_number = %s", (account_number,))
    user = cursor.fetchone()

    if not user:
        flash("Account not found. Please login again.")
        return redirect(url_for('login'))

    name, balance = user

    # ✅ Get last 5 transactions
    cursor.execute("""
        SELECT type, amount, date 
        FROM transactions 
        WHERE account_number = %s 
        ORDER BY date DESC 
        LIMIT 5
    """, (account_number,))
    transactions = cursor.fetchall()

    cursor.close()
    conn.close()

    # ✅ Pass data to dashboard.html
    return render_template("dashboard.html", name=name, balance=balance, transactions=transactions)
   
@app.route('/check_balance', methods=['POST'])
def check_balance():
    if 'account_number' not in session:
        return redirect(url_for('login'))

    account_number = session['account_number']

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        flash(f"💰 Current Balance: ₹{result[0]}")
    else:
        flash("❌ Could not retrieve balance.")

    return redirect(url_for('dashboard'))

@app.route('/deposit', methods=['POST'])
def deposit():
    if 'account_number' not in session:
        return redirect(url_for('login'))

    account_number = session['account_number']
    amount = Decimal(request.form['amount'])

    # ✅ Prevent negative or zero deposits
    if amount <= 0:
        flash("❌ Amount must be greater than ₹0","error")
        return redirect(url_for('dashboard'))

    conn = get_connection()
    cursor = conn.cursor()

    # Get current balance
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()
    balance = result[0] if result else 0

    new_balance = balance + amount
    cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
    cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (%s, %s, %s)",
                   (account_number, 'deposit', amount))

    conn.commit()
    cursor.close()
    conn.close()

    flash(f"✅ Deposited ₹{amount}")
    return redirect(url_for('dashboard'))
                
@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'account_number' not in session:
        return redirect(url_for('login'))

    account_number = session['account_number']
    amount = Decimal(request.form['amount'])

    # ✅ Prevent negative or zero withdrawals
    if amount <= 0:
        flash("❌ Amount must be greater than ₹0")
        return redirect(url_for('dashboard'))

    conn = get_connection()
    cursor = conn.cursor()

    # Get current balance
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()
    balance = result[0] if result else 0

    # ✅ Prevent overdraw
    if amount > balance:
        flash("❌ Insufficient balance!","error")
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))

    # Perform withdrawal
    new_balance = balance - amount
    cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
    cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (%s, %s, %s)",
                   (account_number, 'withdrawal', amount))

    conn.commit()
    cursor.close()
    conn.close()

    flash(f"✅ Withdrawn ₹{amount}")
    return redirect(url_for('dashboard'))
@app.route('/transaction_history')
def transaction_history():
    if 'account_number' not in session:
        return redirect(url_for('login'))

    account_number = session['account_number']

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT type, amount, timestamp 
        FROM transactions 
        WHERE account_number = %s 
        ORDER BY timestamp DESC
    """, (account_number,))
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('transactions.html', transactions=transactions)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('account_number', None)
    flash("👋 You have been logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
