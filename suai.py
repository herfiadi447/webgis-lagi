#SUAI2
import geopandas as gpd
import os

# Daftar layer dan field kelas unik
layers_info = [
    {"filename": "batuan_permukaan.json", "fields": ['S1_BP', 'S2_BP', 'S3_BP', 'N_BP']},
    {"filename": "KTK.json", "fields": ['S1_KTK', 'S2_KTK', 'S3_KTK', 'N_KTK']},
    {"filename": "C_Org.json", "fields": ['S1_COrg', 'S2_COrg', 'S3_COrg', 'N_COrg']},
    {"filename": "ph.json", "fields": ['S1_pH', 'S2_pH', 'S3_pH', 'N_pH']},
    {"filename": "tekstur.json", "fields": ['S1_Tekstur', 'S2_Tekstur', 'S3_Tekstur', 'N_Tekstur']},
    {"filename": "drainase.json", "fields": ['S1_Dr', 'S2_Dr', 'S3_Dr', 'N_Dr']},
    {"filename": "salinitas.json", "fields": ['S1_EC', 'S2_EC', 'S3_EC', 'N_EC']},
    {"filename": "kedalaman_tanah.json", "fields": ['S1_KT', 'S2_KT', 'S3_KT', 'N_KT']},
    {"filename": "kemiringan_lereng.json", "fields": ['S1_Lereng', 'S2_Lereng', 'S3_Lereng', 'N_Lereng']},
    # Tambahkan layer lain jika ada
]

gdfs = []
for info in layers_info:
    if not os.path.exists(info["filename"]):
        print(f"File {info['filename']} tidak ditemukan, lewati.")
        continue
    gdf = gpd.read_file(info["filename"])
    # Hapus baris pertama (index 0)
    gdf = gdf.iloc[1:].reset_index(drop=True)
    # Pastikan semua kolom kelas ada, jika tidak isi 0
    for col in info["fields"]:
        if col not in gdf.columns:
            gdf[col] = 0
    gdfs.append(gdf[info["fields"] + ['geometry']])

def overlay_layers(layers):
    result = layers[0]
    for gdf in layers[1:]:
        result = gpd.overlay(result, gdf, how='intersection')
    return result

kesesuaian = overlay_layers(gdfs)

def tentukan_kelas(row):
    n_cols = [col for col in row.index if col.startswith('N_')]
    s3_cols = [col for col in row.index if col.startswith('S3_')]
    s2_cols = [col for col in row.index if col.startswith('S2_')]
    s1_cols = [col for col in row.index if col.startswith('S1_')]
    if any(row[col] == 1 for col in n_cols):
        return 'Tidak Sesuai'
    elif any(row[col] == 1 for col in s3_cols):
        return 'Sesuai Marginal'
    elif any(row[col] == 1 for col in s2_cols):
        return 'Sesuai'
    elif all(row[col] == 1 for col in s1_cols):
        return 'Sangat Sesuai'
    else:
        return 'Tidak Diketahui'

kesesuaian['kelas_kesesuaian'] = kesesuaian.apply(tentukan_kelas, axis=1)

def cari_faktor_pembatas(row):
    kolom_to_layer = {
        'BP': 'Batuan Permukaan',
        'KTK': 'KTK',
        'COrg': 'C_Org',
        'pH': 'pH',
        'Tekstur': 'Tekstur',
        'Dr': 'Drainase',
        'EC': 'Salinitas',
        'KT': 'Kedalaman Tanah',
        'Lereng': 'Kemiringan Lereng'
    }
    kelas = row['kelas_kesesuaian']
    pembatas = []
    if kelas == 'Tidak Sesuai':
        prefix = 'N_'
    elif kelas == 'Sesuai Marginal':
        prefix = 'S3_'
    elif kelas == 'Sesuai':
        prefix = 'S2_'
    else:
        return '-'
    for key in kolom_to_layer:
        col = f"{prefix}{key}"
        if col in row and row[col] == 1:
            pembatas.append(kolom_to_layer[key])
    return ', '.join(pembatas) if pembatas else '-'

kesesuaian['faktor_pembatas'] = kesesuaian.apply(cari_faktor_pembatas, axis=1)
kesesuaian[['geometry', 'kelas_kesesuaian', 'faktor_pembatas']].to_file('kesesuaian_lahan1.geojson', driver='GeoJSON')
print("Peta kesesuaian lahan berhasil dibuat: kesesuaian_lahan1.geojson")

# Dissolve agar hanya 4 baris (masing-masing kelas)
gdf = gpd.read_file('kesesuaian_lahan1.geojson')
gdf_dissolved = gdf.dissolve(by='kelas_kesesuaian', as_index=False)
gdf_dissolved.to_file('kesesuaian_lahan_dissolved1.geojson', driver='GeoJSON')
print("Peta kesesuaian lahan terkelompok (4 baris) berhasil dibuat: kesesuaian_lahan_dissolved1.geojson")