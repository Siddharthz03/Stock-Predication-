from flask import Flask, render_template, request, jsonify
import yfinance as yf
import mysql.connector
import google.generativeai as genai

# ✅ Set Gemini API Key
genai.configure(api_key="Your_API_Key")

# ✅ MySQL connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin2024",
        database="stock_analysis"
    )
    cursor = db.cursor()
except Exception as e:
    print(f"[❌ DB Connection Error] {e}")
    db = None
    cursor = None

# 🔮 AI Summary Function
def get_ai_prediction_summary(ticker, last_price):
    prompt = f"""
    Analyze the stock {ticker.upper()} with a current price of ₹{last_price}.  
Evaluate its historical price movements, volatility, and trading volume trends.  
Consider past market crashes, industry trends, and major financial events affecting its performance.  
Assess whether it has shown resilience or high risk over time.  
Provide a concise, structured analysis in 5-6 lines.  
Conclude with a final decision: **"Safe to invest"** or **"Risky investment"**, based on historical data.  
"""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[❌ Gemini API Error] {e}")
        return "AI prediction failed."

# 📊 Predict Stock Function
def predict_stock(ticker):
    try:
        ticker = ticker.replace(" ", "").upper()
        if not ticker.endswith(".NS"):
            ticker += ".NS"

        stock = yf.Ticker(ticker)
        info = stock.info

        if not info or "regularMarketPrice" not in info or info["regularMarketPrice"] is None:
            raise ValueError("Invalid or unrecognized stock ticker.")

        last_price = float(info["regularMarketPrice"])
        ai_prediction = get_ai_prediction_summary(ticker, last_price)

        if db and cursor:
            cursor.execute("""
                INSERT INTO stocks (ticker, last_price, ai_prediction)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE last_price=%s, ai_prediction=%s
            """, (ticker[:20], last_price, ai_prediction, last_price, ai_prediction))
            db.commit()

        return ticker, last_price, ai_prediction

    except Exception as e:
        print(f"[❌ Error] {e}")
        return ticker, 0.0, "Error: Invalid or unsupported ticker."

# 🌐 Flask App
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    ticker_input = data.get('ticker', '')
    ticker, price, prediction = predict_stock(ticker_input)
    return jsonify({
        'ticker': ticker,
        'last_price': price,
        'prediction': prediction
    })

if __name__ == '__main__':
    app.run(debug=True)
