import folium
import geopandas as gpd
from sqlalchemy import create_engine

def peta_tekstur():
    engine = create_engine("postgresql://postgres:reski447@localhost:5432/herfiadidb")
    gdf = gpd.read_postgis("SELECT * FROM tekstur", engine, geom_col='geom')

    if gdf.crs is None:
        gdf = gdf.set_crs(epsg=4326)
    gdf = gdf.to_crs(epsg=4326)

    # Tambahkan kolom 'kelas_tekstur' ke GeoDataFrame
    def tentukan_kelas(row):
        if row.get('s1_tekstur', 0) == 1:
            return 'S1'
        elif row.get('s2_tekstur', 0) == 1:
            return 'S2'
        elif row.get('s3_tekstur', 0) == 1:
            return 'S3'
        elif row.get('n_tekstur', 0) == 1:
            return 'N'
        else:
            return 'Tidak Ada'

    gdf['kelas_tekstur'] = gdf.apply(tentukan_kelas, axis=1)

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
        name="Tekstur",
        style_function=lambda feature: {
            'color': 'black',
            'weight': 0.2,
            'fillColor': "#43d935" if feature['properties'].get('s1_tekstur', 0) == 1 else
                         "#99e573" if feature['properties'].get('s2_tekstur', 0) == 1 else
                         "#ffb74d" if feature['properties'].get('s3_tekstur', 0) == 1 else
                         "#ff1919" if feature['properties'].get('n_tekstur', 0) == 1 else
                         "#ffffff",
            'fillOpacity': 0.5
        },
        popup=folium.GeoJsonPopup(
        fields=['tekstur', 'luas_ha', 'kelas_tekstur'],
        aliases=['tekstur', 'Luas (ha)', 'Kelas Kesesuaian'],  # opsional untuk memberi label
        localize=True)
    ).add_to(m)

    return m
