# app/main.py

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.db_handler import execute_query
from app.llm_handler import convert_question_to_sql, get_fallback_sql
from app.visualizer import generate_sales_bar_chart
import time

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(req: QuestionRequest):
    try:
        question = req.question
        sql_query = convert_question_to_sql(question)
        print(f"Generated SQL: {sql_query}")

        result = execute_query(sql_query)

        # Round float values
        if "rows" in result and isinstance(result["rows"], list):
            result["rows"] = [
                [round(val, 2) if isinstance(val, float) else val for val in row]
                for row in result["rows"]
            ]

        # Fallback if no results
        if not result.get("rows"):
            print("No results found. Trying fallback...")
            fallback_query = get_fallback_sql(question)
            if fallback_query:
                print("Fallback SQL:", fallback_query)
                result = execute_query(fallback_query)
                if "rows" in result and isinstance(result["rows"], list):
                    result["rows"] = [
                        [round(val, 2) if isinstance(val, float) else val for val in row]
                        for row in result["rows"]
                    ]
                sql_query += "\n-- Fallback applied"

        response_data = {
            "question": question,
            "sql_query": sql_query,
            "response": result
        }

        # ✅ Safe chart generation if "sales" is mentioned
        if "sales" in question.lower() and result.get("columns") and result.get("rows"):
            try:
                print("Returned columns:", result["columns"])
                chart_base64 = generate_sales_bar_chart(result["columns"], result["rows"])
                response_data["chart"] = f"data:image/png;base64,{chart_base64}"
            except Exception as chart_error:
                print("Chart generation error:", chart_error)

        return response_data

    except Exception as e:
        return {"error": str(e)}

@app.post("/stream")
def stream_response(req: QuestionRequest):
    question = req.question
    sql_query = convert_question_to_sql(question)
    print(f"Generated SQL: {sql_query}")
    result = execute_query(sql_query)

    if "rows" in result and isinstance(result["rows"], list):
        result["rows"] = [
            [round(val, 2) if isinstance(val, float) else val for val in row]
            for row in result["rows"]
        ]

    message = f"Question: {question}\nSQL: {sql_query}\nAnswer:\n{result}"

    def event_generator():
        for char in message:
            yield f"data: {char}\n\n"
            time.sleep(0.02)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
