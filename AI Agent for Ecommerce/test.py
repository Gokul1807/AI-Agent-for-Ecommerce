# import google.generativeai as genai
# genai.configure(api_key="AIzaSyAZJ8ozaEgE-c4__9oFOgQlhpjpyaDryQc")

# models = genai.list_models()
# for model in models:
#     print(model.name)

import plotly.express as px

# fig = px.bar(x=["A", "B", "C"], y=[10, 20, 30])
# fig.write_image("test_chart.png")  # requires kaleido
# print("Image created successfully.")
import plotly.express as px
import os

# Create a simple bar chart
fig = px.bar(x=["Product A", "Product B", "Product C"], y=[100, 200, 150], title="Sales per Product")

# Define full path to save image
output_path = os.path.abspath("output.png")

# Save the image
fig.write_image(output_path)

# Print confirmation with path
print("Saved to:", output_path)
