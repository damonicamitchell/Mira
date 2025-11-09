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
# Utility functions
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
# Mock grant search & scoring logic
# ------------------------------------
def mock_discover_results(org_profile):
    """Returns example grant opportunities for demonstration."""
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
            "why_match": "Good fit for youth sports and mentoring programs in North Alabama.",
            "requirements": ["990", "Budget", "Program Summary"],
            "links": {"guidelines": "https://cfhsv.org/guidelines", "apply": "https://cfhsv.org/apply"}
        }
    ]

def compute_fit_score(brief, org_profile):
    """Simple placeholder scoring function."""
    elig = 1.0 if "501c3" in brief.get("eligibility", []) else 0.0
    geo = 1.0 if any(g in org_profile.get("geography", []) for g in brief.get("geography", [])) else 0.5
    time_bonus = 0.8
    score = round(40 * elig + 30 * geo + 30 * time_bonus, 2)
    return score

# ------------------------------------
# Sidebar
# ------------------------------------
with st.sidebar:
    st.title("Mira")
    st.caption("Your AI Grant Scout for Nonprofits")
    client_id = st.text_input("Client ID (example: hoopswood)", value="demo_client")
    if st.button("Create workspace"):
        os.makedirs(os.path.join(DATA_ROOT, "clients", client_id), exist_ok=True)
        st.success(f"Workspace ready for {client_id}")

# ------------------------------------
# Main App Tabs
# ------------------------------------
st.title("Mira - Nonprofit Grant Scout")

tabs = st.tabs(["About Mira", "Client Profile", "Discover Grants", "Saved Briefs", "Calendar"])

# ------------------------------------
# Tab 1: About Mira
# ------------------------------------
with tabs[0]:
    st.subheader("Meet Mira — Your Nonprofit Grant Scout")
    st.write("""
**Mira** helps nonprofits *see* funding opportunities clearly.  
She continuously discovers and ranks grants that match your mission, location, and goals, then turns them into
concise, actionable briefs you can act on quickly.

**Mira’s personality:** empathetic, insightful, resourceful, and encouraging.

**What Mira does:**
- Ingests your organization’s profile once (mission, geography, focus areas)
- Scans curated grant sources
- Scores eligibility and mission-fit transparently
- Creates easy-to-read grant briefs
- Keeps a rolling deadline calendar
    """)
    st.info("💡 Tip: Mira’s data is sample-based right now. You can connect real APIs and AI models later.")

# ------------------------------------
# Tab 2: Client Profile
# ------------------------------------
with tabs[1]:
    st.subheader("Organization Profile")

    profile_path = os.path.join(DATA_ROOT, "clients", client_id, "profile.json")
    profile = load_json(profile_path, default={
        "org_name": "",
        "mission": "",
        "geography": [],
        "populations_served": [],
        "keywords": [],
        "annual_budget": ""
    })

    profile["org_name"] = st.text_input("Organization Name", value=profile.get("org_name", ""))
    profile["mission"] = st.text_area("Mission Statement", value=profile.get("mission", ""), height=120)
    profile["geography"] = st.multiselect(
        "Service Areas",
        ["AL", "TN", "GA", "WI", "National", "Madison County", "Limestone County"],
        default=profile.get("geography", [])
    )
    profile["populations_served"] = st.multiselect(
        "Populations Served",
        ["youth", "adults", "families", "students", "seniors", "veterans", "homeless"],
        default=profile.get("populations_served", [])
    )
    profile["keywords"] = st.multiselect(
        "Focus Keywords",
        ["sports", "mental health", "STEM", "arts", "nutrition", "mentoring", "housing", "workforce"],
        default=profile.get("keywords", [])
    )
    profile["annual_budget"] = st.text_input("Annual Budget (USD)", value=profile.get("annual_budget", ""))

    if st.button("💾 Save Profile"):
        save_json(profile_path, profile)
        st.success("Profile saved successfully!")

# ------------------------------------
# Tab 3: Discover Grants
# ------------------------------------
with tabs[2]:
    st.subheader("Discover Grants")
    st.write("Mira scans opportunities and ranks them for fit with your mission.")

    query = st.text_input("Refine your search (optional)", "youth mental health Alabama")

    if st.button("🔎 Find Grants"):
        if not profile.get("org_name"):
            st.warning("Please complete and save your organization profile first.")
        else:
            results = mock_discover_results(profile)
            for res in results:
                res["score"] = compute_fit_score(res, profile)

            results.sort(key=lambda x: x["score"], reverse=True)

            for res in results:
                with st.expander(f"{res['title']} — {res['funder']} | Score: {res['score']}"):
                    col1, col2 = st.columns([2, 2])
                    with col1:
                        st.write(f"**Deadline:** {res['deadline']}")
                        st.write(f"**Amount:** ${res['amount_min']:,} – ${res['amount_max']:,}")
                        st.write(f"**Geography:** {', '.join(res.get('geography', []))}")
                        st.write(f"**Areas:** {', '.join(res.get('program_area', []))}")
                    with col2:
                        st.write("**Why it matches**")
                        st.write(res.get("why_match", ""))
                        st.write("**Requirements**")
                        st.write(", ".join(res.get("requirements", [])))
                        st.markdown(f"[Guidelines]({res['links']['guidelines']}) | [Apply]({res['links']['apply']})")

                    if st.button(f"💾 Save Brief: {res['title']}", key=res['title']):
                        brief_id = short_id("brief")
                        brief_dir = os.path.join(DATA_ROOT, "clients", client_id, "briefs")
                        os.makedirs(brief_dir, exist_ok=True)
                        brief_path = os.path.join(brief_dir, f"{brief_id}.json")
                        save_json(brief_path, {"brief_id": brief_id, "client_id": client_id, "opportunity": res})
                        st.success(f"Saved {res['title']} as brief {brief_id}")

# ------------------------------------
# Tab 4: Saved Briefs
# ------------------------------------
with tabs[3]:
    st.subheader("Saved Briefs")

    briefs_dir = os.path.join(DATA_ROOT, "clients", client_id, "briefs")
    if not os.path.isdir(briefs_dir) or not os.listdir(briefs_dir):
        st.info("No briefs saved yet.")
    else:
        for fname in sorted(os.listdir(briefs_dir)):
            path = os.path.join(briefs_dir, fname)
            brief = load_json(path, {})
            opp = brief.get("opportunity", {})
            with st.expander(f"{opp.get('title', 'Untitled')} — {opp.get('funder', 'Unknown')}"):
                st.write(f"**Deadline:** {opp.get('deadline', 'TBD')}")
                st.write(f"**Why Match:** {opp.get('why_match', '')}")
                st.write(f"**Requirements:** {', '.join(opp.get('requirements', []))}")
                st.markdown(f"[Guidelines]({opp.get('links', {}).get('guidelines', '#')}) | [Apply]({opp.get('links', {}).get('apply', '#')})")

# ------------------------------------
# Tab 5: Calendar
# ------------------------------------
with tabs[4]:
    st.subheader("Upcoming Deadlines")
    deadlines = []
    briefs_dir = os.path.join(DATA_ROOT, "clients", client_id, "briefs")
    if os.path.isdir(briefs_dir):
        for fname in os.listdir(briefs_dir):
            brief = load_json(os.path.join(briefs_dir, fname), {})
            opp = brief.get("opportunity", {})
            try:
                d = datetime.strptime(opp.get("deadline", "2099-12-31"), "%Y-%m-%d")
                deadlines.append((d, opp.get("title", "Untitled"), opp.get("funder", "")))
            except Exception:
                pass

    if deadlines:
        deadlines.sort()
        for d, title, funder in deadlines:
            st.write(f"**{d.date()}** — {title} | {funder}")
    else:
        st.info("No upcoming deadlines yet.")
