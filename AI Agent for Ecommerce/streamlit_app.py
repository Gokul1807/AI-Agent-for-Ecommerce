# streamlit_app.py

import streamlit as st
import requests
from PIL import Image
import io
import base64

st.set_page_config(page_title="E-commerce AI Agent", layout="centered")
st.title("AI Agent for Ecommerce 🛒")
st.text("Developed by Gokul R") 

# Input field
question = st.text_input("Enter your question:", placeholder="e.g., What is my total sales?")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question to generate !")
    else:
        # Call FastAPI /ask endpoint
        with st.spinner("Thinking..."):
            response = requests.post("http://localhost:8000/ask", json={"question": question})

        if response.status_code == 200:
            data = response.json()
            st.success("Response received from user !")

            # Show SQL Query
            st.markdown("**SQL Query Generated based on user query :**")
            st.code(data.get("sql_query", "No SQL generated."), language="sql")

            # Show Answer
            st.markdown("**Answer for query :**")
            if "response" in data and "rows" in data["response"]:
                rows = data["response"]["rows"]
                columns = data["response"]["columns"]
                if rows:
                    st.dataframe([dict(zip(columns, row)) for row in rows])
                else:
                    st.info("No results found ")
            else:
                st.warning("No data returned ")

            # Show Chart (if available)
            if "chart" in data:
                chart_base64 = data["chart"].split(",")[-1]  # remove the data:image/png;base64, prefix
                image_bytes = base64.b64decode(chart_base64)
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption="Visualized Chart", use_column_width=True)
        else:
            st.error("Failed to get response from FastAPI ")