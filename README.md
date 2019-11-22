# PointCloudGenerator

Code for our winning entry in the MBRDI CEA Virtual Drive Challenge

Uploaded here are the scripts that provide added functionality to blensor[https://www.blensor.org/]

Instructions for running:
1. The whole program can be downloaded from here[https://drive.google.com/open?id=1fRSUaQCmDz9W81wDlHitvMMrWjLA4Gzb]
2. Extract the PointCloudGenerator folder to any folder X and run the below script with the root as folder X.
3. Given below is an example script to generate the json file
```
from PointCloudGenerator.PointCloudGenerator import PtCloudGenerator

positions = [[13.375, 27.4]]
heading = [1.57079632679]
positions_shift = []
for position in positions:
	positions_shift.append([position[0]-9.5,position[1]])
car_data = {'position': positions_shift, 'heading': heading}
r = PtCloudGenerator(opendrive_file = './opendrive_files/road_specification_v3.xodr', car_data = car_data, json_save ='./output.json')
r.generate_pt_clouds()
```
4. The opendrive_file is located in "PointCloudGenerator/opendrive_files/"
5. The output is generated to "PointCloudGenerator/output.json"
6. Use the viewpointcloud.py script to visualize the point cloud data
