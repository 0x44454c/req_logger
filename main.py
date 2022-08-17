# Request Logger
# Author: Delusional

import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask("req_logger")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///req_logger.db"
app.config["SECRET_KEY"] = "my_own_secret"
db = SQLAlchemy(app)

class req_logger(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	method = db.Column(db.String(8), nullable=False)
	time = db.Column(db.DateTime, nullable=False)
	ip = db.Column(db.Text)
	raw_url = db.Column(db.Text)
	headers = db.Column(db.Text)
	args = db.Column(db.Text)
	form = db.Column(db.Text)
	json = db.Column(db.Text)
	data = db.Column(db.Text)

db.create_all()


def iter_to_str(iter):
	data_str = ""
	for each in iter:
		data_str += f"{each[0]}: {each[1]}\n"

	return data_str


@app.route("/req", methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"])
def log():
	method = request.method
	time = datetime.datetime.now()
	ip = request.remote_addr
	raw_url = request.url
	headers = iter_to_str(request.headers.items())
	args = iter_to_str(request.args.items(multi=True))
	form = iter_to_str(request.form.items(multi=True))
	json_str = json.dumps(request.get_json(silent=True), indent=4)
	data = request.get_data(as_text=True)
	if not args: args = ""
	if not form: form = ""
	if json_str=='null': json_str = ""
	if not data: data = ""

	req_data = req_logger(method=method, time=time, ip=ip, raw_url=raw_url, headers=headers, args=args, form=form, json=json_str, data=data)
	db.session.add(req_data)
	db.session.commit()

	return "0"

if __name__ == "__main__":
	app.run(host="192.168.29.141", port=8080)