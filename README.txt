To view this project, install Homebrew and git. run "git clone https://github.com/jnerby/fetch.git" and cd into the fetch directory in your VS Code Terminal.
Run "pip3 install -r requirements.txt" from the command line, then run "python3 server.py." 
Click on the address in "* Running on ..." in the terminal window to open the web service in your browser.

The web service contains three input forms, one to add a new transaction, one to spend points, and one to view all point balances by payer.
Each request returns a JSON object in a new route. Click the back arrow in your browser to return to the User Rewards Homepage.

Given more time, I would use a SQL database to store transaction data and improve the UI with more navigation options.