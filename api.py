from flask import Flask, request, jsonify
import MySQLdb

app = Flask(__name__)

def get_db_connection():
    return MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="",
        db="inkspad"
    )

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    nama = data.get('nama')
    email = data.get('email')
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM tb_hasilcheckup WHERE nama=%s AND email=%s"
    cursor.execute(query, (nama, email))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    data = request.json
    nama = data.get('nama')
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT pdf_blob FROM tb_hasilcheckup WHERE nama=%s"
    cursor.execute(query, (nama,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return jsonify({"status": "success", "pdf_blob": result[0].decode('latin1')})
    else:
        return jsonify({"status": "fail"})

if __name__ == '__main__':
    app.run(debug=True)
