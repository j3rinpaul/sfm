import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
from plyfile import PlyData
import os 

# 1. Setup the Webpage Layout
st.set_page_config(page_title="3D Point Cloud Viewer", layout="wide")
st.title("COLMAP Sparse Reconstruction Viewer")
st.markdown("Use your mouse to drag, rotate, and scroll to zoom in on the point cloud.")

# --- Debugging Block ---
st.write("### Debugging: What files does Streamlit see?")
st.write("Current working directory:", os.getcwd())
st.write("Files in current directory:", os.listdir())
if os.path.exists("static"):
    st.write("Files in /static folder:", os.listdir("static"))
else:
    st.write("ERROR: The 'static' folder does not exist!")
# -----------------------

@st.cache_data
def load_point_cloud(filename):
    # Dynamically find the absolute path to the folder where app.py lives
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Safely join paths regardless of Windows/Linux
    full_path = os.path.join(base_dir, filename)
    
    # Read the PLY file using the bulletproof path
    plydata = PlyData.read(full_path)
    vertex_data = plydata['vertex'].data
    
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
    # FIX: Use forward slashes and drop the "web_app" prefix!
    df = load_point_cloud("model.ply")

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