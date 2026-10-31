from datetime import date
from xml.sax.saxutils import escape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def clean(text):
    # Remove characters the PDF font cannot show, and escape symbols like & and <
    text = str(text).encode("cp1252", "ignore").decode("cp1252")
    return escape(text)


def make_pdf(stock, headlines, analysis, filename):
    styles = getSampleStyleSheet()  # ready-made text styles (Title, Heading2, ...)
    story = []  # the list of things that will go into the PDF, top to bottom

    story.append(Paragraph(clean("TradeLens Report: " + stock["Company"]), styles["Title"]))
    story.append(Paragraph("Report date: " + str(date.today()), styles["BodyText"]))

    story.append(Paragraph("Stock Information", styles["Heading2"]))
    for label, value in stock.items():
        story.append(Paragraph(clean(label + ": " + str(value)), styles["BodyText"]))

    story.append(Paragraph("Latest News", styles["Heading2"]))
    if len(headlines) == 0:
        story.append(Paragraph("No news found.", styles["BodyText"]))
    for headline in headlines:
        story.append(Paragraph(clean("- " + headline), styles["BodyText"]))

    story.append(Paragraph("AI Analysis", styles["Heading2"]))
    for line in analysis.split("\n"):
        line = line.strip()
        if line == "":
            continue  # skip empty lines
        if line.endswith(":"):
            story.append(Paragraph(clean(line), styles["Heading3"]))  # a section heading
        else:
            story.append(Paragraph(clean(line), styles["BodyText"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("This report is for learning only. It is not financial advice.", styles["Italic"]))

    SimpleDocTemplate(filename).build(story)  # create the PDF file
