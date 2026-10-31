from dotenv import load_dotenv
from graph import build_graph

load_dotenv()  # read the API keys and email details from the .env file

print("===== TradeLens: Stock Research Agent =====")
symbol = input("Enter a stock symbol (example: AAPL, TSLA, RELIANCE.NS): ").strip().upper()

app = build_graph()             # build the LangGraph workflow
app.invoke({"symbol": symbol})  # run it, starting with the symbol in the state
