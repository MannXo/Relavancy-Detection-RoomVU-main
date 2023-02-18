import io
from SpacyModel import SpacyModel

from flask import Flask, render_template, request
from utils import validate_file_features

app = Flask(__name__, static_folder="static")


@app.route("/")
def form():
    return render_template("form.html")


@app.route("/train", methods=["POST"])
def upload_file_train():
    f = request.files["data_file"]
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    result = validate_file_features(stream.read(), "train")
    training_results = SpacyModel(df=result).train()
    return training_results, 200

@app.route("/test", methods=["POST"])
def upload_file_test():
    f = request.files["data_file"]
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    result = validate_file_features(stream.read(), "test")
    testing_results = SpacyModel(df=result,batch_testing=True).batch_evaluate()
    return testing_results, 200

@app.route("/manual_predict", methods=["POST"])
def manual_predict():
    if request.form['Title']:
        values = SpacyModel().predict(request.form['Title'])
        print(values)
        response = f"news with title {request.form['Title']} is {max(values, key=values.get)} to realstate market.\nplease press back button."
        return response,  200
    else:
        return 'error', 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
