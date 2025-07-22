# app/llm_handler.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the Gemini API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT_TEMPLATE = """
You are an expert AI SQL assistant. Convert the user's natural language question into a valid SQL query using **SQLite** syntax only.
Only return the SQL code (no explanations, no markdown).
Here is the schema:

Table: total_sales_metrics(date, item_id, total_sales, total_units_ordered)
Table: ad_sales_metrics(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
Table: eligibility_table(eligibility_datetime_utc, item_id, eligibility, message)

Guidelines:
- Always use INNER JOIN when relevant across tables via item_id.
- If the question is about CPC (Cost Per Click), calculate it as SUM(ad_spend)/SUM(clicks).
- To avoid divide-by-zero, use a `HAVING SUM(clicks) > 0` clause if you’re dividing by SUM(clicks).
- Include WHERE clauses like `eligibility = 'eligible'` if the question implies filtering eligible products.

User Question: "{question}"

SQL:
"""



def convert_question_to_sql(question: str) -> str:
    prompt = PROMPT_TEMPLATE.format(question=question)

    #  Use correct model name
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    # Call the model
    response = model.generate_content(prompt)
    print("Gemini raw response:", response.text)

    # Clean up response (remove markdown if any)
    lines = response.text.strip().split("\n")
    sql_lines = [line for line in lines if not line.startswith("```")]
    return "\n".join(sql_lines).strip()

# Fallback SQL logic when Gemini-generated SQL fails
def get_fallback_sql(question: str) -> str | None:
    q = question.lower()

    if "cpc" in q or "cost per click" in q:
        return """
        SELECT item_id, ROUND(SUM(ad_spend) / SUM(clicks), 2) AS cpc
        FROM ad_sales_metrics
        WHERE clicks > 0
        GROUP BY item_id
        ORDER BY cpc DESC
        LIMIT 1;
        """

    elif "highest total sales" in q or "top selling" in q:
        return """
        SELECT item_id, SUM(total_sales) AS total_sales_amount
        FROM total_sales_metrics
        GROUP BY item_id
        ORDER BY total_sales_amount DESC
        LIMIT 1;
        """

    elif "most clicks" in q:
        return """
        SELECT item_id, SUM(clicks) AS total_clicks
        FROM ad_sales_metrics
        GROUP BY item_id
        ORDER BY total_clicks DESC
        LIMIT 1;
        """

    return None  # No fallback if not matched
