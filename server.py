
import flask
import io
import pickle
from flask_cors import CORS

import numpy as np
import tensorflow as tf

from keras.models import load_model


# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
CORS(app)
model = None
graph = None
drugs = None
targets = None
ts = None
ds = None

def init():
	global model, graph, drugs, targets, ts, ds
	model = load_model('DenseModel_v1.h5')
	graph = tf.get_default_graph()
	drugs = pickle.load(open('EmbedDict_drug.pkl', 'rb'))
	targets= pickle.load(open('EmbedDict_target.pkl', 'rb'))
	ds = np.array(list(drugs.values()))
	ts = np.array(list(targets.values()))

def prepare_data(d, drugFlag):
	global drugs, targets, ts, ds
	if drugFlag == True:
		print(ts.shape)
		temp = drugs[d]
		return np.hstack((ts, np.tile(temp,(ts.shape[0],1))))
	else:
		temp = targets[d]
		return np.hstack((np.tile(temp,(ds.shape[0],1)), ds))

def model_predictions(dataset, x, names, data):
	data["requestID"] = x
	with graph.as_default():
		y_preds = model.predict(dataset)
	results = [1 if y[0]>=0.5 else 0 for y in y_preds]
	predictions = [[names[i], results[i], y_preds[i][0]] for i in range(0, len(y_preds))]
	predictions = sorted(predictions, key=lambda x: x[2], reverse=True)
	data["predictions"] = []
	for val in predictions:
		r = {"label": val[0], "result": val[1], "probability" : float(val[2])}
		data["predictions"].append(r)
	return data

@app.route("/vishesh", methods=["GET"])
def vishesh():
	response =flask.jsonify({"hello" : 123})
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response


@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	global drugs, targets
	data = {"success": False}


	# print(flask.request.form)
	# print(flask.request.json)

	if flask.request.method == "POST":
		if flask.request.json.get("drug"):
			drug = flask.request.json["drug"]
			# print(drug)
			dataset = prepare_data(drug, True)
			# print(dataset.shape)
			data = model_predictions(dataset, drug, list(targets.keys()), data)

		elif flask.request.json.get("target"):
			# read the image in PIL format
			target = flask.request.json["target"]
			# print(target)
			dataset= prepare_data(target, False)
			data = model_predictions(dataset, target, list(drugs.keys()), data)
		data["success"] = True

	response = flask.jsonify(data)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	init()
	app.run(host='0.0.0.0', port='5000')
