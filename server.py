import os
from flask import flash, Flask, jsonify, redirect, render_template, request
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
        # resp = []
        res = {}

        avail_points = []
        total_points = 0

        # sort transactions sorted from oldest to newest
        for transaction in TRANSACTIONS:
            # create tuples to sort by timestamp
            tup = (transaction['timestamp'], transaction['points'], transaction['payer'])
            avail_points.append(tup) 
            total_points += transaction['points']

        # if user has enough points, start spending
        if to_spend <= total_points:

            # sort all possible points by timestamp      
            avail_points.sort()

            for tup in avail_points:
                if to_spend == 0:
                    break
                
                points = tup[1]
                payer = tup[2]
                # if transaction has surplus points, set to spend to 0 and subtract value of to_spend
                if to_spend <= points:
                    to_deduct = to_spend
                    to_spend = 0
                # if to_spend exceeds transaction's points, deduct all points and subtract points from to_spend
                if to_spend > points:
                    to_deduct = points
                    to_spend -= points 

                # create new transaction to subtract points
                timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                current = {'payer': tup[2],
                    'points': -to_deduct,
                    'timestamp': timestamp}
                # update transactions to include point deduction  
                TRANSACTIONS.append(current)

                if payer in res:
                    res[payer] -= to_deduct
                else:
                    res[payer] = -to_deduct

            return jsonify(res)
            # return jsonify(resp)

        # if user does not have enough points, notify
        else:
            flash(f"Insufficient funds. Current point balance is {total_points}.")
            return redirect('/')

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
    app.run(host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 4444)))