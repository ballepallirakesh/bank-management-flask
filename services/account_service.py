from utils.db_connection import get_connection
import hashlib

def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def create_account(name, account_number, pin):
    conn = get_connection()
    cursor = conn.cursor()
    pin_hash = hash_pin(pin)

    try:
        cursor.execute("""
            INSERT INTO accounts (name, account_number, pin_hash)
            VALUES (%s, %s, %s)
        """, (name, account_number, pin_hash))
        conn.commit()
        print("✅ Account created successfully.")
    except Exception as e:
        print("❌ Error creating account:", e)
    finally:
        cursor.close()
        conn.close()

def verify_login(account_number, pin):
    conn = get_connection()
    cursor = conn.cursor()
    pin_hash = hash_pin(pin)

    cursor.execute("""
        SELECT * FROM accounts WHERE account_number=%s AND pin_hash=%s
    """, (account_number, pin_hash))

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result is not None

