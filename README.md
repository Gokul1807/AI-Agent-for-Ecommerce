# AI-Agent-for-Ecommerce

Built a FastAPI app that uses Google Gemini to convert natural language questions into SQL queriesfor SQLite datasets to analyzing an organization’s sales data, returning real-time insights withpandas processing and Matplotlib visualizations for one dataset about their sales

Details:
E-Commerce AI Data Query & Visualization Assistant
Developed an AI-powered FastAPI application that converts natural language questions into optimized SQLite queries using Google Gemini 1.5 Flash.
Designed and integrated RESTful APIs for querying e-commerce datasets and returning insights in JSON format with dynamic Matplotlib visualizations.
Implemented data processing pipelines using pandas for aggregation, filtering, and metric calculations (CPC, impressions, sales trends).
Automated SQL generation for multiple datasets (total_sales_metrics, ad_sales_metrics, eligibility_table) with LLM prompt engineering.
Deployed backend with Uvicorn, ensuring efficient request handling and integration of environment-based API key management via python-dotenv.
Tech Stack: Python, FastAPI, SQLite, pandas, Matplotlib, Google Generative AI, Uvicorn, dotenv
