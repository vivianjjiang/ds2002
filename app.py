from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd
import numpy as np
import json
import plotly

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    chart_type = request.form.get("chart_type", "box")

    # Generate random data
    df = pd.read_csv("coffee_exports.csv")

    # Select chart type
    if chart_type == "bar":
        fig = px.bar(df, x="Region", y="Export_Tons", color="Country", title="Bar Chart")
    elif chart_type == "scatter":
        fig = px.scatter(df, x="Region", y="Export_Tons", color="Country", title="Scatter Plot")
    else:
        fig = px.box(df, x="Region", y="Export_Tons", color="Country", title="Box Plot")

    # Dark layout
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