#-*- coding: utf-8 -*-
import googlemaps,math,tsp,json
from numpy import *
from flask import Flask
app = Flask(__name__)
@app.route('/<location_list>')
def defined_route(location_list):
	args = list(location_list)
	args.pop()
	location_list = "".join(args)
	args = str(location_list).split("$")
	gmaps = googlemaps.Client(key = "AIzaSyDPhqx7w-aEmxQZyk3s2gKY9WaMZYqi1CQ")
	dict_latitude = {}
	dict_longitude = {}
	distance_dict = {}
	tsp_as_json = {}
	distance_bw2_matrix = [] 
	way_of_travel = []

	def get_distance(location_source, location_destination):	
		distance_matrix = gmaps.distance_matrix(location_source, location_destination)
		print distance_matrix
		if distance_matrix['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
			return "No results for " + distance_matrix['origin_addresses'][0] + " and " + distance_matrix['destination_addresses'][0]
		else:
			if "," in distance_matrix['rows'][0]['elements'][0]['distance']['text'].split(" ")[0]:
				temp = distance_matrix['rows'][0]['elements'][0]['distance']['text'].split(" ")[0].split(",")
				return float(temp[0]+temp[1])
			else:
				return float(distance_matrix['rows'][0]['elements'][0]['distance']['text'].split(" ")[0])

	for i in range(len(args)):
		for j in range(len(args)):
			if i==j:
				distance_bw2_matrix.append(0)
			else:
				distance_bw2_matrix.append(get_distance(args[i], args[j]))
	distance_bw2_matrix = reshape(distance_bw2_matrix,(len(args),len(args)))
	r = range(len(distance_bw2_matrix))
	dist = {(i, j): distance_bw2_matrix[i][j] for i in r for j in r}
	tsp_list = list((tsp.tsp(r, dist)))
	for x in tsp_list[1]:
		way_of_travel.append(args[x])
	tsp_as_json['distance'] = str(tsp_list[0])
	for x in range(1,len(way_of_travel)+1):
		tsp_as_json[x] = str(way_of_travel[x-1])
	return json.dumps(tsp_as_json)	