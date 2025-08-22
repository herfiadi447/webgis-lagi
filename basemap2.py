import folium

def basemaps1():
    basemaps = {
           'Google Satellite': folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='Google',
            name='Google Satellite',
            overlay=False,
            control=True,
            show=False  # Sisanya False
        ),
    }
    return basemaps
