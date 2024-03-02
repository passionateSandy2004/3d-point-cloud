import cv2
import torch
import time
import numpy as np

# Q matrix 
Q = np.array(([1.0, 0.0, 0.0, -160.0],
              [0.0, 1.0, 0.0, -120.0],
              [0.0, 0.0, 0.0, 350.0],
              [0.0, 0.0, 1.0/90.0, 0.0]),dtype=np.float32)


#Load a MiDas model
model_type = "DPT_Large"     # MiDaS v3 - Large  
#model_type = "DPT_Hybrid"   # MiDaS v3 - Hybrid    
#model_type = "MiDaS_small"  # MiDaS v2.1 - Small   

midas = torch.hub.load("intel-isl/MiDaS", model_type)

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
midas.to(device)
midas.eval()
midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
    transform = midas_transforms.dpt_transform
else:
    transform = midas_transforms.small_transform

def create_output(vertices, colors, filename):
	colors = colors.reshape(-1,3)
	vertices = np.hstack([vertices.reshape(-1,3),colors])

	ply_header = '''ply
		format ascii 1.0
		element vertex %(vert_num)d
		property float x
		property float y
		property float z
		property uchar red
		property uchar green
		property uchar blue
		end_header
		'''
	with open(filename, 'w') as f:
		f.write(ply_header %dict(vert_num=len(vertices)))
		np.savetxt(f,vertices,'%f %f %f %d %d %d')

#---------------------------
def makeDepthAndCloud(read_file):
	#read_file=""
	img=cv2.imread(read_file)
	if img is None:
		print("Error: Image not loaded. Check the file path.")
		exit()
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	input_batch = transform(img).to(device)
		
	with torch.no_grad():
		prediction = midas(input_batch)

		prediction = torch.nn.functional.interpolate(
			prediction.unsqueeze(1),
			size=img.shape[:2],
			mode="bicubic",
			align_corners=False,
			).squeeze()

	depth_map = prediction.cpu().numpy()

	depth_map = cv2.normalize(depth_map, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
	points_3D = cv2.reprojectImageTo3D(depth_map, Q, handleMissingValues=False)
	#masking
	mask_map = depth_map > 0.4
	#Mask colors and points. 
	output_points = points_3D[mask_map]
	output_colors = img[mask_map]
	img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

	depth_map = (depth_map*255).astype(np.uint8)
	depth_map = cv2.applyColorMap(depth_map , cv2.COLORMAP_MAGMA)
	depth_map_uint8 = (depth_map * 255).astype(np.uint8)
	no=read_file[-5]
	depth_map_file=f"depth/{no}.png"
	# Save the depth_map as a PNG file
	cv2.imwrite(depth_map_file, depth_map_uint8)
	point_cloud_file=f"cloud/{no}.ply"
	cloud_file = point_cloud_file
	create_output(output_points, output_colors, cloud_file)
	cv2.destroyAllWindows()
