# peta.py

import folium
import os
import geopandas

def tambah_layer_geojson(map_obj, geojson_path, nama_layer, tooltip_fields, warna_layer=None):
    def style_function(feature):
        props = feature['properties']
        # Default warna untuk tiap kelas
        warna_s1 = '#1a9641'
        warna_s2 = '#a6d96a'
        warna_s3 = '#fdae61'
        warna_n  = "#fcfcfcff"
        # Batuan Permukaann
        if warna_layer == 'blue':
            warna_s1 = "#3e19d2"
            warna_s2 = "#6470f6"
            warna_s3 = "#90d9f9"
            warna_n  = "#ff3c00"
        # KTK 2
        elif warna_layer == 'red':
            warna_s1 = "#d93535"
            warna_s2 = "#e57373"
            warna_s3 = '#ffb74d'
            warna_n  = "#616161"
        # C Organik
        elif warna_layer == 'green':
            warna_s1 = "#388e3c"
            warna_s2 = "#81c784"
            warna_s3 = "#c8e6c9"
        # pH Tanah
        elif warna_layer == 'purple':
            warna_s1 = "#7b1fa2"
            warna_s2 = "#ba68c8"
            warna_s3 = "#e1bee7"
        # Tekstur
        elif warna_layer == 'orange':
            warna_s1 = "#f57c00"
            warna_s3 = "#ffe0b2"
            warna_n  = "#ff1919"
        # Drainase
        elif warna_layer == 'blue':
            warna_s1 = "#00f5dd"
            warna_s3 = "#6ea7a6"
            warna_n  = "#ff1919"
        # salinitas
        elif warna_layer == 'orange':
            warna_s1 = "#f57c00"
        # kedalaman tanah
        elif warna_layer == 'brown':
            warna_s1 = "#886255"   # coklat tua
            warna_s2 = "#a1887f"   # coklat muda
            warna_s3 = "#d7ccc8"   # coklat pastel
            warna_n  = "#2d1b18"   # coklat gelap
        # kemiringan lereng
        elif warna_layer == 'orange':
            warna_s1 = "#f1d442" 
            warna_s2 = "#fff176"   # kuning muda
            warna_s3 = "#f7e51d"   # kuning pastel
            warna_n  = "#f1cd72" 
           
        # Tambahkan else untuk warna lain jika perlu

        # Penentuan field S1/S2/S3/N sesuai layer
        if 'BP' in tooltip_fields[1]:
            s1, s2, s3, n = 'S1_BP', 'S2_BP', 'S3_BP', 'N_BP'
        elif 'KTK' in tooltip_fields[1]:
            s1, s2, s3, n = 'S1_KTK', 'S2_KTK', 'S3_KTK', 'N_KTK'
        elif 'COrg' in tooltip_fields[1]:
            s1, s2, s3, n = 'S1_COrg', 'S2_COrg', 'S3_COrg', 'N_COrg'
        elif 'pH' in tooltip_fields[1]:
            s1, s2, s3, n = 'S1_pH', 'S2_pH', 'S3_pH', 'N_pH'
        elif 'Tekstur' in tooltip_fields[1]:
            s1, s2, s3, n = 'S1_Tekstur', 'S2_Tekstur', 'S3_Tekstur', 'N_Tekstur'
        elif 'Dr' in tooltip_fields[1]:
            s1, s2, s3, n = 'S1_Dr', 'S2_Dr', 'S3_Dr', 'N_Dr'
        elif 'EC' in tooltip_fields[1]:
            s1, s2, s3, n = 'S1_EC', 'S2_EC', 'S3_EC', 'N_EC'   
        elif 'KT' in tooltip_fields[1]:
            s1, s2, s3, n = 'S1_KT', 'S2_KT', 'S3_KT', 'N_KT' 
        elif 'Lereng' in tooltip_fields[1]:
            s1, s2, s3, n = 'S1_Lereng', 'S2_Lereng', 'S3_Lereng', 'N_Lereng'  
        else:
            s1 = s2 = s3 = n = None

        if s1 and props.get(s1, 0) == 1:
            fillColor = warna_s1
        elif s2 and props.get(s2, 0) == 1:
            fillColor = warna_s2
        elif s3 and props.get(s3, 0) == 1:
            fillColor = warna_s3
        elif n and props.get(n, 0) == 1:
            fillColor = warna_n
        else:
            fillColor = "#ffffff"
        return {
            'color': 'black',
            'weight': 0.2,
            'fillColor': fillColor,
            'fillOpacity': 0.5
        }

    fg = folium.FeatureGroup(name=nama_layer)
    fg.add_child(folium.GeoJson(
        geojson_path,
        name=nama_layer,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=tooltip_fields)
    ))
    map_obj.add_child(fg)

def peta_multi_layer(map_obj):
    d = os.path.dirname(os.path.abspath(__file__))
    layers = [
        {
            "filename": "batuan_permukaan.json",
            "nama": "Batuan Permukaan",
            "warna": "blue",
            "fields": ['BATUAN_NIL', 'S1_BP', 'S2_BP', 'S3_BP', 'N_BP']
        },
        {
            "filename": "KTK.json",
            "nama": "KTK 2",
            "warna": "red",
            "fields": ['KTK_NILAI', 'S1_KTK', 'S2_KTK', 'S3_KTK', 'N_KTK']
        },
        {
            "filename": "C_Org.json",
            "nama": "C Organik",
            "warna": "green",
            "fields": ['CORG_NILAI', 'S1_COrg', 'S2_COrg', 'S3_COrg', 'N_COrg']
        },
        {
            "filename": "ph.json",
            "nama": "pH",
            "warna": "purple",
            "fields": ['PH_NILAI', 'S1_pH', 'S2_pH', 'S3_pH', 'N_pH']
        },
        {
            "filename": "tekstur.json",
            "nama": "Tesktur",
            "warna": "orange",
            "fields": ['KTG_TXTR', 'S1_Tekstur', 'S2_Tekstur', 'S3_Tekstur', 'N_Tekstur']
        },
        {
            "filename": "drainase.json",
            "nama": "Drainase",
            "warna": "blue",
            "fields": ['DRAINASE', 'S1_Dr', 'S2_Dr', 'S3_Dr', 'N_Dr']
        },
        {
            "filename": "salinitas.json",
            "nama": "Salinitas",
            "warna": "orange",
            "fields": ['EC_NILAI', 'S1_EC', 'S2_EC', 'S3_EC', 'N_EC']
        },
        {
            "filename": "kedalaman_tanah.json",
            "nama": "Kedalaman Tanah",
            "warna": "brown",
            "fields": ['DALAM_TNH', 'S1_KT', 'S2_KT', 'S3_KT', 'N_KT']
        },
        {
            "filename": "kemiringan_lereng.json",
            "nama": "Kemiringan Lereng",
            "warna": "orange",
            "fields": ['KL', 'S1_Lereng', 'S2_Lereng', 'S3_Lereng', 'N_Lereng']
        },
        # Tambahkan layer lain sesuai kebutuhan
    ]
    for layer in layers:
        geojson_path = os.path.join(d, layer["filename"])
        if not os.path.exists(geojson_path):
            shp_path = geojson_path.replace('.json', '.shp')
            if os.path.exists(shp_path):
                gdf = geopandas.read_file(shp_path)
                gdf.to_file(geojson_path, driver='GeoJSON')
        if os.path.exists(geojson_path):
            tambah_layer_geojson(map_obj, geojson_path, layer["nama"], layer["fields"], layer["warna"])
