from flask import Flask, request, redirect, url_for, Response
import csv
from datetime import datetime
from collections import defaultdict
import io

app = Flask(__name__)
entries = []

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Mini List App</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 40px auto; background: #fff; padding: 24px; border-radius: 8px; box-shadow: 0 2px 8px #ccc; }}
        h1 {{ text-align: center; font-family: Georgia; color: black;  }}
        form {{ margin-bottom: 24px; }}
        input, select {{ padding: 8px; margin: 4px 0; width: 100%; box-sizing: border-box; border-radius: 20px;  }}
        input:hover {{ background: #f0f0f0; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #f0f0f0; }}
        .actions {{ margin-top: 16px; text-align: center; }}
        .actions a {{ margin: 0 8px; text-decoration: none; color: #007bff; }}
        .summary {{ margin-top: 24px; }}
        button {{ background: #007bff; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 10px; }}
        h2 {{ font-family: Georgia; color: black; width: 20ch; text-wrap: nowrap; overflow: hidden; animation: typing 2s steps(20) infinite alternate-reverse; @keyframes typing {{ from {{ width: 0ch; }} to {{ width: 20ch; }} }} }}
    </style>
</head>
<body>
<div class="container">
    <h1>Mini List App</h1>
    <form method="post" action="/add">
        <label>Date: <input type="date" name="date" value="{date_today}" required></label><br>
        <label>Amount: <input type="number" step="0.01" name="amount" required></label><br>
        <label>Category: <input type="text" name="category" required></label><br>
        <label>Description: <input type="text" name="description" required></label><br>
        <button type="submit">Add Entry</button>
    </form>
    <div class="actions">
        <a href="/export">Export to CSV</a> |
        <a href="/monthly">Monthly Summary</a> |
        <a href="/category">Category Summary</a>
    </div>
    <h2>Current List</h2>
    <table>
        <tr><th>#</th><th>Date</th><th>Amount</th><th>Category</th><th>Description</th></tr>
        {rows}
    </table>
</div>
</body>
</html>
'''

SUMMARY_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 40px auto; background: #fff; padding: 24px; border-radius: 8px; box-shadow: 0 2px 8px #ccc; }}
        h1 {{ text-align: center; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #f0f0f0; }}
        .actions {{ margin-top: 16px; text-align: center; }}
        .actions a {{ margin: 0 8px; text-decoration: none; color: #007bff; }}
    </style>
</head>
<body>
<div class="container">
    <h1>{title}</h1>
    <div class="actions">
        <a href="/">Back to Home</a>
    </div>
    <table>
        <tr><th>{col1}</th><th>Total</th></tr>
        {rows}
    </table>
</div>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    rows = "".join(f"<tr><td>{i+1}</td><td>{e['date']}</td><td>{e['amount']:.2f}</td><td>{e['category']}</td><td>{e['description']}</td></tr>" for i, e in enumerate(entries))
    return HTML_TEMPLATE.format(
        date_today=datetime.today().strftime('%Y-%m-%d'),
        rows=rows
    )

@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    amount = float(request.form['amount'])
    category = request.form['category']
    description = request.form['description']
    entries.append({
        'date': date,
        'amount': amount,
        'category': category,
        'description': description
    })
    return redirect(url_for('index'))

@app.route('/export')
def export():
    si = io.StringIO()
    writer = csv.DictWriter(si, fieldnames=['date', 'amount', 'category', 'description'])
    writer.writeheader()
    for entry in entries:
        writer.writerow(entry)
    output = si.getvalue()
    return Response(
        output,
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=expenses.csv"}
    )

@app.route('/monthly')
def monthly():
    summary = defaultdict(float)
    for entry in entries:
        month = entry['date'][:7]
        summary[month] += entry['amount']
    rows = "".join(f"<tr><td>{month}</td><td>{total:.2f}</td></tr>" for month, total in sorted(summary.items()))
    return SUMMARY_TEMPLATE.format(title="Monthly Summary", col1="Month", rows=rows)

@app.route('/category')
def category():
    summary = defaultdict(float)
    for entry in entries:
        summary[entry['category']] += entry['amount']
    rows = "".join(f"<tr><td>{cat}</td><td>{total:.2f}</td></tr>" for cat, total in sorted(summary.items()))
    return SUMMARY_TEMPLATE.format(title="Category Summary", col1="Category", rows=rows)

if __name__ == '__main__':
    app.run()