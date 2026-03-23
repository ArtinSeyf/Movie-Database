from flask import Flask, jsonify, request

# create the app
app = Flask(__name__)

# test route to see if server is working
@app.route("/")
def home():
    return "Backend is running"

# this route will later return movie data
# empty list for now
@app.route("/movies")
def movies():
    return jsonify([])

# route for the filters web page takes values from the URL and sends them back 
# to check everything is being received properly
@app.route("/filter")
def filter_movies():
    
    # get values from URL 
    year_min = request.args.get("yearMin")
    year_max = request.args.get("yearMax")

    budget_min = request.args.get("budgetMin")
    budget_max = request.args.get("budgetMax")

    revenue_min = request.args.get("revenueMin")
    revenue_max = request.args.get("revenueMax")

    # returns values to test it works
    return jsonify({
        "yearMin": year_min,
        "yearMax": year_max,
        "budgetMin": budget_min,
        "budgetMax": budget_max,
        "revenueMin": revenue_min,
        "revenueMax": revenue_max
    })

# runs app
if __name__ == "__main__":
    app.run(debug=True)