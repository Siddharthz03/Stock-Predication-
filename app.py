# app.py
from flask import Flask, render_template, request, jsonify
from main import analyze  # Import your logic
from main import predict_stock
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_stock_api():  # ✅ changed name to avoid conflict
    data = request.get_json()
    ticker_input = data.get('ticker', '').strip()

    if not ticker_input:
        return jsonify({'error': 'Ticker is required'}), 400

    try:
        ticker, price, prediction = predict_stock(ticker_input)
        return jsonify({
            'ticker': ticker,
            'last_price': price,
            'prediction': prediction
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True)