from flask import Flask 
from flask import render_template
from flask import redirect
from flask_pymongo import PyMongo
import mars_scrape

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    destination_data = mongo.db.mars_collection.find_one()

    # Return template and data
    return render_template("index.html", mars = destination_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = mars_scrape.scraper_function()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
