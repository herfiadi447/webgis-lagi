import folium
import os
import geopandas

def peta_CH():
    d = os.path.dirname(os.path.abspath(__file__))
    geojson_path = os.path.join(d, "CH.json")
    if not os.path.exists(geojson_path):
        shp_path = geojson_path.replace('.json', '.shp')
        if os.path.exists(shp_path):
            gdf = geopandas.read_file(shp_path)
            gdf.to_file(geojson_path, driver='GeoJSON')
    m = folium.Map(location=[-4.47, 119.61], zoom_start=12)

    # Tambahkan Google Satellite
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google Satellite',
        name='Google Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    if os.path.exists(geojson_path):
        folium.GeoJson(
            geojson_path,
            name="Curah Hujan",
            style_function=lambda feature: {
                'color': 'black',
                'weight': 0.2,
                'fillOpacity': 0.5
            },
            tooltip=folium.GeoJsonTooltip(fields=['CH'])
        ).add_to(m)
    return m