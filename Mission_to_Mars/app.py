from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection to mars_db database
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def index():
    print("Querying the data")
    marsdata = mongo.db.marsdata.find_one()
    print("Started rendering the page...")
    # print(marsdata.html_table)
    return render_template("index.html", listings=marsdata)

@app.route("/scrape")
def scraper():
    
    # remove previous documents before insert
    mongo.db.marsdata.delete_many({})

    # Run the scrape function
    mars_data = scrape_mars.scrape()
    print("Completed scraping and before insert to database")
    
    # Insert the document into the database
    mongo.db.marsdata.insert_one(mars_data)
    
    print("Return back to home page")
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
