# TradeLens Code Guide

A simple explanation of every file, so you can explain the project with confidence.

## The big picture
TradeLens is a **workflow**: a list of steps that run one after another, with a few yes/no decisions on the way. LangGraph lets us describe that workflow as a **graph** (like a flowchart) and then runs it for us.

```
symbol -> stock -> news -> analysis -> report -> ask email? -> ask address -> confirm -> send
```

## What is LangGraph? (the 5 words to remember)
- **State**: a shared notebook (a dictionary). Every step can read from it and write to it. Example: the stock step writes `stock`, and the news step reads it.
- **Node**: one step. It is just a normal Python function. It receives the state and returns the new things to save.
- **Edge**: an arrow from one node to the next.
- **Conditional edge**: an arrow that chooses the next node by looking at the state (a yes/no decision).
- **compile() and invoke()**: `compile()` turns the plan into a runnable workflow. `invoke()` runs it.

## main.py
1. `load_dotenv()` reads the secret keys from the `.env` file.
2. `input(...)` asks for the stock symbol. `.strip()` removes extra spaces and `.upper()` makes capital letters.
3. `build_graph()` creates the workflow.
4. `app.invoke({"symbol": symbol})` runs it. The symbol is the first thing we put in the state.

## graph.py (the map)
- **TradeState** lists the names of everything stored in the state. It uses the word `class`, but it is only a labeled list of fields. It is the one class in the project, and LangGraph needs it.
- **Decision functions** (`check_stock`, `check_wants_email`, `check_recipient`, `check_confirmed`) look at the state and return a word like `"found"` or `"no"`.
- **build_graph()** does three things:
  1. `add_node("name", function)` adds each step.
  2. `add_edge("a", "b")` draws an arrow from a to b.
  3. `add_conditional_edges("a", decision_function, {"word": "next step"})` says: ask the decision function, then follow the arrow that matches the word it returns.
- `END` means "stop here".
- The `invalid` email arrow points back to `ask_recipient`. This makes a **loop**, so the program asks again until the address looks valid.

## nodes.py (the steps)
Each function is one box in the diagram:
- `stock_node`: fetches stock data. If the stock is not found, it saves `None` and the graph stops.
- `news_node`: searches the news and saves the headlines.
- `analysis_node`: sends the data and headlines to Gemini and saves the answer.
- `report_node`: creates the PDF and saves the file name.
- `ask_email_node`: asks "Do you want to email this report?" and saves True or False.
- `recipient_node`: asks for the address. It must contain `@` and `.`, otherwise it saves an empty text.
- `confirm_node`: asks for the final confirmation and saves True or False.
- `send_node`: sends the email.

## Helper files (the tools used by the steps)
- **stock.py**: `yf.Ticker(symbol).info` gives a dictionary of facts. `info.get("key", "N/A")` avoids a crash if a value is missing. `try / except` returns `None` if something fails.
- **news.py**: Tavily searches the web. `topic="news"` asks for news and `max_results=5` limits the results. A `for` loop keeps only the titles.
- **ai.py**: builds a `prompt` (the instruction for Gemini) from the stock data and headlines, sends it with `generate_content`, and returns `response.text`. `MODEL_NAME` is at the top so it is easy to change.
- **report.py**: ReportLab builds the PDF from a list called `story`, where each item is a `Paragraph` with a style. `clean()` removes characters the PDF font cannot show.
- **emailer.py**: `EmailMessage` builds the email and attaches the PDF. `with open(...)` opens the file and closes it by itself. `SMTP_SSL("smtp.gmail.com", 465)` connects securely to Gmail. Gmail needs an **App Password**.

## show_graph.py
Prints the workflow as a Mermaid diagram. Paste it into https://mermaid.live to see the picture. Useful for your presentation.

## The .env file
It stores secrets outside the code. `.gitignore` lists `.env`, so the secrets are not uploaded to GitHub. `.env.example` shows the format with empty values.

## Python ideas used
Variables, `input` and `print`, functions with `return`, `if / else`, `for` loops, lists, dictionaries, `try / except`, `with`, and one `TypedDict`.

## Questions you may be asked
- **Why LangGraph?** It turns the steps into a clear graph. It is easy to see, easy to add a new step, and it supports decisions and loops.
- **Could this be done without LangGraph?** Yes, with plain `if / else`. A small project like this works either way. LangGraph makes the flow clearer and is a popular tool for AI workflows.
- **Is it an AI agent?** It is a fixed workflow. Gemini writes the analysis, but simple rules in the code choose the next step. LangGraph can also build agents where the AI chooses the next step.
- **What is the state?** A shared dictionary that carries data from one step to the next.
- **Node vs edge?** A node is a step (a function). An edge is the arrow between steps.
- **What is a conditional edge?** An arrow where the next step depends on the state, like "send email: yes or no".
- **Why separate files?** Each file does one job, so the code is easier to read and fix.
- **Why a `.env` file?** Keys should never be written in code or uploaded online.
- **Why `try / except`?** The internet or an API can fail. This way the program shows a message instead of crashing.
- **Why confirm before sending?** An email cannot be taken back, so I ask twice.
- **What could be improved?** Search by company name, compare two stocks, add charts to the PDF.
