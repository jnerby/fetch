# Add transactions for a specific payer and date
# Spend points and return list of { "payer": <string>, "points": <integer> }
# Return all payer point balances

# Can store transactions in memory
from flask import Flask, jsonify, redirect, render_template, request
from datetime import datetime

app = Flask(__name__)
app.secret_key = "dev"

# Global variable to store transactions in memory
TRANSACTIONS = []

@app.route("/")
def render_homepage():
    """Render homepage template"""
    return render_template("base.html")

@app.route('/add', methods=['GET', 'POST'])
def add_transactions():
    """Add transactions for specific payer and date"""
    if request.method == 'POST':
        payer = request.form['payer']
        points = int(request.form['points'])
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        # create dictionary of current transaction
        current = {'payer': payer,
                    'points': points,
                    'timestamp': timestamp}
        # store current transaction in global var
        TRANSACTIONS.append(current)

        # return jsonify(TRANSACTIONS)
        print(TRANSACTIONS)
        return redirect('/')
    # if method is GET, render base template
    return render_template("base.html")

@app.route('/spend', methods=['GET', 'POST'])
def spend_points():
    """Spend user's points"""
    to_spend = int(request.form['to-spend'])
    # print(to_spend)
    resp = []

    avail_points = []

    # get positive transactions sorted from oldest to newest
    for transaction in TRANSACTIONS:
        # get positive transactions
        if transaction['points'] > 0:
            # create tuples to sort by timestamp
            tup = (transaction['timestamp'], transaction['points'], transaction['payer'])
            avail_points.append(tup) 

    # sort all possible points by timestamp      
    avail_points.sort()

    for transaction in avail_points:
        if to_spend == 0:
            break
        points = transaction[1]
        # if surplus points, set to spend to 0 and subtract value of to_spend
        if to_spend < points:
            to_deduct = to_spend
            to_spend = 0
        # if to_spend is greater, deduct all points and subtract points from to_spend
        if to_spend > points:
            to_deduct = points
            to_spend -= points 
        # create new transaction to subtract points
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        current = {'payer': transaction[2],
            'points': -to_deduct,
            'timestamp': timestamp}
        # append point deduction to transactions   
        TRANSACTIONS.append(current)
        resp.append({'payer': transaction[2], 'points': -to_deduct})

    # print(TRANSACTIONS)
    # print(resp)

    return jsonify(resp)
    # return redirect('/')
    

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )