import open3d as o3d
import numpy as np
import cv2

# Load the individual point clouds and depth maps
point_clouds = []
depth_maps = []

for i in range(1, 8):  
    pcd = o3d.io.read_point_cloud(f'cloud/{i}.ply')
    depth_map = cv2.imread(f'depth/{i}.png', cv2.IMREAD_GRAYSCALE).astype(np.float32) / 1000.0
    point_clouds.append(pcd)
    depth_maps.append(depth_map)

# Merge point clouds using depth maps
merged_pcd = o3d.geometry.PointCloud()

for i in range(len(point_clouds)):
    pcd = point_clouds[i]
    depth_map = depth_maps[i]

    # Estimate normals for the source point cloud
    pcd.estimate_normals()

    # Create a PointCloud with color and depth information
    source_pcd = o3d.geometry.PointCloud()
    source_pcd.points = pcd.points
    source_pcd.colors = pcd.colors
    source_pcd.normals = pcd.normals

    # Transform the source point cloud based on the depth map
    transformation = o3d.pipelines.registration.TransformationEstimationPointToPlane().compute_transformation(
        source=source_pcd,
        target=merged_pcd,
        source_normals=source_pcd.normals,
        target_normals=merged_pcd.normals,
    )

    # Apply the transformation to the source point cloud
    source_pcd.transform(transformation)

    # Integrate the transformed source point cloud into the merged point cloud
    merged_pcd += source_pcd

# Visualization
o3d.visualization.draw_geometries([merged_pcd])
