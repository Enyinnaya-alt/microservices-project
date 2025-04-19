from flask import Flask, jsonify
import psycopg2
import time  # Missing import
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Product Service Info', version='1.0')

# Database configuration
def get_db_connection():
    attempts = 0
    while attempts < 5:
        try:
            conn = psycopg2.connect(
                dbname='products_db',
                user='postgres',
                password='password',
                host='postgres',
                connect_timeout=3  # Added timeout
            )
            conn.autocommit = True  # Recommended for read-only operations
            return conn
        except psycopg2.OperationalError as e:
            print(f"Connection failed (attempt {attempts + 1}): {e}")
            time.sleep(2)
            attempts += 1
    raise Exception("Could not connect to PostgreSQL after 5 attempts")

@app.route('/products/<product_id>')
def get_product(product_id):
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:  # Context manager for cursor
            cursor.execute("SELECT id, name, price FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            
            if product:
                return jsonify({
                    'id': product[0],
                    'name': product[1],
                    'price': float(product[2])  # Ensure proper JSON serialization
                })
            return jsonify({'error': 'Product not found'}), 404
            
    except Exception as e:
        app.logger.error(f"Error fetching product: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)