from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

em = {}
go = False
doctors = {}
doctor0 = {
	'id': '342d',
	'name': 'Mister Doctor',
	'skills': 2,
	'lat': 43.6685586,
	'lng': -79.3979803
}
doctor1 = {
	'id': '168a',
	'name': 'Doctor Doom',
	'skills': 1,
	'lat': 43.6694453,
	'lng': -79.3954161
}
doctors[0] = doctor0
doctors[1] = doctor1
candidate = -1
accepted = False
potential_doctors = {}

@app.route('/', methods = ['POST'])
def root():
	return 'Doctors Within Borders'

@app.route('/emergency/start', methods = ['POST'])
def startEmergency():
	global go
	global em
	data = request.data.decode('utf-8')
	store = json.loads(data)
	go = True
	em['em'] = go
	em['name'] = store['Name']
	em['sex'] = store['Sex']
	em['age'] = store['Age']
	em['skills'] = store['Skills']
	em['lat'] = store['Lat']
	em['lng'] = store['Lng']
	em['symptoms'] = store['Symptoms']
	if em['lat'] == None or em['lng'] == None:
		return "Need to provide latitude and longitude!"
	else:
		return jsonify(doctors)

@app.route('/polling', methods = ['POST'])
def poll():
	global em
	global go
	global doctors
	global accepted
	global potential_doctors
	data = request.data.decode('utf-8')
	info = json.loads(data)
	for i in range(len(doctors)):
		if doctors[i]['id'] == info['id']:
			doctors[i]['lat'] = info['lat']
			doctors[i]['lng'] = info['lng']
		if (go and not accepted and candidate >= 0
			and potential_doctors[candidate]['id'] == info['id']):
			return jsonify({
				'em': True,
				'dist': potential_doctors[candidate]['dist']
			})
		else:
			return jsonify({
				'em': False
			})

@app.route('/closest', methods = ['POST'])
def closest():
	global candidate
	global accepted
	global potential_doctors
	data = request.data.decode('utf-8')
	potential_doctors = json.loads(data)
	accepted = False
	candidate = 0
	return "true"

@app.route('/polling/accept', methods = ['POST'])
def reply():
	global candidate
	global em
	global doctors
	data = request.data.decode('utf-8')
	info = json.loads(data)
	accepted = info['go']
	if not accepted:
		candidate = (candidate + 1) % len(doctors)
		while potential_doctors[candidate]['skills'] < em['Skills']:
			candidate = (candidate + 1) % len(doctors)
		return jsonify({
			'null': 0
		})
	else:
		return jsonify(em)
