from flask import Flask, render_template
from flask import request, redirect, url_for, flash
import os, zipfile, shutil
import geopandas as gpd
import folium
from basemap2 import basemaps1
from peta_BP import peta_batuan
from peta_ktk import peta_ktk
from peta_Corg import peta_corg
from peta_ph import peta_ph
from peta_tektstur import peta_tekstur
from peta_drainase import peta_drainase
from peta_salinitas import peta_salinitas
from peta_KT import peta_KedalamanTanah
from peta_lereng import peta_lereng
from kesesuaian_lahan import peta_kesesuaian
from flask import request, jsonify
import requests
import psycopg2

app = Flask(__name__)
app.secret_key = 'geoai-secret-key-2025'  # Ganti dengan string acak untuk produksi
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['EXTRACT_FOLDER'] = 'static/extracted'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXTRACT_FOLDER'], exist_ok=True)



@app.route('/')
def index():
    # Peta untuk dashboard (bisa multi-layer atau ringkasan)
    dashboard_map = folium.Map(location=[-4.47, 119.61], zoom_start=12, control_scale=True)
    basemaps1()
    # ...tambahkan layer jika perlu...
    dashboard_map_html = dashboard_map._repr_html_()
    return render_template('index.html', dashboard_map_html=dashboard_map_html)


# Endpoint untuk setiap peta layer (dipanggil via iframe)
@app.route('/peta_BP.py')
def show_peta_batuan():
    m = peta_batuan()
    return m._repr_html_()

@app.route('/peta_ktk.py')
def show_peta_ktk():
    m = peta_ktk()
    return m._repr_html_()

@app.route('/peta_Corg.py')
def show_peta_corg():
    m = peta_corg()
    return m._repr_html_()

@app.route('/peta_ph.py')
def show_peta_ph():
    m = peta_ph()
    return m._repr_html_()

@app.route('/peta_tektstur.py')
def show_peta_tekstur():
    m = peta_tekstur()
    return m._repr_html_()

@app.route('/peta_drainase.py')
def show_peta_drainase():
    m = peta_drainase()
    return m._repr_html_()

@app.route('/peta_salinitas.py')
def show_peta_salinitas():
    m = peta_salinitas()
    return m._repr_html_()

@app.route('/peta_KT.py')
def show_peta_kedalaman():
    m = peta_KedalamanTanah()
    return m._repr_html_()

@app.route('/peta_lereng.py')
def show_peta_lereng():
    m = peta_lereng()
    return m._repr_html_()

@app.route('/kesesuaian_lahan.py')
def show_peta_kesesuaian():    
    m = peta_kesesuaian()
    return m._repr_html_()


@app.route('/upload_layer', methods=['POST'])
def upload_layer():
    layer_name = request.form.get('layer_name')
    file = request.files.get('layer_file')
    if not file or not layer_name:
        flash('Nama layer dan file wajib diisi!')
        return redirect(url_for('index'))

    filename = file.filename
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    # Ekstrak jika zip
    extract_path = os.path.join(app.config['EXTRACT_FOLDER'], os.path.splitext(filename)[0])
    if filename.lower().endswith('.zip'):
        with zipfile.ZipFile(save_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        # Cari file .shp
        shp_file = None
        for f in os.listdir(extract_path):
            if f.endswith('.shp'):
                shp_file = os.path.join(extract_path, f)
                break
        if not shp_file:
            flash('File SHP tidak ditemukan dalam ZIP!')
            shutil.rmtree(extract_path, ignore_errors=True)
            os.remove(save_path)
            return redirect(url_for('index'))
        gdf = gpd.read_file(shp_file)
    elif filename.lower().endswith('.geojson'):
        gdf = gpd.read_file(save_path)
    else:
        flash('Format file tidak didukung!')
        os.remove(save_path)
        return redirect(url_for('index'))

    # Simpan ke GeoJSON hasil ekstrak
    geojson_name = layer_name.replace(' ', '_') + '.geojson'
    geojson_path = os.path.join('static/geojson', geojson_name)
    os.makedirs('static/geojson', exist_ok=True)
    gdf.to_file(geojson_path, driver='GeoJSON')

    # TODO: Simpan metadata ke database jika perlu

    flash(f'Layer "{layer_name}" berhasil diupload!')
    return redirect(url_for('index'))


@app.route('/kelas_lahan_chart')
def kelas_lahan_chart():
    # Koneksi ke database
    conn = psycopg2.connect(
        dbname='herfiadidb',
        user='postgres',
        password='reski447',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()
    # Hitung jumlah masing-masing kelas
    cur.execute("""
        SELECT kesesuaian_lahan, COUNT(*) 
        FROM  kesesuaian4
        GROUP BY kesesuaian_lahan
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Mapping agar urutan warna konsisten
    kelas_order = ['Sangat Sesuai', 'Sesuai', 'Sesuai Marginal', 'Tidak Sesuai']
    kelas_dict = {k: 0 for k in kelas_order}
    for k, v in rows:
        kelas_dict[k] = v

    return jsonify({
        "labels": kelas_order,
        "values": [kelas_dict[k] for k in kelas_order]
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

