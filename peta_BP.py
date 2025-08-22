import folium
import geopandas as gpd
from sqlalchemy import create_engine

def peta_batuan():
    # Koneksi ke PostGIS
    engine = create_engine("postgresql://postgres:reski447@localhost:5432/herfiadidb")

    # Ambil data dari tabel `BP`, pastikan kolom geometry bernama 'geom'
    gdf = gpd.read_postgis("SELECT * FROM batuan_permukaan", engine, geom_col='geom')

    # Jika GeoDataFrame tidak punya CRS, set ke EPSG:4326 (atau sesuai SRID di DB)
    if gdf.crs is None:
        gdf = gdf.set_crs(epsg=4326)

    # Baru transformasi (jika diperlukan)
    gdf = gdf.to_crs(epsg=4326)

    # Tambahkan kolom 'kelas_bp' ke GeoDataFrame
    def tentukan_kelas(row):
        if row.get('s1_bp', 0) == 1:
            return 'S1'
        elif row.get('s2_bp', 0) == 1:
            return 'S2'
        elif row.get('s3_bp', 0) == 1:
            return 'S3'
        elif row.get('n_bp', 0) == 1:
            return 'N'
        else:
            return 'Tidak Ada'

    gdf['kelas_bp'] = gdf.apply(tentukan_kelas, axis=1)

    m = folium.Map(location=[-4.4031, 119.6302], zoom_start=8.5)

    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google Satellite',
        name='Google Satellite',
        overlay=False,
        control=True
    ).add_to(m)

    folium.GeoJson(
        data=gdf,
        name="Batuan Permukaan",
        style_function=lambda feature: {
            'color': 'black',
            'weight': 0.2,
            'fillColor': "#3e19d2" if feature['properties'].get('s1_bp', 0) == 1 else
                         "#6470f6" if feature['properties'].get('s2_bp', 0) == 1 else
                         "#90d9f9" if feature['properties'].get('s3_bp', 0) == 1 else
                         "#ff3c00" if feature['properties'].get('n_bp', 0) == 1 else
                         "#ffffff",
            'fillOpacity': 0.5
        },
    
        popup=folium.GeoJsonPopup(
        fields=['batuan_permukaan', 'luas_ha', 'kelas_bp'],  # tambahkan 'kelas_bp'
        aliases=['batuan_permukaan', 'Luas (ha)', 'Kelas Kesesuaian'],  # opsional untuk memberi label
        localize=True)
    ).add_to(m)

    return m
