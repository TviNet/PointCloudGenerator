import bpy
from mathutils import *
from math import *
import numpy as np
import sys

scale = 10
cam_x = float(sys.argv[sys.argv.index("--") + 1])
cam_y = float(sys.argv[sys.argv.index("--") +2])
heading = float(sys.argv[sys.argv.index("--") +3])
save_name = sys.argv[sys.argv.index("--") +4]
index = int(sys.argv[sys.argv.index("--") +5])
cam_z = 0.5
cam_dir = (1.57079632679,0,heading - 1.57079632679)

cam_x_scaled = cam_x/scale
cam_y_scaled = cam_y/scale
cam_z_scaled = cam_z/scale

# set the camera to active for performing scan
bpy.context.scene.objects.active = bpy.data.objects['Camera']
bpy.context.object.location = Vector((cam_x_scaled, cam_y_scaled, cam_z_scaled))
#output = bpy.context.object.ray_cast(bpy.context.object.location, Vector(0,0,-1))
#cam_dir = output[2]
bpy.data.objects['Camera'].rotation_euler = cam_dir

# blendodyne settings
# scan settings
bpy.data.objects['Camera'].add_scan_mesh = True
bpy.data.objects['Camera'].add_noise_scan_mesh = False
bpy.data.objects['Camera'].store_data_in_mesh = False
bpy.data.objects['Camera'].save_scan = True
bpy.data.objects['Camera'].local_coordinates = False 

# camera settigns
bpy.data.objects['Camera'].velodyne_angle_resolution = 0.0928
bpy.data.objects['Camera'].velodyne_max_dist = 200/scale
bpy.data.objects['Camera'].velodyne_start_angle = -72.5 
bpy.data.objects['Camera'].velodyne_end_angle = +72.5
bpy.data.objects['Camera'].velodyne_vstart_angle = -25 
bpy.data.objects['Camera'].velodyne_vend_angle = 15

# this requires the context to be camera
bpy.ops.blensor.scan(filepath=f'./files/numpy/{save_name}_{index}.numpy')

#scan = np.loadtxt("./files/numpy/point_cloud_data.numpy")

'''
0 timestamp 
1 yaw, 
2 pitch
3 distance,
4 distance_noise
5 x,
6 y,
7 z
8 x_noise,
9 y_noise,
10 z_noise
11 object_id
12 255*color[0]
13 255*color[1]
14 255*color[2]
15 idx
'''
#pt_cloud = scan[:,5:8]
#pt_cloud_colors = scan[:,12:15]

#print(pt_cloud.shape)

