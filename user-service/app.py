import psycopg2
from flask import Flask, jsonify
import os

app = Flask(__name__)
def get_db_connection():
    return psycopg2.connect(
        host="postgres", 
        database="users_db",
        user="postgres",
        password="password"
    )

# user-service/app.py
@app.route('/users/<user_id>')
def get_user(user_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if user:
            return jsonify({
                'id': user[0],
                'username': user[1],
                'email': user[2]
            })
        return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)