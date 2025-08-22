import folium
import geopandas as gpd
from sqlalchemy import create_engine

def peta_kesesuaian():
    engine = create_engine("postgresql://postgres:reski447@localhost:5432/herfiadidb")
    gdf = gpd.read_postgis("SELECT * FROM kesesuaian4", engine, geom_col='geom')

    if gdf.crs is None:
        gdf = gdf.set_crs(epsg=4326)
    gdf = gdf.to_crs(epsg=4326)

    warna_dict = {
        "Sangat Sesuai": "#1a9641",
        "Sesuai": "#a6d96a",
        "Sesuai Marginal": "#fdae61",
        "Tidak Sesuai": "#d7191c",
        "Tidak Diketahui": "#cccccc"
    }

    m = folium.Map(location=[-4.47, 119.61], zoom_start=9)

    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google Satellite',
        name='Google Satellite',
        overlay=False,
        control=True
    ).add_to(m)

    folium.GeoJson(
        data=gdf,
        name="Kesesuaian Lahan",
        style_function=lambda feature: {
            'color': 'black',
            'weight': 0.2,
            'fillColor': warna_dict.get(feature['properties'].get('kesesuaian_lahan', 'Tidak Diketahui'), "#cccccc"),
            'fillOpacity': 0.5
        },

        popup=folium.GeoJsonPopup(
        fields=['kesesuaian_lahan', 'faktor_pembatas', 'luas_ha'],
        aliases=['Kesesuaian Lahan', 'Faktor Pembatas', 'Luas (ha)'],
        localize=True)
    ).add_to(m)

    return m