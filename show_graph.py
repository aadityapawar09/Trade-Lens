from graph import build_graph

app = build_graph()
# Prints the workflow as a Mermaid diagram. Paste it into https://mermaid.live to see the picture.
print(app.get_graph().draw_mermaid())
