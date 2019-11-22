import subprocess
import os
import numpy as np
import json
import copy
class PtCloudGenerator:
	def __init__(self, opendrive_file, car_data, json_save):
		self.opendrive_file = opendrive_file
		self.road_script_file = './scripts/road_creator.py'
		self.cloud_script_file = './scripts/lidar_script.py'
		self.car_data = car_data
		self.opendrive_filename = os.path.basename(opendrive_file)
		self.add_noise = False
		self.json_save = json_save
		
	def generate_pt_clouds(self):
		self.make_blender_file()
		self.generate_data()
		add_n = 0
		if self.add_noise == True:
			add_n = 3
		scan = self.numpy_to_json()
		return scan[:,(5+add_n):(8+add_n)]


	def make_blender_file(self):
		os.chdir(os.path.dirname(os.path.realpath(__file__)))
		command = f"blender -b --python {self.road_script_file} -- {self.opendrive_file}"
		os.system(command)
		print('\n Generated 3D data')

	def generate_data(self):
		for i in range(len(self.car_data['heading'])):
			args_string = str(self.car_data['position'][i][0]) + ' ' + str(self.car_data['position'][i][1])
			command = f"blender --verbose 0 -b ./files/blend/{self.opendrive_filename[:-5]}.blend --python {self.cloud_script_file} -- {args_string} {self.car_data['heading'][i]} {self.opendrive_filename[:-5]} {i}"
			os.system(command)
			print('\n Generated Point cloud data')

	def numpy_to_json(self):
		main_dict = {}
		for i in range(len(self.car_data['heading'])):
			scan = np.loadtxt(f"./files/numpy/{self.opendrive_filename[:-5]}_{i}.numpy")
			
			
			lidar_list = []
			lidar_dict = {}
			point_cloud_array = []

			add_n = 0
			if self.add_noise == True:
				add_n = 3

			scan_white = scan[np.where((scan[:, 12:15] != np.array([0,0,0])).all(axis = 1))]

			for point in scan_white:
				point_dict = {}
				point_dict['Pos_x'] = point[5 + add_n]*10+9.5
				point_dict['Pos_y'] = point[6 + add_n]*10
				point_dict['Pos_z'] = point[7 + add_n]*10
				point_dict['ValidFlag'] = True
				point_cloud_array.append(point_dict)

			lidar_dict['Point Cloud'] = point_cloud_array 
			lidar_list.append(lidar_dict)
			vehicle_position_list = []
			vehicle_position_dict = {}
			vehicle_position_dict['Pos_x'] = self.car_data['position'][i][0]+9.5
			vehicle_position_dict['Pos_y'] = self.car_data['position'][i][1]
			vehicle_position_list.append(vehicle_position_dict)
			timestamp_dict = {}
			timestamp_dict['VehiclePosition'] = vehicle_position_list
			timestamp_dict['Lidar'] = lidar_list
			timestamp_list = []
			timestamp_list.append(timestamp_dict)
			main_dict['timestamp'] = timestamp_list

		with open(f'./files/json/{self.opendrive_filename[:-5]}.json', 'w') as f:
			json.dump(main_dict,f)
		with open(self.json_save, 'w') as f:
			json.dump(main_dict,f)

		return scan

	def return_true(self):
		return True
