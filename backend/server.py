import flask
import BTL_model
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    input_data = flask.request.json
    model = BTL_model.BTLModel(4)
    model.maximize_log_likelihood(input_data)
    return flask.jsonify(model.get_estimates().tolist())

if __name__ == '__main__':
    app.run(port=5000)
