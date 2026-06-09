import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
from plyfile import PlyData

# 1. Setup the Webpage Layout
st.set_page_config(page_title="3D Point Cloud Viewer", layout="wide")
st.title("COLMAP Sparse Reconstruction Viewer")
st.markdown("Use your mouse to drag, rotate, and scroll to zoom in on the point cloud.")

# 2. Load the Data using plyfile (Cloud-friendly!)
@st.cache_data
def load_point_cloud(filepath):
    # Read the PLY file
    plydata = PlyData.read(filepath)
    vertex_data = plydata['vertex'].data
    
    # Extract coordinates and colors into a Pandas DataFrame
    df = pd.DataFrame({
        "x": vertex_data['x'],
        "y": vertex_data['y'],
        "z": vertex_data['z'],
        "r": vertex_data['red'],
        "g": vertex_data['green'],
        "b": vertex_data['blue']
    })
    return df

with st.spinner("Loading 3D Point Cloud..."):
    df = load_point_cloud("static/model.ply")

# ... (The rest of your PyDeck code remains exactly the same!)
# 3. Create the PyDeck Point Cloud Layer
point_cloud_layer = pdk.Layer(
    "PointCloudLayer",
    data=df,
    get_position=["x", "y", "z"],
    get_color=["r", "g", "b"],
    get_normal=[0, 0, 15],  # Adjusts lighting calculation
    point_size=3,           # Increase this if points look too small
    pickable=False,
    auto_highlight=True
)

# 4. Set the Initial Camera Viewpoint
# We center the camera directly in the middle of your point cloud
view_state = pdk.ViewState(
    target=[df["x"].mean(), df["y"].mean(), df["z"].mean()],
    zoom=8,
    pitch=45,    # Tilt angle
    bearing=0    # Rotation angle
)

# 5. Render the 3D Chart in Streamlit
st.pydeck_chart(pdk.Deck(
    layers=[point_cloud_layer], 
    initial_view_state=view_state,
    # A dark map style provides the best contrast for colorful point clouds
    map_provider=None, 
    parameters={"clearColor": [0.1, 0.1, 0.1, 1]} # Dark grey background
))