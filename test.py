# test_main.py

from backend import predict_stock

ticker = input("Enter NSE stock ticker (e.g., INFY, TCS): ").upper()
prediction, price = predict_stock(ticker)

print("\n📈 Stock Analysis Result")
print(f"Ticker      : {ticker}")
print(f"Last Price  : ₹{price}")
print(f"AI Prediction:\n{prediction}")