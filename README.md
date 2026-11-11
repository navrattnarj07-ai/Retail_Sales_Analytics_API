# Retail Sales & Profit Margin Analytics API

**Programme:** First-Year B.Sc. (Data Science & Business Analytics)  
**Subject:** Python Programming  
**Framework:** FastAPI  

## Project Overview
A lightweight RESTful analytics API built with Python and FastAPI that helps small retail and campus canteen operators record daily sales transactions, persist records locally in CSV format, and compute real-time business KPIs including total revenue, net profit, profit margins, category revenue share, and low-margin/loss alerts.

## Features
1. **Record New Sale (`POST /sales`):** Validates input data, calculates line-item revenue and profit, and appends the transaction to `data/sales_records.csv`.
2. **Query & Filter Sales (`GET /sales`):** Retrieves all stored transactions or filters records by product category.
3. **Business Analytics Summary (`GET /analytics/summary`):** Computes total transactions, total revenue, total profit, overall profit margin percentage, and category-wise revenue share.
4. **Performance & Margin Alerts (`GET /analytics/alerts`):** Identifies the highest profit-generating transaction and flags items falling below a configurable profit margin threshold (default `15%`).

## Folder Structure
```text
Retail_Sales_Analytics_API/
├── main.py                  # FastAPI application, Pydantic validation & endpoints
├── analytics.py             # Core Python business logic, KPI calculations & CSV I/O
├── data/
│   └── sales_records.csv    # Persistent CSV dataset
├── requirements.txt         # Project dependencies
├── .gitignore               # Excluded environment/cache files
└── README.md                # Setup and usage guide
