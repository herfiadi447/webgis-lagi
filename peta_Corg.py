import folium
import geopandas as gpd
from sqlalchemy import create_engine

def peta_corg():
    engine = create_engine("postgresql://postgres:reski447@localhost:5432/herfiadidb")
    gdf = gpd.read_postgis("SELECT * FROM c_org", engine, geom_col='geom')

    if gdf.crs is None:
        gdf = gdf.set_crs(epsg=4326)
    gdf = gdf.to_crs(epsg=4326)

    # Tambahkan kolom 'kelas_corg' ke GeoDataFrame
    def tentukan_kelas(row):
        if row.get('s1_corg', 0) == 1:
            return 'S1'
        elif row.get('s2_corg', 0) == 1:
            return 'S2'
        elif row.get('s3_corg', 0) == 1:
            return 'S3'
        elif row.get('n_corg', 0) == 1:
            return 'N'
        else:
            return 'Tidak Ada'

    gdf['kelas_corg'] = gdf.apply(tentukan_kelas, axis=1)

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
        name="C Organik",
        style_function=lambda feature: {
            'color': 'black',
            'weight': 0.2,
            'fillColor': "#388e3c" if feature['properties'].get('s1_corg', 0) == 1 else
                         "#81c784" if feature['properties'].get('s2_corg', 0) == 1 else
                         "#c8e6c9" if feature['properties'].get('s3_corg', 0) == 1 else
                         "#ffffff",
            'fillOpacity': 0.5
        },
        
        popup=folium.GeoJsonPopup(
        fields=['c_organik', 'luas_ha', 'kelas_corg'],
        aliases=['c_organik', 'Luas (ha)', 'Kelas Kesesuaian'],  # opsional untuk memberi label
        localize=True)
    ).add_to(m)

    return m
