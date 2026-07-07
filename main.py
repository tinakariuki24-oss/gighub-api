from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="GigHub API - C027-01-0877/2024")

class CategoryEnum(str, Enum):
    MARKETING = "Marketing"
    DATA = "Data"
    CONSULTING = "Consulting"

class StatusEnum(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    CLOSED = "Closed"

class GigCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=20, max_length=500)
    category: CategoryEnum
    budget: float = Field(..., gt=0)
    client_name: str = Field(..., min_length=2, max_length=50)

class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0)
    status: Optional[StatusEnum] = None

class Gig(BaseModel):
    id: int
    title: str
    description: str
    category: CategoryEnum
    budget: float
    currency: str = "KES"
    status: StatusEnum
    client_name: str

gigs_db: List[Gig] = [
    Gig(id=1, title="Social Media Campaign", description="Launch a comprehensive Facebook and Instagram campaign for a local retail brand.", category=CategoryEnum.MARKETING, budget=45000.0, status=StatusEnum.OPEN, client_name= "John Kamau"),
    Gig(id=2, title="Data Cleaning Pipeline", description="Build an automated Python script to scrub messy CSV transaction files weekly.", category=CategoryEnum.DATA, budget=30000.0, status=StatusEnum.OPEN, client_name="Alice Mwangi"),
    Gig(id=3, title="Financial Strategy Review", description="Analyze corporate cashflow statements and recommend structural optimization models.", category=CategoryEnum.CONSULTING, budget=85000.0, status=StatusEnum.IN_PROGRESS, client_name="David Otieno"),
    Gig(id=4, title="SEO Optimization Audit", description="Perform deep-dive keyword research and competitor tracking for an e-commerce platform.", category=CategoryEnum.MARKETING, budget=25000.0, status=StatusEnum.OPEN, client_name="Grace Wambui"),
    Gig(id=5, title="PowerBI Sales Dashboard", description="Design interactive executive visualizations connected directly to an SQL Server instance.", category=CategoryEnum.DATA, budget=60000.0, status=StatusEnum.OPEN, client_name="Peter Ochieng"),
    Gig(id=6, title="HR Compliance Advisory", description="Evaluate employment contracts against current Kenyan labor laws and guidelines.", category=CategoryEnum.CONSULTING, budget=40000.0, status=StatusEnum.CLOSED, client_name="Mary Atieno"),
    Gig(id=7, title="Google Ads Optimization", description="Audit existing search ad copy and restructure bidding strategies to reduce spend.", category=CategoryEnum.MARKETING, budget=20000.0, status=StatusEnum.OPEN, client_name="Kevin Kiprop"),
    Gig(id=8, title="Predictive Churn Model", description="Train a machine learning system to flag subscribers likely to cancel active plans.", category=CategoryEnum.DATA, budget=95000.0, status=StatusEnum.OPEN, client_name="Sarah Cherono"),
    Gig(id=9, title="Supply Chain Assessment", description="Audit logistical bottlenecks within an agricultural distribution center in Nairobi.", category=CategoryEnum.CONSULTING, budget=110000.0, status=StatusEnum.IN_PROGRESS, client_name="James Njoroge"),
    Gig(id=10, title="Email Copywriting Setup", description="Draft a cold outreach sequence containing exactly five high-converting follow-ups.", category=CategoryEnum.MARKETING, budget=15000.0, status=StatusEnum.OPEN, client_name="Lucy Wanjiku"),
    Gig(id=11, title="Customer Survey Analysis", description="Process textual feedback arrays using natural language parsing to track sentiment.", category=CategoryEnum.DATA, budget=35000.0, status=StatusEnum.OPEN, client_name="Brian Ndwiga"),
    Gig(id=12, title="Business Process Mapping", description="Document existing operational workflows to eliminate redundant cross-department loops.", category=CategoryEnum.CONSULTING, budget=70000.0, status=StatusEnum.OPEN, client_name="Faith Mutua")
]

id_counter = 13

@app.get("/gigs", response_model=List[Gig])
def get_gigs(
    category: Optional[CategoryEnum] = None,
    min_budget: Optional[float] = Query(None, gt=0),
    max_budget: Optional[float] = Query(None, gt=0)
):
    filtered = gigs_db
    if category:
        filtered = [g for g in filtered if g.category == category]
    if min_budget is not None:
        filtered = [g for g in filtered if g.budget >= min_budget]
    if max_budget is not None:
        filtered = [g for g in filtered if g.budget <= max_budget]
    return filtered

@app.get("/gigs/search", response_model=List[Gig])
def search_gigs(q: str = Query(..., min_length=1)):
    return [g for g in gigs_db if q.lower() in g.title.lower()]

@app.get("/gigs/{gig_id}", response_model=Gig)
def get_gig(gig_id: int):
    for gig in gigs_db:
        if gig.id == gig_id:
            return gig
    raise HTTPException(status_code=404, detail="Gig not found")

@app.post("/gigs", response_model=Gig, status_code=status.HTTP_201_CREATED)
def create_gig(gig_in: GigCreate):
    global id_counter
    new_gig = Gig(
        id=id_counter,
        title=gig_in.title,
        description=gig_in.description,
        category=gig_in.category,
        budget=gig_in.budget,
        currency="KES",
        status=StatusEnum.OPEN,
        client_name=gig_in.client_name
    )
    gigs_db.append(new_gig)
    id_counter += 1
    return new_gig

@app.put("/gigs/{gig_id}", response_model=Gig)
def update_gig(gig_id: int, gig_in: GigUpdate):
    for gig in gigs_db:
        if gig.id == gig_id:
            if gig_in.budget is not None:
                gig.budget = gig_in.budget
            if gig_in.status is not None:
                gig.status = gig_in.status
            return gig
    raise HTTPException(status_code=404, detail="Gig not found")

@app.delete("/gigs/{gig_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gig(gig_id: int):
    for index, gig in enumerate(gigs_db):
        if gig.id == gig_id:
            gigs_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Gig not found")