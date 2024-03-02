import streamlit as st
import pyvista as pv

# Load the point cloud data from a PLY file
point_cloud = pv.read('cloud/1.ply')

# Create a Streamlit component for displaying the point cloud
@st.cache(allow_output_mutation=True)
def display_point_cloud(point_cloud):
    plotter = pv.Plotter()
    plotter.add_mesh(point_cloud, point_size=5, color="blue")
    plotter.show(auto_close=False)
    return plotter

st.write("## 3D Point Cloud Viewer")

# Display the point cloud
plotter = display_point_cloud(point_cloud)

# Add interactive controls if needed
# For example, you can add sliders to control point size or color
point_size = st.slider("Point Size", 1, 10, 5)
plotter.update_point_size(point_size)
