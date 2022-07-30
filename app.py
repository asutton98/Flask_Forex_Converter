from flask import Flask,request, render_template , redirect , flash ,jsonify
from flask_debugtoolbar import DebugToolbarExtension
import currency
from currency import rates


app = Flask(__name__)
app.config['SECRET_KEY'] = "chickensRcool"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

def convert_to_float(s):
    try:
        return float(s)
    except ValueError:
        return None

@app.route('/')
def home_page():
    rep = rates.get_rates('USD').keys()
    return render_template('home.html' , rep = rep)

@app.route('/results')
def handle_form():
    """Handle conversion form."""

    code_from = request.args['code_from'].upper()
    code_to = request.args['code_to'].upper()
    amt = convert_to_float(request.args['amount'])
    errs = []

    if amt is None:
        errs.append("Not a valid amount.")

    if not currency.check_code(code_from):
        errs.append(f"Not a valid code: {code_from}")

    if not currency.check_code(code_to):
        errs.append(f"Not a valid code: {code_to}")

    if not errs:
        result = currency.convert_with_symbol(code_from, code_to, amt)
        if result is None:
            errs.append("Conversion failed.")

    if errs:
        for err in errs:
            flash(err)
        return render_template("home.html",
                               code_from=code_from,
                               code_to=code_to,
                               amt=amt or "")

    else:
        return render_template("results.html", result=f"{result}")
