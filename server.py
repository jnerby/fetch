# Add transactions for a specific payer and date
# Spend points and return list of { "payer": <string>, "points": <integer> }
# Return all payer point balances

# Can store transactions in memory
from flask import Flask, redirect, render_template, request
from datetime import datetime

app = Flask(__name__)
app.secret_key = "dev"

# Global variable to store transactions in memory
# TRANSACTIONS = []
TRANSACTIONS = [{'payer': 'Dannon', 'points': 500, 'timestamp': '2022-01-03T12:12:18Z'}, 
                {'payer': 'Miller Coors', 'points': 500, 'timestamp': '2021-01-03T12:12:22Z'}, 
                {'payer': 'Miller Coors', 'points': -100, 'timestamp': '2021-01-03T12:12:22Z'}, 
                {'payer': 'Dannon', 'points': 500, 'timestamp': '2022-01-03T12:12:22Z'}, 
                {'payer': 'Unilever', 'points': -1000, 'timestamp': '2022-01-03T12:12:27Z'}]

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

        return redirect("/")
    return render_template("base.html")

@app.route('/spend', methods=['GET', 'POST'])
def spend_points():
    """Spend user's points"""
    to_spend = int(request.form['to-spend'])

    possible_points = []

    # get positive transactions sorted from oldest to newest
    for transaction in TRANSACTIONS:
        # get positive transactions
        if transaction['points'] > 0:
            # create tuples to sort by timestamp
            tup = (transaction['timestamp'], transaction['points'], transaction['payer'])
            possible_points.append(tup) 

    # sort all possible points by timestamp      
    possible_points.sort()

    # loop over possible points until to_spend is 0
    while to_spend > 0:
        for item in possible_points:
            payer = item[2]
            points = item[1]
            # if item has surplus points
            if points > to_spend:
                # create new transaction to subtract points from payer
                timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                current = {'payer': payer,
                    'points': -to_spend,
                    'timestamp': timestamp}   
                TRANSACTIONS.append(current)
                # set to_spend to 0
                to_spend = 0
                
    print(TRANSACTIONS)
    return redirect('/')
    

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )