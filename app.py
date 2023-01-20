from flask import Flask, jsonify, request, make_response
import psycopg2

app = Flask(__name__)
app.config["DEBUG"] = True

# For connect psql to this project
conn = psycopg2.connect("postgresql://postgres:alam@localhost:5432/jabarprov")
token = "private"


# To check psql connected
@app.route('/', methods=['GET'])
def index():
    conn = psycopg2.connect("postgresql://postgres:alam@localhost:5432/jabarprov")
    return "it works!"

@app.route('/public/data_warga')
def get_data_warga():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT sum(jumlah_penduduk) FROM data_warga WHERE jenis_kelamin='LAKI-LAKI'")
            laki_laki = cursor.fetchone()[0]
            cursor.execute("SELECT sum(jumlah_penduduk) FROM data_warga WHERE jenis_kelamin='PEREMPUAN'")
            perempuan = cursor.fetchone()[0]
            cursor.execute("SELECT sum(jumlah_penduduk) FROM data_warga")
            total = cursor.fetchone()[0]
            return {"data": {"LAKI-LAKI" : laki_laki, "PEREMPUAN":perempuan, "TOTAL":total}}


@app.route('/private/data_warga_kota')
def get_private_data_warga():
    if request.headers["Authorization"] == token:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT nama_kabupaten_kota, sum(jumlah_penduduk) FROM data_warga GROUP BY nama_kabupaten_kota")
                penduduk = cursor.fetchall()
                cursor.execute("SELECT sum(jumlah_penduduk) FROM data_warga")
                total = cursor.fetchone()[0]
                return jsonify({'data': {k: v for k, v in penduduk}})
    else:
        return {"message": "token is not valid"}

@app.route('/private/data_warga_tahun')
def get_private_data_warga2():
    if request.headers["Authorization"] == token:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT tahun, sum(jumlah_penduduk) FROM data_warga WHERE tahun BETWEEN '2018' AND '2022' GROUP BY tahun")
                penduduk = cursor.fetchall()
                cursor.execute("SELECT sum(jumlah_penduduk) FROM data_warga WHERE tahun BETWEEN '2018' AND '2022'")
                total = cursor.fetchone()[0]
                return jsonify({'data': {k: v for k, v in penduduk}})
    else:
        return {"message": "token is not valid"}

app.run()