# import the necessary packages
from flask import Flask, render_template, redirect, url_for, request,session,Response,send_file
from geopy.geocoders import Nominatim
import folium
from hereapi import *
import pandas as pd
import numpy as np
import json

geolocator = Nominatim(user_agent="traffic_control")

lat = 0
lon = 0

app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/home', methods=['GET', 'POST'])
def home():
	return redirect(url_for('input'))

@app.route('/', methods=['GET', 'POST'])
def input():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			return redirect(url_for('location'))

	return render_template('input.html', error=error)

@app.route('/location',methods=['GET', 'POST'])
def location():
	global lat
	global lon
	if request.method == 'POST':
		name = request.form['name']
		location = geolocator.geocode(name)
		result = "Lattitude = "+str(location.latitude) + ", " + "Longitude = " + str(location.longitude)
		my_map = folium.Map(location=[location.latitude,location.longitude], zoom_start=14)
		folium.Marker([location.latitude,location.longitude],popup = name).add_to(my_map)
		my_map.save("templates/map.html ")
		lat = location.latitude
		lon = location.longitude
		return render_template('location.html',result=result,address=location.address)
	return render_template('location.html')


@app.route('/map')
def map():
	return send_file('templates/map.html')

@app.route('/traffic_data',methods=['GET', 'POST'])
def traffic_data():
	global lat
	global lon
	road_names,road_jf,road_avgSpeed,road_freeSpeed = calculate_traffic(lat,lon)
	traffic_data ={
		'Road':road_names[0:4],
		'Jam Factor':road_jf[0:4],
		'Current Average Speed':road_avgSpeed[0:4],
		'Free Flow Speed':road_freeSpeed[0:4]
	}

	traffic_data1 ={
		'Jam Factor':road_jf
	}

	df = pd.DataFrame(traffic_data)
	df1 = pd.DataFrame(traffic_data1)

	if request.method == 'POST':
		df.to_csv('traffic_data.csv')
		df1.to_csv('dataset.csv')
		return redirect(url_for('traffic_control'))

	return render_template('traffic_data.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/traffic_control', methods=['GET', 'POST'])
def traffic_control():
	global lat
	global lon

	#lat = 18.4481
	#lon = 73.8585

	road_names,road_jf,road_avgSpeed,road_freeSpeed = calculate_traffic(lat,lon)

	road1 = road_names[0]
	road2 = road_names[1]
	road3 = road_names[2]
	road4 = road_names[3]

	jam1 = road_jf[0]
	jam2 = road_jf[1]
	jam3 = road_jf[2]
	jam4 = road_jf[3]

	cspeed1 = road_avgSpeed[0]
	cspeed2 = road_avgSpeed[1]
	cspeed3 = road_avgSpeed[2]
	cspeed4 = road_avgSpeed[3]

	fspeed1 = road_freeSpeed[0]
	fspeed2 = road_freeSpeed[1]
	fspeed3 = road_freeSpeed[2]
	fspeed4 = road_freeSpeed[3]

	road_jf = [float(i) for i in road_jf]

	time1 = int(float(jam1)/sum(road_jf[0:4]) * 60)
	time2 = int(float(jam2)/sum(road_jf[0:4]) * 60)
	time3 = int(float(jam3)/sum(road_jf[0:4]) * 60)
	time4 = int(float(jam4)/sum(road_jf[0:4]) * 60)

	t1 = json.dumps(int(time1))
	t2 = json.dumps(int(time2))
	t3 = json.dumps(int(time3))
	t4 = json.dumps(int(time4))



	colors = np.array(['w3-green','w3-red','w3-red','w3-yellow'])
	print(road_jf[0:4])
	idx = np.argsort(np.array(road_jf[0:4]))
	print(idx)

	colors[idx[0]] = 'w3-yellow'
	colors[idx[3]] = 'w3-green'
	colors[idx[1]] = 'w3-red'
	colors[idx[2]] = 'w3-red'
	print(colors)






	return render_template('traffic_control.html',s='w3-red',
							road1=road1,road2=road2,road3=road3,road4=road4,
							jam1=jam1,jam2=jam2,jam3=jam3,jam4=jam4,
							cspeed1=cspeed1,cspeed2=cspeed2,cspeed3=cspeed3,cspeed4=cspeed4,
							fspeed1=fspeed1,fspeed2=fspeed2,fspeed3=fspeed3,fspeed4=fspeed4,
							time1=time1,time2=time2,time3=time3,time4=time4,
							c1=colors[0],c2=colors[1],c3=colors[2],c4=colors[3],
							t1=t1,t2=t2,t3=t3,t4=t4
							)


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, threaded=True)