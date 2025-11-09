import streamlit as st

# ------------------------------------
# App Setup
# ------------------------------------
st.set_page_config(page_title="Meet Mira - Your Grant Scout", page_icon="🔎", layout="centered")

# ------------------------------------
# Hero Section
# ------------------------------------
st.title("🤖 Meet Mira")
st.subheader("Your Nonprofit Grant Scout & AI Assistant")

st.markdown("""
Mira helps nonprofits **find funding faster** and **stay organized** — 
without needing a grant expert on staff.  

She’s friendly, resourceful, and always ready to help you win more grants.
""")

# ------------------------------------
# Mira's Mission
# ------------------------------------
st.header("🌟 Mira’s Mission")
st.markdown("""
To help **every nonprofit, big or small**, access the funding they deserve.  

Mira searches, sorts, and explains grants in plain language — so you can focus on your impact, not the paperwork.
""")

# ------------------------------------
# Mira's Responsibilities (What She Does)
# ------------------------------------
st.header("🧩 What Mira Can Do")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ✅ **Find Grants that Fit You**  
    Mira searches the web and grant databases to match funding opportunities with your mission.  

    ✅ **Explain Grants Simply**  
    She breaks down requirements, deadlines, and next steps — no jargon.  

    ✅ **Send Reminders**  
    Mira tracks deadlines so you never miss out.  
    """)

with col2:
    st.markdown("""
    ✅ **Organize Your Grant Info**  
    Mira keeps all your grant briefs in one simple dashboard.  

    ✅ **Learn Your Preferences**  
    The more you use her, the better she gets at finding perfect matches.  

    ✅ **Collaborate with Your Team**  
    Everyone can log in and see what’s due next.
    """)

# ------------------------------------
# Mira's Toolbox
# ------------------------------------
st.header("🧰 Mira’s Toolbox")
st.markdown("""
Mira uses smart tools behind the scenes to do her job:
- 🔍 **Grant Finder** — searches government, foundation, and corporate grants  
- 🧠 **AI Assistant** — reads and summarizes RFPs  
- 🗂️ **Grant Brief Builder** — creates easy-to-read summaries  
- ⏰ **Deadline Tracker** — keeps your team on time  
- 📬 **Smart Alerts** — sends reminders when new grants match your mission  
""")

# ------------------------------------
# Testimonials / Personality
# ------------------------------------
st.header("💬 What People Say About Mira")
st.info("""
“Mira explains grants like a real teammate — clear, patient, and helpful.”  
— A nonprofit founder in Alabama
""")

# ------------------------------------
# Call to Action
# ------------------------------------
st.header("🚀 Ready to Work with Mira?")
st.write("Sign up below to be the first to try Mira when she launches!")

with st.form("signup_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Email Address")
    org = st.text_input("Nonprofit or Organization Name")
    submitted = st.form_submit_button("💌 Join the Waitlist")

    if submitted:
        st.success(f"Thanks {name or 'friend'}! Mira will reach out to you soon at {email}.")

# ------------------------------------
# Footer
# ------------------------------------
st.markdown("---")
st.caption("Created by DaMonica Mitchell | Mira AI © 2025 | Helping Nonprofits See Funding Clearly 💙")
