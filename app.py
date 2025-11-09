import os
import json
from datetime import datetime, timedelta
import streamlit as st

# -----------------------------
# Basic Setup
# -----------------------------
st.set_page_config(page_title="Mira — Nonprofit Grant Scout", page_icon="🔎", layout="wide")
DATA_ROOT = "data"

def ensure_dirs():
    os.makedirs(DATA_ROOT, exist_ok=True)
    os.makedirs(os.path.join(DATA_ROOT, "clients"), exist_ok=True)
    os.makedirs(os.path.join(DATA_ROOT, "briefs"), exist_ok=True)
ensure_dirs()

# -----------------------------
# Utility Functions
# -----------------------------
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

# -----------------------------
# Mock AI & Search Logic
# -----------------------------
def summarize_rfp_to_brief(org_profile):
    """Mock function to simulate grant discovery results."""
    return [
        {
            "title": "Youth Wellness Initiative",
            "funder": "Blue Cross Blue Shield Foundation",
            "deadline": (datetime.utcnow() + timedelta(days=40)).strftime("%Y-%m-%d"),
            "amount_min": 10000,
            "amount_max": 50000,
            "geography": ["AL", "Madison County"],
            "program_area": ["youth", "mental health", "sports"],
            "eligibility": ["501c3", "US-based"],
            "why_match": f"This grant supports youth wellness programs, aligning perfectly with {org_profile.get('org_name','your organization')}.",
            "requirements": ["990", "Board List", "Budget", "LOI"],
            "links": {"guidelines": "https://example.org/guidelines", "apply": "https://example.org/apply"}
        },
        {
            "title": "Community Sports and Wellness Fund",
            "funder": "Community Foundation of Huntsville",
            "deadline": (datetime.utcnow() + timedelta(days=20)).strftime("%Y-%m-%d"),
            "amount_min": 5000,
            "amount_max": 25000,
            "geography": ["AL"],
            "program_area": ["youth", "sports", "community"],
            "eligibility": ["501c3", "AL-based"],
            "why_match": f"Strong fit with your youth sports and mentoring programs.",
            "requirements": ["990", "Budget", "Program Summary"],
            "links": {"guidelines": "https://cfhsv.org/guidelines", "apply": "https://cfhsv.org/apply"}
        }
    ]

def compute_fit_score(brief, org_profile):
    """Simple scoring logic placeholder."""
    elig = 1.0 if "501c3" in brief.get("eligibility", []) else 0.0
    geo = 1.0 if any(g in org_profile.get("geography", []) for g in brief.get("geography", [])) else 0.5
    time_bonus = 0.8
    score = round(40 * elig + 30 * geo + 30 * time_bonus, 2)
    return score

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("🤖 Mira")
    st.caption("Your AI-powered Grant Scout for Nonprofits.")
    client_id = st.text_input("Client ID (ex: hoopswood)", value="demo_client")
    if st.button("Create Workspace"):
        os.makedirs(os.path.join(DATA_ROOT, "clients", client_id), e
