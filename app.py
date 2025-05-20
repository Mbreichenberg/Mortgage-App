from flask import Flask, render_template, request, send_file, session
import openpyxl
import xlsxwriter
import pandas as pd
import io
import requests
from helper import create_excel
from decimal import Decimal, getcontext
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.secret_key = 'AylaJunoCats'

getcontext().prec = 28  # Set precision for financial calculations

# Global currency code and symbol maps
CURRENCY_CODE_MAP = {
    '1': 'USD',
    '2': 'BRL',
    '3': 'EUR',
    '4': 'JPY',
    '5': 'AUD',
    '6': 'MXN',
    '7': 'CAD'
}

CURRENCY_SYMBOL_MAP = {
    'USD': '$',
    'BRL': 'R$',
    'EUR': '€',
    'JPY': '¥',
    'AUD': 'A$',
    'MXN': 'Mex$',
    'CAD': 'C$'
}

# Exchange rate API config
API_KEY = '77b589a6647cc952825a4fbe'
BASE_URL = 'https://api.exchangerate-api.com/v4/latest/'

@app.template_filter('stringformat')
def string_format(value):
    if isinstance(value, Decimal):
        value = value.quantize(Decimal('0.01'))
    return f"{value:,.2f}"

def calculate_amortization_schedule(principal, annual_interest_rate, years, currency_symbol):
    schedule = []
    months = years * 12
    monthly_interest_rate = annual_interest_rate / Decimal('12')

    monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** months) / \
                      ((1 + monthly_interest_rate) ** months - 1)

    balance = principal
    total_interest = Decimal('0.0')
    total_principal = Decimal('0.0')

    for month in range(1, months + 1):
        interest = balance * monthly_interest_rate
        principal_payment = monthly_payment - interest
        balance -= principal_payment
        balance = max(balance, Decimal('0.0'))

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
        try:
            principal = Decimal(request.form['principal'].replace(',', ''))
            annual_interest_rate = Decimal(request.form['interest_rate'])
            years = int(request.form['years'])
            currency_choice = request.form['base_currency']
        except Exception as e:
            return f"Error converting input values: {e}"

        base_currency_code = CURRENCY_CODE_MAP.get(currency_choice, 'USD')
        currency_symbol = CURRENCY_SYMBOL_MAP.get(base_currency_code, '$')

        session['base_currency'] = base_currency_code
        session['original_principal'] = str(principal)
        session['original_currency'] = base_currency_code

        try:
            monthly_payment, schedule, total_principal, total_interest = calculate_amortization_schedule(
                principal, annual_interest_rate / Decimal('100'), years, currency_symbol
            )
        except Exception as e:
            return f"Error calculating amortization: {e}"

        return render_template('result.html',
                               monthly_payment=monthly_payment,
                               schedule=schedule,
                               currency_symbol=currency_symbol,
                               principal=principal,
                               annual_interest_rate=annual_interest_rate,
                               years=years,
                               currency_choice=base_currency_code,
                               total_principal=total_principal,
                               total_interest=total_interest)

    return render_template('index.html')

@app.route('/convert_results', methods=['POST'])
def convert_results():
    try:
        annual_interest_rate = Decimal(request.form['interest_rate'])
        years = int(request.form['years'])
        target_currency = request.form['target_currency']

        base_currency = session.get('original_currency', 'USD')
        principal = Decimal(session.get('original_principal', '0'))
    except Exception as e:
        return f"Error with form inputs: {e}"

    try:
        response = requests.get(f'{BASE_URL}{base_currency}')
        rates = response.json().get('rates', {})
        conversion_rate = Decimal(str(rates.get(target_currency, 1)))
    except Exception as e:
        return f"Error fetching conversion rates: {e}"

    converted_principal = (principal * conversion_rate).quantize(Decimal('0.01'))
    currency_symbol = CURRENCY_SYMBOL_MAP.get(target_currency, '$')

    try:
        monthly_payment, schedule, total_principal, total_interest = calculate_amortization_schedule(
            converted_principal, annual_interest_rate / Decimal('100'), years, currency_symbol
        )
    except Exception as e:
        return f"Error recalculating results: {e}"

    session['base_currency'] = target_currency

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
    try:
        principal = Decimal(request.form['principal'])
        annual_interest_rate = Decimal(request.form['interest_rate'])
        years = int(request.form['years'])
        currency_choice = request.form['currency']
    except Exception as e:
        return f"Error with form inputs: {e}"

    currency_symbol = CURRENCY_SYMBOL_MAP.get(currency_choice, '$')

    try:
        monthly_payment, schedule, total_principal, total_interest = calculate_amortization_schedule(
            principal, annual_interest_rate / Decimal('100'), years, currency_symbol
        )
    except Exception as e:
        return f"Error generating amortization schedule: {e}"

    output = create_excel(schedule, currency_symbol)

    return send_file(
        output,
        as_attachment=True,
        download_name="amortization_schedule.xlsx",
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# if __name__ == '__main__':
#     app.run(debug=True)
