from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    total_dict = mongo.db.total_dict.find_one()
    return render_template("index.html", total_dict = total_dict)

@app.route("/scrape")
def scraper():
    total_dict = mongo.db.total_dict
    total_data = scrape_mars.scrape()
    total_dict.update({},total_data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)