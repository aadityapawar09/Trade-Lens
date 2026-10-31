from stock import get_stock_data
from news import get_news
from ai import analyze_stock
from report import make_pdf
from emailer import send_email

# Every node (step) receives the "state" (a dictionary) and returns
# a dictionary with the new things it wants to save in the state.


def stock_node(state):
    print("\nFetching stock data...")
    stock = get_stock_data(state["symbol"])
    if stock is None or stock["Price"] is None:
        print("Sorry, I could not find that stock. Please check the symbol.")
        return {"stock": None}
    print(stock["Company"], "is trading at", stock["Price"], stock["Currency"])
    return {"stock": stock}


def news_node(state):
    print("Searching for financial news...")
    return {"headlines": get_news(state["stock"]["Company"])}


def analysis_node(state):
    print("Asking Gemini to analyze the stock...")
    return {"analysis": analyze_stock(state["stock"], state["headlines"])}


def report_node(state):
    filename = state["symbol"] + "_report.pdf"
    make_pdf(state["stock"], state["headlines"], state["analysis"], filename)
    print("Report saved as", filename)
    return {"filename": filename}


def ask_email_node(state):
    answer = input("\nDo you want to email this report? (yes/no): ").strip().lower()
    if answer != "yes":
        print("No email sent. Goodbye!")
    return {"wants_email": answer == "yes"}


def recipient_node(state):
    email = input("Enter the recipient's email address: ").strip()
    if "@" not in email or "." not in email:
        print("That does not look like a valid email address. Please try again.")
        email = ""
    return {"recipient": email}


def confirm_node(state):
    answer = input("Send the report to " + state["recipient"] + "? (yes/no): ").strip().lower()
    if answer != "yes":
        print("Email cancelled.")
    return {"confirmed": answer == "yes"}


def send_node(state):
    send_email(state["recipient"], state["filename"])  # nothing new to save in the state
