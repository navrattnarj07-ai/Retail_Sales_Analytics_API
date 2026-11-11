from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
import analytics

app = FastAPI(
    title="Retail Sales & Profit Margin Analytics API",
    description="First-Year B.Sc. Data Science & Business Analytics Python Project",
    version="1.0.0",
)


class SaleInput(BaseModel):
    item_name: str = Field(..., examples=["Cold Coffee"])
    category: str = Field(..., examples=["Beverages"])
    cost_price: float = Field(..., gt=0, examples=[30.0])
    selling_price: float = Field(..., gt=0, examples=[65.0])
    quantity_sold: int = Field(..., gt=0, examples=[4])

    @field_validator("item_name", "category")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Field cannot be blank or whitespace only.")
        return value


@app.get("/")
def home():
    return {
        "project": "Retail Sales & Profit Margin Analytics API",
        "status": "online",
        "interactive_docs": "Open http://127.0.0.1:8000/docs in your browser",
    }


# Feature 1: Add a new sale record
@app.post("/sales", status_code=201)
def create_sale(sale: SaleInput):
    record = analytics.add_sale_record(
        item_name=sale.item_name,
        category=sale.category,
        cost_price=sale.cost_price,
        selling_price=sale.selling_price,
        quantity_sold=sale.quantity_sold,
    )
    return {"message": "Sale recorded successfully", "data": record}


# Feature 2: View all sales or filter by category
@app.get("/sales")
def get_sales(category: str | None = None):
    records = analytics.load_all_sales()
    if category:
        records = [r for r in records if r["category"].lower() == category.strip().lower()]
        if not records:
            raise HTTPException(
                status_code=404,
                detail=f"No records found for category '{category}'.",
            )
    return {"count": len(records), "records": records}


# Feature 3: Business analytics summary (revenue, profit, margin %, category share)
@app.get("/analytics/summary")
def get_analytics_summary():
    return analytics.compute_summary()


# Feature 4: Top performer & low-margin / loss alerts
@app.get("/analytics/alerts")
def get_performance_alerts(min_margin_pct: float = 15.0):
    if min_margin_pct < 0 or min_margin_pct > 100:
        raise HTTPException(
            status_code=400,
            detail="min_margin_pct must be between 0 and 100.",
        )
    return analytics.get_performance_alerts(min_margin_pct=min_margin_pct)
