# -*- coding: utf-8 -*-

from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo, MongoClient
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'test_phishing'
app.config['MONGO_URI'] = 'mongodb://admin:1q2w3e4r@ds239931.mlab.com:39931/test_phishing'
mongo = PyMongo(app)
APP_URL = "http://127.0.0.1:5000"

class Data(Resource):
	def get(self):
		data = []
		cursor = mongo.db.DomainRecord.find({}, {"_id": 0, "update_time": 0}).limit(10)
		for domain_name in cursor:
			print(domain_name)
			domain_name['url'] = APP_URL + url_for('domain_names') + '/' + domain_name.get('rec_id')
			data.append(domain_name)

		return jsonify({"response": data})

	def post(self):
		data = request.get_json()
		if not data:
			data = {"response": "ERROR"}
			return jsonify(data)
		else:
			rec_id = data.get('rec_id')
			if rec_id:
				if mongo.db.DomainRecord.find_one({"rec_id": rec_id}):
					return {"response": "duplicate rec_id"}
				else:
					mongo.db.DomainRecord.insert(data)
			else:
				return {"response": ""}
		
		return redirect(url_for("domain_names"))

	def put(self, rec_id):
		data = request.get_json()
		mongo.db.DomainRecord.update({"rec_id": rec_id}, {"$set": data})
		return redirect(url_for("domain_names"))

	def delete(self, rec_id):
		mongo.db.DomainRecord.remove({"rec_id": rec_id})
		return redirect(url_for("domain_names"))

class Index(Resource):
	def get(self):
		return redirect(url_for("domain_names"))

api = Api(app)
api.add_resource(Index, "/", endpoint="index")
api.add_resource(Data, "/api", endpoint="domain_names")
api.add_resource(Data, "/api/<string:rec_id>", endpoint="rec_id")

if __name__ == "__main__":
    app.run(host='0.0.0.0')