# app/visualizer.py

import plotly.graph_objects as go
import base64
from io import BytesIO
import pandas as pd

def generate_sales_bar_chart(columns, rows):
    df = pd.DataFrame(rows, columns=columns)

    # Use 'item_id' as x-axis if product name is not available
    product_col = next((col for col in columns if 'product' in col.lower() or 'item' in col.lower()), 'item_id')
    sales_col = next((col for col in columns if 'sales' in col.lower() or 'amount' in col.lower()), None)

    if not sales_col:
        raise ValueError("Could not determine sales column for visualization.")

    fig = go.Figure(data=[
        go.Bar(x=df[product_col], y=df[sales_col], marker_color='lightskyblue')
    ])
    fig.update_layout(title="Sales per Product", xaxis_title=product_col.title(), yaxis_title=sales_col.title())

    #  Save chart to file
    fig.write_image("output.png")

    #  Also return base64 version for API
    buffer = BytesIO()
    fig.write_image(buffer, format='png')
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return encoded
