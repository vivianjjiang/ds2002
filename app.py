
from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd
import json
import plotly

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    chart_type = request.form.get("chart_type", "box")
    df = pd.read_csv("coffee_exports.csv")

    if chart_type == "bar":
        fig = px.bar(df, x="Country", y="Export_quantity", color="Coffee_type", title="Coffee Export Quantity by Country")
    elif chart_type == "scatter":
        fig = px.scatter(df, x="Year", y="Export_quantity", color="Country", title="Coffee Exports Over Time")
    else:
        fig = px.box(df, x="Country", y="Export_quantity", color="Coffee_type", title="Coffee Export Distribution by Country")

    fig.update_layout(
        plot_bgcolor='#1a1c23',
        paper_bgcolor='#1a1c23',
        font_color='#ffffff',
        autosize=True,
        margin=dict(t=50, l=50, r=50, b=50),
        height=600
    )
    fig.update_xaxes(showgrid=False, color='#cccccc')
    fig.update_yaxes(showgrid=False, color='#cccccc')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("index.html", graphJSON=graphJSON, chart_type=chart_type)

if __name__ == "__main__":
    app.run(debug=True)
