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

        return jsonify(TRANSACTIONS)

    # if method is GET, render base template
    return render_template("base.html")


@app.route('/spend', methods=['POST'])
def spend_points():
    """Spend user's points"""
    if request.method == 'POST':
        # cast user submitted value to int
        to_spend = int(request.form['to-spend'])
        # initialize empty list to jsonify in response
        resp = []

        # get positive transactions sorted from oldest to newest
        avail_points = []
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
            # if transaction has surplus points, set to spend to 0 and subtract value of to_spend
            if to_spend < points:
                to_deduct = to_spend
                to_spend = 0
            # if to_spend exceeds transaction's points, deduct all points and subtract points from to_spend
            if to_spend > points:
                to_deduct = points
                to_spend -= points 
            # create new transaction to subtract points
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            current = {'payer': transaction[2],
                'points': -to_deduct,
                'timestamp': timestamp}
            # update transactions to include point deduction  
            TRANSACTIONS.append(current)
            resp.append({'payer': transaction[2], 'points': -to_deduct})

        return jsonify(resp)

    # if method is GET, redirect to base
    return redirect('/')


@app.route('/balance', methods=['POST'])
def return_balances():
    if request.method == 'POST':
        # init empty dict to store balances
        balances = {}
        # loop through all transactions to calc balance per payer
        for transaction in TRANSACTIONS:
            if transaction['payer'] in balances:
                balances[transaction['payer']] += transaction['points']
            else:
                balances[transaction['payer']] = transaction['points']

        return jsonify(balances)

    # if method is GET, redirect to base 
    return redirect('/')


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True,
    )