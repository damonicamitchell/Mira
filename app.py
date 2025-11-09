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
    """Simple scoring placeholder. Swap with real embeddings and rules."""
    elig = 1.0 if "501c3" in brief.get("eligibility", []) else 0.0
    geo = 1.0 if any(g in org_profile.get("geography", []) for g in brief.get("geography", [])) else 0.5
    time_bonus = 0.8  # example constant for now
    # weights: elig 40, geo 30, time 30
    score = round(40 * elig + 30 * geo + 30 * time_bonus, 2)
    return score

# ------------------------------------
# Sidebar
# ------------------------------------
with st.sidebar:
    st.title("Mira")
    st.caption("Your grant discovery assistant")
    client_id = st.text_input("Client ID (example: hoopswood)", value="demo_client")
    if st.button("Create workspace"):
        os.makedirs(os.path.join(DATA_ROOT, "clients", client_id), exist_ok=True)
        st.success(f"Workspace ready for {client_id}")

# ------------------------------------
# App title
# ------------------------------------
st.title("Mira - Nonprofit Grant Scout")
st.write("Mira helps nonprofits find funding opportunities that match their mission and goals.")

tabs = st.tabs(["Client Profile", "Discover Grants", "Saved Briefs", "Calendar"])

# ------------------------------------
# 1. Client Profile
# ------------------------------------
with tabs[0]:
    st.subheader("Organization profile")

    profile_path = os.path.join(DATA_ROOT, "clients", client_id, "profile.json")
    profile = load_json(profile_path, default={
        "org_name": "",
        "mission": "",
        "geography": [],
        "populations_served": [],
        "keywords": [],
        "annual_budget": ""
    })

    profile["org_name"] = st.text_input("Organization name", value=profile.get("org_name", ""))
    profile["mission"] = st.text_area("Mission statement", value=profile.get("mission", ""), height=120)
    profile["geography"] = st.multiselect(
        "Service areas",
        ["AL", "TN", "GA", "WI", "National", "Madison County", "Limestone County"],
        default=profile.get("geography", [])
    )
    profile["populations_served"] = st.multiselect(
        "Populations served",
        ["youth", "adults", "families", "students", "seniors", "veterans", "homeless"],
        default=profile.get("populations_served", [])
    )
    profile["keywords"] = st.multiselect(
        "Focus keywords",
        ["sports", "mental health", "STEM", "arts", "nutrition", "mentoring", "housing", "workforce"],
        default=profile.get("keywords", [])
    )
    profile["annual_budget"] = st.text_input("Annual budget (USD)", value=profile.get("annual_budget", ""))

    if st.button("Save profile"):
        save_json(profile_path, profile)
        st.success("Profile saved")

# ------------------------------------
# 2. Discover Grants
# ------------------------------------
with tabs[1]:
    st.subheader("Discover grants")
    st.write("Mira scans opportunities and ranks them for fit.")

    query = st.text_input("Refine your search (optional)", "youth mental health Alabama")
    if st.button("Find grants"):
        # require a saved profile
        if not load_json(profile_path, default=None) or not profile.get("org_name"):
            st.warning("Please complete and save the organization profile first.")
        else:
            results = mock_discover_results(profile)
            for res in results:
                res["score"] = compute_fit_score(res, profile)

            results.sort(key=lambda x: x["score"], reverse=True)

            for res in results:
                key_base = f"{res['title']}-{res['funder']}"
                with st.expander(f"{res['title']} - {res['funder']}  |  Score: {res['score']}"):
                    col1, col2 = st.columns([2, 2])
                    with col1:
                        st.write(f"**Deadline:** {res['deadline']}")
                        st.write(f"**Amount:** ${res['amount_min']:,} to ${res['amount_max']:,}")
                        st.write(f"**Geography:** {', '.join(res.get('geography', []))}")
                        st.write(f"**Areas:** {', '.join(res.get('program_area', []))}")
                    with col2:
                        st.write("**Why it matches**")
                        st.write(res.get("why_match", ""))
                        st.write("**Requirements**")
                        st.write(", ".join(res.get("requirements", [])))

                    st.markdown(f"[Guidelines]({res['links']['guidelines']})  |  [Apply]({res['links']['apply']})")

                    if st.button(f"Save brief: {res['title']}", key=f"save-{key_base}"):
                        brief_id = short_id("brief")
                        brief_dir = os.path.join(DATA_ROOT, "clients", client_id, "briefs")
                        os.makedirs(brief_dir, exist_ok=True)
                        brief_path = os.path.join(brief_dir, f"{brief_id}.json")
                        save_json(brief_path, {"brief_id": brief_id, "client_id": client_id, "opportunity": res})
                        st.success(f"Saved as brief {brief_id}")

# ------------------------------------
# 3. Saved Briefs
# ------------------------------------
with tabs[2]:
    st.subheader("Saved briefs")
    briefs_dir = os.path.join(DATA_ROOT, "clients", client_id, "briefs")
    if not os.path.isdir(briefs_dir) or not os.listdir(briefs_dir):
        st.info("No briefs saved yet")
    else:
        for fname in sorted(os.listdir(briefs_dir)):
            bpath = os.path.join(briefs_dir, fname)
            brief = load_json(bpath, {})
            opp = brief.get("opportunity", {})
            title = opp.get("title", "Untitled")
            funder = opp.get("funder", "Unknown")
            with st.expander(f"{title} - {funder}"):
                st.write(f"**Brief ID:** {brief.get('brief_id')}")
                st.write(f"**Deadline:** {opp.get('deadline', 'TBD')}")
                st.write(f"**Why match:** {opp.get('why_match', '')}")
                st.write(f"**Requirements:** {', '.join(opp.get('requirements', []))}")
                st.markdown(f"[Guidelines]({opp.get('links', {}).get('guidelines', '#')})  |  [Apply]({opp.get('links', {}).get('apply', '#')})")

# ------------------------------------
# 4. Calendar
# ------------------------------------
with tabs[3]:
    st.subheader("Upcoming deadlines")
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
            st.write(f"**{d.date()}** - {title} | {funder}")
    else:
        st.info("No upcoming deadlines saved yet")

