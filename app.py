import os
import json
from datetime import datetime, timedelta
import streamlit as st

# ------------------------------------
# Basic setup
# ------------------------------------
st.set_page_config(page_title="Mira - Nonprofit Grant Scout", page_icon="🔎", layout="wide")

DATA_ROOT = "data"

def ensure_dirs():
    os.makedirs(DATA_ROOT, exist_ok=True)
    os.makedirs(os.path.join(DATA_ROOT, "clients"), exist_ok=True)

ensure_dirs()

# ------------------------------------
# Utilities
# ------------------------------------
def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path, default=None):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def short_id(prefix):
    return f"{prefix}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

# ------------------------------------
# Mock search and scoring
# Replace these with your real connectors and LLM logic
# ------------------------------------
def mock_discover_results(org_profile):
    """Return example results for demonstration."""
    return [
        {
            "title": "Youth Wellness Initiative",
            "funder": "Blue Cross Blue Shield of Alabama Foundation",
            "deadline": (datetime.utcnow() + timedelta(days=40)).strftime("%Y-%m-%d"),
            "amount_min": 10000,
            "amount_max": 50000,
            "geography": ["AL", "Madison County"],
            "program_area": ["youth", "mental health", "sports"],
            "eligibility": ["501c3", "US-based"],
            "why_match": f"This funder prioritizes youth wellness in Alabama. Strong alignment with {org_profile.get('org_name','your organization')}.",
            "requir
