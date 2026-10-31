from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from nodes import (stock_node, news_node, analysis_node, report_node,
                   ask_email_node, recipient_node, confirm_node, send_node)


class TradeState(TypedDict, total=False):
    # The "state" is a shared notebook. Every step can read it and write to it.
    symbol: str
    stock: dict
    headlines: list
    analysis: str
    filename: str
    wants_email: bool
    recipient: str
    confirmed: bool


# Decision functions: they read the state and return a word.
# The graph uses that word to choose the next step.
def check_stock(state):
    if state["stock"] is None:
        return "not_found"
    return "found"


def check_wants_email(state):
    if state["wants_email"]:
        return "yes"
    return "no"


def check_recipient(state):
    if state["recipient"] == "":
        return "invalid"
    return "valid"


def check_confirmed(state):
    if state["confirmed"]:
        return "yes"
    return "no"


def build_graph():
    graph = StateGraph(TradeState)

    # 1. Add the steps (called nodes)
    graph.add_node("stock", stock_node)
    graph.add_node("news", news_node)
    graph.add_node("analysis", analysis_node)
    graph.add_node("report", report_node)
    graph.add_node("ask_email", ask_email_node)
    graph.add_node("ask_recipient", recipient_node)
    graph.add_node("confirm", confirm_node)
    graph.add_node("send", send_node)

    # 2. Connect the steps (called edges)
    graph.add_edge(START, "stock")
    graph.add_conditional_edges("stock", check_stock, {"found": "news", "not_found": END})
    graph.add_edge("news", "analysis")
    graph.add_edge("analysis", "report")
    graph.add_edge("report", "ask_email")
    graph.add_conditional_edges("ask_email", check_wants_email, {"yes": "ask_recipient", "no": END})
    graph.add_conditional_edges("ask_recipient", check_recipient, {"valid": "confirm", "invalid": "ask_recipient"})
    graph.add_conditional_edges("confirm", check_confirmed, {"yes": "send", "no": END})
    graph.add_edge("send", END)

    return graph.compile()  # turn the plan into a runnable workflow
