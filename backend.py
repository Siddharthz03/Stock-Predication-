import yfinance as yf
import google.generativeai as genai
import mysql.connector

# Configure Gemini API key
genai.configure(api_key="AIzaSyD2FQcuLrFUNEC49mgFgc-z6D8HvdGUzw0")

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin2024",
    database="stock_analysis"
)
cursor = db.cursor()

# 🔮 AI Prediction Function
def get_ai_prediction_summary(ticker, last_price):
    prompt = f"""
    The current stock price of {ticker.upper()} is ₹{last_price}.
    Based on this and general financial knowledge, would this be a good investment? 
    Provide a short, clear explanation.
    """

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text.strip()

# 🔧 Main Stock Analysis Function
def predict_stock(ticker):
    try:
        # 🛠️ Sanitize ticker input
        if ticker.lower().endswith(".ns"):
            ticker = ticker[:-3]
        full_ticker = f"{ticker.upper()}.NS"

        stock = yf.Ticker(full_ticker)
        last_price = stock.info.get('regularMarketPrice')

        if last_price is None:
            raise ValueError("No market price found")

        ai_prediction = get_ai_prediction_summary(ticker, last_price)

        # Save to DB
        cursor.execute("""
            INSERT INTO stocks (ticker, last_price, ai_prediction)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE last_price=%s, ai_prediction=%s
        """, (ticker, last_price, ai_prediction, last_price, ai_prediction))
        db.commit()

        return ai_prediction, last_price

    except Exception as e:
        print(f"[❌ Error] {e}")
        return "Error fetching data", 0.0
    except Exception as e:
        print(f"[❌ Error] {e}")
        return "Error fetching data", 0.0