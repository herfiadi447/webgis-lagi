import folium
import geopandas as gpd
from sqlalchemy import create_engine

def peta_ph():
    # Koneksi ke PostGIS
    engine = create_engine("postgresql://postgres:reski447@localhost:5432/herfiadidb")

    # Ambil data dari tabel `ph`, pastikan kolom geometry bernama 'geom'
    gdf = gpd.read_postgis("SELECT * FROM ph", engine, geom_col='geom')

    # Jika GeoDataFrame tidak punya CRS, set ke EPSG:4326 (atau sesuai SRID di DB)
    if gdf.crs is None:
        gdf = gdf.set_crs(epsg=4326)

    # Baru transformasi (jika diperlukan)
    gdf = gdf.to_crs(epsg=4326)

    # Tambahkan kolom 'kelas_ph' ke GeoDataFrame
    def tentukan_kelas(row):
        if row.get('s1_ph', 0) == 1:
            return 'S1'
        elif row.get('s2_ph', 0) == 1:
            return 'S2'
        elif row.get('s3_ph', 0) == 1:
            return 'S3'
        elif row.get('n_ph', 0) == 1:
            return 'N'
        else:
            return 'Tidak Ada'

    gdf['kelas_ph'] = gdf.apply(tentukan_kelas, axis=1)

    # Inisialisasi peta
    m = folium.Map(location=[-4.4031, 119.6302], zoom_start=8.5)

    # Tambahkan Google Satellite
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google Satellite',
        name='Google Satellite',
        overlay=False,
        control=True
    ).add_to(m)

    # Tambahkan layer pH dari database
    folium.GeoJson(
        data=gdf,
        name="pH",
        style_function=lambda feature: {
            'color': 'black',
            'weight': 0.2,
            'fillColor': (
                "#7b1fa2" if feature['properties'].get('s1_ph', 0) == 1 else
                "#af55be" if feature['properties'].get('s2_ph', 0) == 1 else
                "#d593df" if feature['properties'].get('s3_ph', 0) == 1 else
                "#ffffff"
            ),
            'fillOpacity': 0.5
        },
        popup=folium.GeoJsonPopup(
            fields=['ph', 'luas_ha', 'kelas_ph'],   # tambahkan 'kelas_ph'
            aliases=['pH', 'Luas (ha)', 'Kelas Kesesuaian'],  # label popup
            localize=True)
    ).add_to(m)

    return m
