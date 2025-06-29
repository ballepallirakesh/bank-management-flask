from utils.db_connection import get_connection

def deposit(account_number, amount):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (amount, account_number))
        cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'deposit', %s)", (account_number, amount))
        conn.commit()
        print("💰 Deposit successful.")
    except Exception as e:
        print("❌ Error during deposit:", e)
    finally:
        cursor.close()
        conn.close()

def withdraw(account_number, amount):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
        result = cursor.fetchone()
        if result and result[0] >= amount:
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_number = %s", (amount, account_number))
            cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'withdrawal', %s)", (account_number, amount))
            conn.commit()
            print("💸 Withdrawal successful.")
        else:
            print("❌ Insufficient balance.")
    except Exception as e:
        print("❌ Error during withdrawal:", e)
    finally:
        cursor.close()
        conn.close()

def get_balance(account_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0
def get_transaction_history(account_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT type, amount, date
        FROM transactions
        WHERE account_number = %s
        ORDER BY date DESC
    """, (account_number,))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results

