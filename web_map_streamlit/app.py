import ellipsis as el
import folium as f
import streamlit as st
from streamlit_folium import st_folium

# link and info 
folium_map = f.Map([38.851724, -77.04289], zoom_start=14)
xyz_url = 'https://api.ellipsis-drive.com/v3/path/2a9c0593-4a6b-4584-ac5d-7f76809a3536/raster/timestamp/7949023f-f33d-40bb-b0c9-5f46aa77bd31/tile/{z}/{x}/{y}?style=7d204d83-3ffa-4e64-ab38-17affe285b2d&token=epat_cekg540mBW9E09ogs3XW7gXSsZvntMdGuHTyiczNlqPcsykZG56dokkLwys2CcM9'
pathId  = "a3d9c869-790b-4ec1-8801-79734a5fc4ac"
timestampId = "8d993685-1e2d-4005-9086-44fda5812435"

# combining rasters and features together
raster_layer = f.raster_layers.TileLayer(tiles = xyz_url, attr = 'ED', max_native_zoom=17)
raster_layer.add_to(folium_map)
sh = el.path.vector.timestamp.listFeatures(pathId = pathId, timestampId = timestampId)['result']
vector_layer = f.GeoJson(sh.to_json(), name="geojson", tooltip=f.features.GeoJsonTooltip(fields=['default'], aliases=['Object:']),  style_function = lambda x: { 'fillColor': x['properties']['color'], 'color': x['properties']['color'], 'weight': 1 })
vector_layer.add_to(folium_map)

# display - st.markdown(folium_map._repr_html_(), unsafe_allow_html =True)
st_data = st_folium(folium_map, width=1280, height=720)
