#! /usr/bin/env python3.6

import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse
import yaml

import pcl as pcl
import pcl.pcl_visualization as visualizer

def map2laserScan(pgmf, resolution = 0.02, origin = [0.0, 0.0, 0.0]):
	"""Return a laseerScan from pgm files."""
	
	pcd = pcl.PointCloud()
	pgmf = np.transpose(pgmf)
	array = np.where(pgmf == 0)
	zeros = np.zeros(len(array[0]))

	vertex = list(zip((origin[0] + (array[0] * resolution)), -(origin[1] + (array[1] * resolution)), zeros))
	
	pcd.from_list(vertex)

	if(args.save_flag):
		pcl.save(pcd, args.destination_name + ".pcd")
	
	if(args.view_flag):
		view = visualizer.CloudViewing()
		view.ShowMonochromeCloud(pcd, b'cloud')
		
		flag = True
		while flag:
			flag = not(view.WasStopped())

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--save", dest="save_flag", action='store_true', help="Save the pgm file")
	parser.add_argument("-m", "--map", dest="map_name", help="Map name yaml file")
	parser.add_argument("-d", "--destination", dest="destination_name", default="pointCloud", help="Destination filename without .pcd", type=str)
	parser.add_argument("-v", "--view", dest="view_flag", action='store_true', help="Visualize the PointCloud")
	
	args = parser.parse_args()

	filename = args.map_name
	with open(filename, "rb") as file:
		yaml = yaml.load(file, Loader=yaml.FullLoader)
		print(yaml.get("image"))

	with open("map/" + yaml.get("image"), "rb") as file:
		pgmf = plt.imread(file)
	

	map2laserScan(pgmf, yaml.get("resolution"), yaml.get("origin"))
