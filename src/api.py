from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['MONGO_DBNAME'] = 'test_phishing'
app.config['MONGO_URI'] = 'mongodb://admin:1q2w3e4r@ds239931.mlab.com:39931/test_phishing'
mongo = PyMongo(app)

@app.route('/api')
def query_example():
    log_domain = request.args.get('log_domain')
    target_domain = request.args.get('target_domain')
    cursor = mongo.db.demo1.find({'target_domain': target_domain})
    # page_score = cursor['page_score']
    # domain_score = cursor['domain_score']
    return dumps(cursor)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
