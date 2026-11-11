import csv
import os

# Relative path so it works on any computer (required by project checklist)
FILE_PATH = os.path.join("data", "sales_records.csv")
HEADERS = ["id", "item_name", "category", "cost_price", "selling_price", "quantity_sold", "revenue", "profit"]


def ensure_data_file():
    """Creates the data folder and CSV with headers if missing (Error Handling)."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)


def load_all_sales() -> list[dict]:
    """Reads all records from the CSV file into a list of dictionaries."""
    ensure_data_file()
    records = []
    try:
        with open(FILE_PATH, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["id"] = int(row["id"])
                row["cost_price"] = float(row["cost_price"])
                row["selling_price"] = float(row["selling_price"])
                row["quantity_sold"] = int(row["quantity_sold"])
                row["revenue"] = float(row["revenue"])
                row["profit"] = float(row["profit"])
                records.append(row)
    except (ValueError, KeyError):
        # Prevents crash if a row in CSV is malformed
        return []
    return records


def add_sale_record(item_name: str, category: str, cost_price: float, selling_price: float, quantity_sold: int) -> dict:
    """Calculates revenue & profit, then saves the new record to CSV."""
    records = load_all_sales()
    new_id = max((r["id"] for r in records), default=0) + 1

    revenue = round(selling_price * quantity_sold, 2)
    profit = round((selling_price - cost_price) * quantity_sold, 2)

    new_record = {
        "id": new_id,
        "item_name": item_name.strip(),
        "category": category.strip().title(),
        "cost_price": round(cost_price, 2),
        "selling_price": round(selling_price, 2),
        "quantity_sold": quantity_sold,
        "revenue": revenue,
        "profit": profit,
    }

    with open(FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writerow(new_record)

    return new_record


def compute_summary() -> dict:
    """Calculates total revenue, profit, margin %, and category share."""
    records = load_all_sales()
    if not records:
        return {"message": "No sales records available yet."}

    total_revenue = 0.0
    total_profit = 0.0
    category_revenue = {}

    for r in records:
        total_revenue += r["revenue"]
        total_profit += r["profit"]
        cat = r["category"]
        category_revenue[cat] = round(category_revenue.get(cat, 0.0) + r["revenue"], 2)

    margin_pct = round((total_profit / total_revenue) * 100, 2) if total_revenue > 0 else 0.0
    category_share = {
        cat: f"{round((rev / total_revenue) * 100, 1)}%"
        for cat, rev in category_revenue.items()
    }

    return {
        "total_transactions": len(records),
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2),
        "overall_profit_margin_pct": margin_pct,
        "revenue_by_category": category_revenue,
        "category_share_pct": category_share,
    }


def get_performance_alerts(min_margin_pct: float = 15.0) -> dict:
    """Finds the top profit-generating item and flags low-margin or loss-making items."""
    records = load_all_sales()
    if not records:
        return {"message": "No sales records available yet."}

    top_item = max(records, key=lambda r: r["profit"])
    low_margin_alerts = []

    for r in records:
        item_margin = (r["profit"] / r["revenue"]) * 100 if r["revenue"] > 0 else 0.0
        if item_margin < min_margin_pct:
            status = "LOSS" if r["profit"] < 0 else "LOW MARGIN"
            low_margin_alerts.append({
                "id": r["id"],
                "item_name": r["item_name"],
                "category": r["category"],
                "profit": r["profit"],
                "margin_pct": round(item_margin, 1),
                "alert": status,
            })

    return {
        "top_performing_sale": {
            "item_name": top_item["item_name"],
            "category": top_item["category"],
            "profit": top_item["profit"],
        },
        "threshold_checked_pct": min_margin_pct,
        "flagged_items_count": len(low_margin_alerts),
        "flagged_items": low_margin_alerts,
    }
