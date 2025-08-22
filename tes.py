import folium

m = folium.Map(location=[-5.14, 119.47], zoom_start=13)

html = """
<div style="width: 200px;">
  <h4>Judul Popover</h4>
  <p>Ini adalah isi popover yang bisa berisi <b>HTML</b> atau info detail.</p>
</div>
"""

popup = folium.Popup(html, max_width=250)

folium.Marker(
    location=[-5.14, 119.47],
    popup=popup,
    tooltip="Klik untuk info lengkap"
).add_to(m)

m.save("map.html")
