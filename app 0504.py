from flask import Flask, render_template, request, send_file, redirect, session, jsonify
import openpyxl
import xlsxwriter
import pandas as pd
import io
import pyzillow
import requests
from helper import create_excel

app = Flask(__name__)
app.secret_key = 'AylaJunoCats'  # Required to use sessions

# Your ExchangeRate API Key
API_KEY = '77b589a6647cc952825a4fbe'
BASE_URL = 'https://api.exchangerate-api.com/v4/latest/USD'  # Example for USD base currency

# (calculate_amortization_schedule function here - same as before)
# Mortgage Amortization Schedule Calculator (User Input with Currency Selection)

def calculate_amortization_schedule(principal, annual_interest_rate, years, currency_symbol):
    schedule = []
    months = years * 12
    monthly_interest_rate = annual_interest_rate / 12

    monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** months) / \
                      ((1 + monthly_interest_rate) ** months - 1)

    balance = principal
    total_interest = 0.0
    total_principal = 0.0

    for month in range(1, months + 1):
        interest = balance * monthly_interest_rate
        principal_payment = monthly_payment - interest
        balance -= principal_payment
        balance = max(balance, 0)  # Avoid small negative due to rounding

        total_interest += interest
        total_principal += principal_payment

        schedule.append({
            'Month': month,
            'Payment': monthly_payment,
            'Interest': interest,
            'Principal': principal_payment,
            'Balance': balance
        })

    return monthly_payment, schedule, total_principal, total_interest


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        principal = float(request.form['principal'].replace(',', ''))
        annual_interest_rate = float(request.form['interest_rate'])
        years = int(request.form['years'])
        currency_choice = request.form['base_currency']  # '1', '2', or '3'

        # Map to actual ISO currency code and store in session
        currency_code_map = {'1': 'USD', '2': 'BRL', '3': 'EUR'}
        base_currency_code = currency_code_map.get(currency_choice, 'USD')
        session['base_currency'] = base_currency_code

        # Use for display only
        currency_symbol = {'1': '$', '2': 'R$', '3': '€'}.get(currency_choice, '$')

        monthly_payment, schedule, total_principal, total_interest = calculate_amortization_schedule(
            principal, annual_interest_rate / 100, years, currency_symbol
        )

        return render_template('result.html',
                               monthly_payment=monthly_payment,
                               schedule=schedule,
                               currency_symbol=currency_symbol,
                               principal=principal,
                               annual_interest_rate=annual_interest_rate,
                               years=years,
                               currency_choice=currency_choice,
                               total_principal=total_principal,
                               total_interest=total_interest)
    return render_template('index.html')

# Route to handle currency conversion requests

@app.route('/convert_results', methods=['POST'])
def convert_results():

    principal = float(request.form['principal'])
    annual_interest_rate = float(request.form['interest_rate'])
    years = int(request.form['years'])
    target_currency = request.form['target_currency']
    new_currency = request.form['base_currency']
    session['base_currency'] = new_currency


    # Get base currency from session
    base_currency = session.get('base_currency', 'USD')

    # Fetch conversion rate
    response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{base_currency}')
    rates = response.json().get('rates', {})
    conversion_rate = rates.get(target_currency, 1)

    # Recalculate results using converted values
    converted_principal = principal * conversion_rate
    currency_symbol = {'USD': '$', 'BRL': 'R$', 'EUR': '€'}.get(target_currency, '$')


    monthly_payment, schedule, total_principal, total_interest = calculate_amortization_schedule(
    principal, annual_interest_rate / 100, years, currency_symbol
)

    # Calculate total principal and total interest
    total_principal = sum(row['Principal'] for row in schedule)
    total_interest = sum(row['Interest'] for row in schedule)

    session['base_currency'] =  target_currency


    return render_template('result.html',
                       monthly_payment=monthly_payment,
                       schedule=schedule,
                       currency_symbol=currency_symbol,
                       principal=converted_principal,
                       annual_interest_rate=annual_interest_rate,
                       years=years,
                       currency_choice=target_currency,
                       total_principal=total_principal,
                       total_interest=total_interest)



@app.route('/download', methods=['POST'])
def download():
    principal = float(request.form['principal'])
    annual_interest_rate = float(request.form['interest_rate'])
    years = int(request.form['years'])
    currency_choice = request.form['currency']

    currency_symbol = {'1': '$', '2': 'R$', '3': '€'}.get(currency_choice, '$')

    # Save to session to persist for reuse
    session['base_currency'] = currency_choice
    session['principal'] = principal
    session['annual_interest_rate'] = annual_interest_rate
    session['years'] = years

    monthly_payment, schedule, total_principal, total_interest = calculate_amortization_schedule(
    principal, annual_interest_rate / 100, years, currency_symbol
)

    output = create_excel(schedule, currency_symbol)

    return send_file(
        output,
        as_attachment=True,
        download_name="amortization_schedule.xlsx",
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if __name__ == '__main__':
    app.run(debug=True)
