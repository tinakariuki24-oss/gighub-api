# GigHub Freelance Gigs API

**Student Admission Number:** C027-01-0877/2024

## Project Description
This is a FastAPI-based backend application developed for GigHub, a Nairobi-based freelancing platform connecting clients and freelancers. The API allows users to create, view, search, filter, update, and delete freelance gig listings using a local, in-memory dataset configured dynamically according to student admission constraints.

## Dataset Parameters
- **Total Initial Gigs:** 12
- **Assigned Categories:** Marketing, Data, Consulting
- **Currency Type:** KES

## Setup Instructions
1. Install dependencies: `uv pip install fastapi uvicorn pydantic`
2. Run the application: `uv run uvicorn main:app --reload`
3. Access API Documentation: Open `http://127.0.0.1:8000/docs` in your browser.