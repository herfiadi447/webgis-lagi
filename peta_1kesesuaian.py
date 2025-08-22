import geopandas as gpd
import os

# Path saat ini (simulasi direktori script pengguna)
d = "/mnt/data"

# Daftar file GeoJSON yang akan digunakan dan field kesesuaian yang relevan
layer_files = [
    ("batuan_permukaan.json", ['S1_BP', 'S2_BP', 'S3_BP', 'N_BP']),
    ("KTK.json", ['S1_KTK', 'S2_KTK', 'S3_KTK', 'N_KTK']),
    ("C_Org.json", ['S1_COrg', 'S2_COrg', 'S3_COrg', 'N_COrg']),
    ("ph.json", ['S1_pH', 'S2_pH', 'S3_pH', 'N_pH']),
    ("tekstur.json", ['S1_Tekstur', 'S2_Tekstur', 'S3_Tekstur', 'N_Tekstur']),
    ("drainase.json", ['S1_Dr', 'S2_Dr', 'S3_Dr', 'N_Dr']),
    ("salinitas.json", ['S1_EC', 'S2_EC', 'S3_EC', 'N_EC']),
    ("kedalaman_tanah.json", ['S1_KT', 'S2_KT', 'S3_KT', 'N_KT']),
    ("kemiringan_lereng.json", ['S1_Lereng', 'S2_Lereng', 'S3_Lereng', 'N_Lereng']),
]

gabungan = None

for filename, fields in layer_files:
    path = os.path.join(d, filename)
    if not os.path.exists(path):
        continue
    gdf = gpd.read_file(path)[fields + ['geometry']]
    gdf = gdf.fillna(0).astype({f: 'int' for f in fields})
    if gabungan is None:
        gabungan = gdf
    else:
        try:
            gabungan = gpd.overlay(gabungan, gdf, how='intersection')
        except Exception as e:
            gabungan = None
            break

# Hitung kelas akhir jika overlay berhasil
if gabungan is not None:
    def hitung_kelas(row):
        total = ''.join([str(val) for val in row])
        if '1' in total[-1::4]:
            return 'N'
        elif '1' in total[2::4]:
            return 'S3'
        elif '1' in total[1::4]:
            return 'S2'
        elif '1' in total[0::4]:
            return 'S1'
        return 'Unknown'

    kelas_cols = []
    for _, fields in layer_files:
        kelas_cols.extend(fields)

    gabungan['KELAS_AKHIR'] = gabungan[kelas_cols].apply(hitung_kelas, axis=1)

    hasil_path = os.path.join(d, "kesesuaian_akhir.json")
    gabungan[['geometry', 'KELAS_AKHIR']].to_file(hasil_path, driver='GeoJSON')

hasil_path if gabungan is not None else "Gagal dalam proses overlay"
