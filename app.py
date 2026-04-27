# import streamlit as st
# import json
# import os
# from pathlib import Path

# # ── Page config ──────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Course Manager",
#     page_icon="🎓",
#     layout="wide",
# )

# # ── Custom CSS ────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
#     .block-container { padding-top: 1.5rem; }
#     .metric-card {
#         background: #f8f9fb;
#         border-radius: 10px;
#         padding: 1rem 1.25rem;
#         border: 1px solid #e8eaed;
#         text-align: center;
#     }
#     .metric-label { font-size: 12px; color: #6b7280; margin-bottom: 4px; }
#     .metric-value { font-size: 26px; font-weight: 600; color: #111827; }
#     .badge-published {
#         background: #d1fae5; color: #065f46;
#         padding: 2px 10px; border-radius: 20px; font-size: 12px; font-weight: 500;
#     }
#     .badge-draft {
#         background: #f3f4f6; color: #6b7280;
#         padding: 2px 10px; border-radius: 20px; font-size: 12px; font-weight: 500;
#     }
#     .badge-budget  { background:#dbeafe; color:#1e40af; padding:2px 8px; border-radius:20px; font-size:12px; }
#     .badge-standard{ background:#fef3c7; color:#92400e; padding:2px 8px; border-radius:20px; font-size:12px; }
#     .badge-premium { background:#fee2e2; color:#991b1b; padding:2px 8px; border-radius:20px; font-size:12px; }
#     div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
# </style>
# """, unsafe_allow_html=True)


# # ── Data helpers ──────────────────────────────────────────────────────────────
# DATA_FILE = Path(__file__).parent / "course.json"

# def load_data():
#     try:
#         with open(DATA_FILE, "r") as f:
#             return json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return []

# def save_data(data):
#     with open(DATA_FILE, "w") as f:
#         json.dump(data, f, indent=2)

# def price_category(price):
#     if price < 700:
#         return "Budget"
#     elif price < 1000:
#         return "Standard"
#     return "Premium"

# def validate_course(data, courses, edit_id=None):
#     errors = []
#     if data["id"] <= 0:
#         errors.append("ID must be greater than 0.")
#     existing_ids = [c["id"] for c in courses if c["id"] != edit_id]
#     if data["id"] in existing_ids:
#         errors.append(f"Course with ID {data['id']} already exists.")
#     if len(data["title"].strip()) < 2:
#         errors.append("Title must be at least 2 characters.")
#     if len(data["instructor"].strip()) < 2:
#         errors.append("Instructor must be at least 2 characters.")
#     if len(data["category"].strip()) < 2:
#         errors.append("Category must be at least 2 characters.")
#     if data["price"] <= 0:
#         errors.append("Price must be greater than 0.")
#     if data["duration_hours"] <= 0:
#         errors.append("Duration must be greater than 0.")
#     if not data["is_published"] and data["discount_percent"] is not None:
#         errors.append("Discount cannot be set for unpublished courses.")
#     return errors


# # ── Session state ─────────────────────────────────────────────────────────────
# if "courses" not in st.session_state:
#     st.session_state.courses = load_data()
# if "edit_id" not in st.session_state:
#     st.session_state.edit_id = None
# if "delete_id" not in st.session_state:
#     st.session_state.delete_id = None
# if "active_tab" not in st.session_state:
#     st.session_state.active_tab = "Browse"

# courses = st.session_state.courses


# # ── Header ────────────────────────────────────────────────────────────────────
# st.markdown("## 🎓 Course Manager")
# st.markdown("---")

# # ── Stats row ────────────────────────────────────────────────────────────────
# c1, c2, c3, c4 = st.columns(4)
# with c1:
#     st.metric("Total Courses", len(courses))
# with c2:
#     published = sum(1 for c in courses if c["is_published"])
#     st.metric("Published", published)
# with c3:
#     avg_price = round(sum(c["price"] for c in courses) / len(courses)) if courses else 0
#     st.metric("Avg Price", f"₹{avg_price:,}")
# with c4:
#     cats = len(set(c["category"] for c in courses))
#     st.metric("Categories", cats)

# st.markdown("")

# # ── Tabs ──────────────────────────────────────────────────────────────────────
# tab_browse, tab_add, tab_edit, tab_delete = st.tabs(["📋 Browse & Filter", "➕ Add Course", "✏️ Edit Course", "🗑️ Delete Course"])


# # ═══════════════════════════════════════════════════════════════════════════════
# # TAB 1 — BROWSE
# # ═══════════════════════════════════════════════════════════════════════════════
# with tab_browse:
#     st.markdown("### All Courses")

#     col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
#     with col1:
#         search = st.text_input("🔍 Search", placeholder="Title or instructor...")
#     with col2:
#         all_cats = sorted(set(c["category"] for c in courses))
#         cat_filter = st.selectbox("Category", ["All"] + all_cats)
#     with col3:
#         status_filter = st.selectbox("Status", ["All", "Published", "Draft"])
#     with col4:
#         price_filter = st.selectbox("Price Tier", ["All", "Budget (<₹700)", "Standard (₹700–999)", "Premium (₹1000+)"])

#     # Apply filters
#     filtered = courses
#     if search:
#         q = search.lower()
#         filtered = [c for c in filtered if q in c["title"].lower() or q in c["instructor"].lower()]
#     if cat_filter != "All":
#         filtered = [c for c in filtered if c["category"] == cat_filter]
#     if status_filter == "Published":
#         filtered = [c for c in filtered if c["is_published"]]
#     elif status_filter == "Draft":
#         filtered = [c for c in filtered if not c["is_published"]]
#     if price_filter == "Budget (<₹700)":
#         filtered = [c for c in filtered if c["price"] < 700]
#     elif price_filter == "Standard (₹700–999)":
#         filtered = [c for c in filtered if 700 <= c["price"] < 1000]
#     elif price_filter == "Premium (₹1000+)":
#         filtered = [c for c in filtered if c["price"] >= 1000]

#     st.caption(f"{len(filtered)} course(s) found")

#     if not filtered:
#         st.info("No courses match the filters.")
#     else:
#         # Build display table
#         import pandas as pd
#         rows = []
#         for c in filtered:
#             disc = f"{c['discount_percent']}%" if c["discount_percent"] is not None else "—"
#             rows.append({
#                 "ID": c["id"],
#                 "Title": c["title"],
#                 "Instructor": c["instructor"],
#                 "Category": c["category"].title(),
#                 "Price (₹)": f"₹{c['price']:,.0f}",
#                 "Discount": disc,
#                 "Duration (h)": c["duration_hours"],
#                 "Status": "✅ Published" if c["is_published"] else "⬜ Draft",
#                 "Tier": price_category(c["price"]),
#             })
#         df = pd.DataFrame(rows)
#         st.dataframe(df, use_container_width=True, hide_index=True)

#     # Chart section
#     st.markdown("---")
#     st.markdown("### 📊 Insights")

#     ic1, ic2 = st.columns(2)
#     import pandas as pd

#     with ic1:
#         st.markdown("**Courses by category**")
#         from collections import Counter
#         cat_counts = Counter(c["category"] for c in courses)
#         cat_df = pd.DataFrame(cat_counts.items(), columns=["Category", "Count"]).sort_values("Count", ascending=False)
#         st.bar_chart(cat_df.set_index("Category"))

#     with ic2:
#         st.markdown("**Price distribution**")
#         price_counts = {"Budget": 0, "Standard": 0, "Premium": 0}
#         for c in courses:
#             price_counts[price_category(c["price"])] += 1
#         price_df = pd.DataFrame(price_counts.items(), columns=["Tier", "Count"])
#         st.bar_chart(price_df.set_index("Tier"))


# # ═══════════════════════════════════════════════════════════════════════════════
# # TAB 2 — ADD COURSE
# # ═══════════════════════════════════════════════════════════════════════════════
# with tab_add:
#     st.markdown("### Add New Course")

#     with st.form("add_form"):
#         a1, a2 = st.columns(2)
#         with a1:
#             new_id = st.number_input("ID", min_value=1, step=1, value=max((c["id"] for c in courses), default=0) + 1)
#             new_title = st.text_input("Title")
#             new_instructor = st.text_input("Instructor")
#             new_category = st.text_input("Category")
#         with a2:
#             new_price = st.number_input("Price (₹)", min_value=0.01, step=1.0, value=499.0)
#             new_duration = st.number_input("Duration (hours)", min_value=0.5, step=0.5, value=10.0)
#             new_published = st.checkbox("Published")
#             new_discount = st.number_input("Discount %", min_value=0.0, max_value=100.0, step=0.1, value=0.0,
#                                            help="Only for published courses. Leave 0 for no discount.")

#         submitted = st.form_submit_button("➕ Add Course", use_container_width=True, type="primary")
#         if submitted:
#             discount_val = new_discount if new_discount > 0 else None
#             new_course = {
#                 "id": int(new_id),
#                 "title": new_title,
#                 "instructor": new_instructor,
#                 "category": new_category.lower().strip(),
#                 "price": float(new_price),
#                 "duration_hours": float(new_duration),
#                 "is_published": new_published,
#                 "discount_percent": discount_val,
#             }
#             errors = validate_course(new_course, courses)
#             if errors:
#                 for e in errors:
#                     st.error(e)
#             else:
#                 courses.append(new_course)
#                 save_data(courses)
#                 st.session_state.courses = courses
#                 st.success(f"✅ Course '{new_title}' added successfully!")
#                 st.rerun()


# # ═══════════════════════════════════════════════════════════════════════════════
# # TAB 3 — EDIT COURSE
# # ═══════════════════════════════════════════════════════════════════════════════
# with tab_edit:
#     st.markdown("### Edit Existing Course")

#     course_options = {f"[{c['id']}] {c['title']}": c["id"] for c in courses}
#     selected_label = st.selectbox("Select course to edit", list(course_options.keys()))
#     selected_id = course_options[selected_label] if selected_label else None
#     course_to_edit = next((c for c in courses if c["id"] == selected_id), None)

#     if course_to_edit:
#         with st.form("edit_form"):
#             e1, e2 = st.columns(2)
#             with e1:
#                 edit_id_val = st.number_input("ID", value=course_to_edit["id"], min_value=1, step=1)
#                 edit_title = st.text_input("Title", value=course_to_edit["title"])
#                 edit_instructor = st.text_input("Instructor", value=course_to_edit["instructor"])
#                 edit_category = st.text_input("Category", value=course_to_edit["category"])
#             with e2:
#                 edit_price = st.number_input("Price (₹)", value=float(course_to_edit["price"]), min_value=0.01, step=1.0)
#                 edit_duration = st.number_input("Duration (hours)", value=float(course_to_edit["duration_hours"]), min_value=0.5, step=0.5)
#                 edit_published = st.checkbox("Published", value=course_to_edit["is_published"])
#                 edit_discount = st.number_input("Discount %", value=float(course_to_edit["discount_percent"] or 0),
#                                                 min_value=0.0, max_value=100.0, step=0.1,
#                                                 help="Leave 0 for no discount.")

#             update_btn = st.form_submit_button("💾 Save Changes", use_container_width=True, type="primary")
#             if update_btn:
#                 discount_val = edit_discount if edit_discount > 0 else None
#                 updated = {
#                     "id": int(edit_id_val),
#                     "title": edit_title,
#                     "instructor": edit_instructor,
#                     "category": edit_category.lower().strip(),
#                     "price": float(edit_price),
#                     "duration_hours": float(edit_duration),
#                     "is_published": edit_published,
#                     "discount_percent": discount_val,
#                 }
#                 errors = validate_course(updated, courses, edit_id=selected_id)
#                 if errors:
#                     for e in errors:
#                         st.error(e)
#                 else:
#                     idx = next(i for i, c in enumerate(courses) if c["id"] == selected_id)
#                     courses[idx] = updated
#                     save_data(courses)
#                     st.session_state.courses = courses
#                     st.success(f"✅ Course updated successfully!")
#                     st.rerun()


# # ═══════════════════════════════════════════════════════════════════════════════
# # TAB 4 — DELETE COURSE
# # ═══════════════════════════════════════════════════════════════════════════════
# with tab_delete:
#     st.markdown("### Delete a Course")

#     del_options = {f"[{c['id']}] {c['title']}": c["id"] for c in courses}
#     del_label = st.selectbox("Select course to delete", list(del_options.keys()))
#     del_id = del_options[del_label] if del_label else None
#     course_to_del = next((c for c in courses if c["id"] == del_id), None)

#     if course_to_del:
#         st.markdown("**Course details:**")
#         d1, d2, d3, d4 = st.columns(4)
#         d1.metric("Price", f"₹{course_to_del['price']:,.0f}")
#         d2.metric("Duration", f"{course_to_del['duration_hours']}h")
#         d3.metric("Status", "Published" if course_to_del["is_published"] else "Draft")
#         d4.metric("Category", course_to_del["category"].title())

#         st.warning(f"⚠️ Are you sure you want to delete **{course_to_del['title']}**? This cannot be undone.")

#         if st.button("🗑️ Confirm Delete", type="primary", use_container_width=False):
#             courses = [c for c in courses if c["id"] != del_id]
#             save_data(courses)
#             st.session_state.courses = courses
#             st.success(f"✅ Course deleted successfully!")
#             st.rerun()


import streamlit as st
import json
import pandas as pd
from pathlib import Path
from collections import Counter

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CourseVault",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS Theme ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:      #080B10;
    --bg2:     #0D1117;
    --bg3:     #111820;
    --card:    #0F1620;
    --border:  #1E2D3D;
    --border2: #243447;
    --accent:  #00F5A0;
    --accent2: #00D4FF;
    --accent3: #FF6B6B;
    --gold:    #FFD166;
    --text:    #E8F4FD;
    --muted:   #5A7A94;
    --muted2:  #3D5A72;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
.stApp { background: var(--bg) !important; }
.block-container { padding: 1.5rem 2.5rem 3rem !important; max-width: 1400px !important; }

/* ── Hero ── */
.hero {
    position: relative;
    padding: 2.5rem 0 2rem;
    margin-bottom: 2rem;
    border-bottom: 1px solid var(--border);
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; left: -100px;
    width: 500px; height: 300px;
    background: radial-gradient(ellipse, rgba(0,245,160,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    top: -40px; right: -80px;
    width: 400px; height: 250px;
    background: radial-gradient(ellipse, rgba(0,212,255,0.05) 0%, transparent 70%);
    pointer-events: none;
}
.hero-label {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.25em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(135deg, #E8F4FD 0%, #00F5A0 50%, #00D4FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin: 0;
}
.hero-sub {
    font-size: 14px;
    color: var(--muted);
    margin-top: 0.5rem;
    font-weight: 300;
}

/* ── Stat cards ── */
.stat-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 2rem; }
.stat-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.stat-card:hover { border-color: var(--border2); }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; }
.stat-card.green::before  { background: linear-gradient(90deg, var(--accent), transparent); }
.stat-card.blue::before   { background: linear-gradient(90deg, var(--accent2), transparent); }
.stat-card.red::before    { background: linear-gradient(90deg, var(--accent3), transparent); }
.stat-card.gold::before   { background: linear-gradient(90deg, var(--gold), transparent); }
.stat-lbl {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.15em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 6px;
}
.stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 30px;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
}
.stat-icon { position: absolute; right: 1rem; top: 50%; transform: translateY(-50%); font-size: 28px; opacity: 0.12; }

/* ── Section headers ── */
.section-hdr { display: flex; align-items: center; gap: 10px; margin-bottom: 1.25rem; }
.section-hdr h3 { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 700; color: var(--text); margin: 0; }
.section-hdr .pill {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
    background: rgba(0,245,160,0.1);
    color: var(--accent);
    border: 1px solid rgba(0,245,160,0.2);
    border-radius: 20px;
    padding: 2px 10px;
}
.section-hdr .pill-red {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
    background: rgba(255,107,107,0.1);
    color: var(--accent3);
    border: 1px solid rgba(255,107,107,0.2);
    border-radius: 20px;
    padding: 2px 10px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg2) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--muted) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 8px 20px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: var(--card) !important;
    color: var(--text) !important;
    border: 1px solid var(--border2) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 1.5rem 0 0 !important; }

/* ── Inputs ── */
.stTextInput input, .stNumberInput input {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,245,160,0.1) !important;
}
.stSelectbox > div > div {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
label { color: var(--muted) !important; font-size: 13px !important; }

/* ── Buttons ── */
.stButton button, .stFormSubmitButton button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: #080B10 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0.04em !important;
}
.stButton button:hover, .stFormSubmitButton button:hover { opacity: 0.85 !important; }

/* ── Dataframe ── */
.stDataFrame { border: 1px solid var(--border) !important; border-radius: 12px !important; overflow: hidden !important; }

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
[data-testid="metric-container"] label { color: var(--muted) !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    color: var(--text) !important;
}

/* ── Form ── */
[data-testid="stForm"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 1.5rem !important;
}

/* ── Alerts ── */
.stSuccess { background: rgba(0,245,160,0.07) !important; border: 1px solid rgba(0,245,160,0.2) !important; border-radius: 8px !important; }
.stWarning { background: rgba(255,209,102,0.07) !important; border: 1px solid rgba(255,209,102,0.2) !important; border-radius: 8px !important; }
.stError   { background: rgba(255,107,107,0.07) !important; border: 1px solid rgba(255,107,107,0.2) !important; border-radius: 8px !important; }

.stCaption { color: var(--muted) !important; font-family: 'Space Mono', monospace !important; font-size: 11px !important; }
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted2); }

/* ── Delete zone ── */
.delete-zone {
    background: rgba(255,107,107,0.05);
    border: 1px solid rgba(255,107,107,0.15);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
DATA_FILE = Path(__file__).parent / "course.json"

def load_data():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def price_category(p):
    return "Budget" if p < 700 else "Standard" if p < 1000 else "Premium"

def validate_course(data, courses, edit_id=None):
    errors = []
    if data["id"] <= 0:
        errors.append("ID must be > 0")
    existing_ids = [c["id"] for c in courses if c["id"] != edit_id]
    if data["id"] in existing_ids:
        errors.append(f"Course ID {data['id']} already exists")
    if len(data["title"].strip()) < 2:
        errors.append("Title must be at least 2 characters")
    if len(data["instructor"].strip()) < 2:
        errors.append("Instructor must be at least 2 characters")
    if len(data["category"].strip()) < 2:
        errors.append("Category must be at least 2 characters")
    if data["price"] <= 0:
        errors.append("Price must be > 0")
    if data["duration_hours"] <= 0:
        errors.append("Duration must be > 0")
    if not data["is_published"] and data["discount_percent"] is not None:
        errors.append("Discount only allowed for published courses")
    return errors


# ── Session state ─────────────────────────────────────────────────────────────
if "courses" not in st.session_state:
    st.session_state.courses = load_data()

courses = st.session_state.courses


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-label">⚡ Admin Dashboard</div>
    <div class="hero-title">CourseVault</div>
    <div class="hero-sub">Manage, monitor and publish your course catalogue in one place</div>
</div>
""", unsafe_allow_html=True)

# ── Stat cards ────────────────────────────────────────────────────────────────
total     = len(courses)
published = sum(1 for c in courses if c["is_published"])
avg_price = round(sum(c["price"] for c in courses) / total) if total else 0
cats      = len(set(c["category"] for c in courses))

st.markdown(f"""
<div class="stat-row">
  <div class="stat-card green">
    <div class="stat-lbl">Total Courses</div>
    <div class="stat-val">{total}</div>
    <div class="stat-icon">📚</div>
  </div>
  <div class="stat-card blue">
    <div class="stat-lbl">Published</div>
    <div class="stat-val">{published}</div>
    <div class="stat-icon">✅</div>
  </div>
  <div class="stat-card gold">
    <div class="stat-lbl">Avg Price</div>
    <div class="stat-val">₹{avg_price:,}</div>
    <div class="stat-icon">💰</div>
  </div>
  <div class="stat-card red">
    <div class="stat-lbl">Categories</div>
    <div class="stat-val">{cats}</div>
    <div class="stat-icon">🏷️</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_browse, tab_add, tab_edit, tab_delete = st.tabs([
    "  📋  Browse & Filter  ",
    "  ➕  Add Course  ",
    "  ✏️  Edit Course  ",
    "  🗑️  Delete Course  "
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — BROWSE
# ══════════════════════════════════════════════════════════════════════════════
with tab_browse:
    st.markdown("""
    <div class="section-hdr">
        <h3>All Courses</h3>
        <span class="pill">LIVE DATA</span>
    </div>""", unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns([3, 2, 1.5, 2])
    with f1:
        search = st.text_input("", placeholder="🔍  Search title or instructor...", key="search")
    with f2:
        all_cats = sorted(set(c["category"] for c in courses))
        cat_filter = st.selectbox("", ["All Categories"] + all_cats, key="cat")
    with f3:
        status_filter = st.selectbox("", ["All Status", "Published", "Draft"], key="status")
    with f4:
        price_filter = st.selectbox("", ["All Tiers", "Budget  <₹700", "Standard  ₹700–999", "Premium  ₹1000+"], key="tier")

    filtered = courses[:]
    if search:
        q = search.lower()
        filtered = [c for c in filtered if q in c["title"].lower() or q in c["instructor"].lower()]
    if cat_filter != "All Categories":
        filtered = [c for c in filtered if c["category"] == cat_filter]
    if status_filter == "Published":
        filtered = [c for c in filtered if c["is_published"]]
    elif status_filter == "Draft":
        filtered = [c for c in filtered if not c["is_published"]]
    if "Budget" in price_filter:
        filtered = [c for c in filtered if c["price"] < 700]
    elif "Standard" in price_filter:
        filtered = [c for c in filtered if 700 <= c["price"] < 1000]
    elif "Premium" in price_filter:
        filtered = [c for c in filtered if c["price"] >= 1000]

    st.caption(f"↳  {len(filtered)} course(s) found")

    if not filtered:
        st.info("No courses match your filters.")
    else:
        rows = []
        for c in filtered:
            disc = f"{c['discount_percent']}%" if c["discount_percent"] is not None else "—"
            rows.append({
                "ID": c["id"],
                "Title": c["title"],
                "Instructor": c["instructor"],
                "Category": c["category"].title(),
                "Price (₹)": f"₹{c['price']:,.0f}",
                "Discount": disc,
                "Hrs": c["duration_hours"],
                "Status": "✅ Published" if c["is_published"] else "○ Draft",
                "Tier": price_category(c["price"]),
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True, height=380)

    st.markdown("---")
    st.markdown("""
    <div class="section-hdr">
        <h3>Insights</h3>
        <span class="pill">ANALYTICS</span>
    </div>""", unsafe_allow_html=True)

    ch1, ch2 = st.columns(2)
    with ch1:
        st.caption("COURSES BY CATEGORY")
        cat_counts = Counter(c["category"].title() for c in courses)
        cat_df = pd.DataFrame(cat_counts.items(), columns=["Category", "Count"]).sort_values("Count", ascending=False)
        st.bar_chart(cat_df.set_index("Category"), color="#00F5A0", height=240)
    with ch2:
        st.caption("PRICE TIER DISTRIBUTION")
        tier_counts = {"Budget": 0, "Standard": 0, "Premium": 0}
        for c in courses:
            tier_counts[price_category(c["price"])] += 1
        tier_df = pd.DataFrame(tier_counts.items(), columns=["Tier", "Count"])
        st.bar_chart(tier_df.set_index("Tier"), color="#00D4FF", height=240)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ADD
# ══════════════════════════════════════════════════════════════════════════════
with tab_add:
    st.markdown("""
    <div class="section-hdr">
        <h3>Add New Course</h3>
        <span class="pill">CREATE</span>
    </div>""", unsafe_allow_html=True)

    with st.form("add_form"):
        a1, a2 = st.columns(2)
        with a1:
            new_id         = st.number_input("Course ID", min_value=1, step=1, value=max((c["id"] for c in courses), default=0) + 1)
            new_title      = st.text_input("Title", placeholder="e.g. Python for Beginners")
            new_instructor = st.text_input("Instructor", placeholder="e.g. Aanya Sharma")
            new_category   = st.text_input("Category", placeholder="e.g. programming")
        with a2:
            new_price     = st.number_input("Price (₹)", min_value=0.01, step=50.0, value=499.0)
            new_duration  = st.number_input("Duration (hours)", min_value=0.5, step=0.5, value=10.0)
            new_published = st.checkbox("Mark as Published")
            new_discount  = st.number_input("Discount %", min_value=0.0, max_value=100.0, step=0.5, value=0.0,
                                            help="Leave 0 for no discount. Only valid when Published.")
        st.markdown("")
        if st.form_submit_button("⚡  Add Course to Vault", use_container_width=True):
            discount_val = new_discount if new_discount > 0 else None
            new_course = {
                "id": int(new_id), "title": new_title, "instructor": new_instructor,
                "category": new_category.lower().strip(), "price": float(new_price),
                "duration_hours": float(new_duration), "is_published": new_published,
                "discount_percent": discount_val,
            }
            errors = validate_course(new_course, courses)
            if errors:
                for e in errors: st.error(f"✖  {e}")
            else:
                courses.append(new_course)
                save_data(courses)
                st.session_state.courses = courses
                st.success(f"✦  **{new_title}** added to the vault!")
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — EDIT
# ══════════════════════════════════════════════════════════════════════════════
with tab_edit:
    st.markdown("""
    <div class="section-hdr">
        <h3>Edit Course</h3>
        <span class="pill">MODIFY</span>
    </div>""", unsafe_allow_html=True)

    course_map = {f"[{c['id']}]  {c['title']}": c["id"] for c in courses}
    sel_label  = st.selectbox("Select a course to edit", list(course_map.keys()), key="edit_sel")
    sel_id     = course_map[sel_label] if sel_label else None
    cte        = next((c for c in courses if c["id"] == sel_id), None)

    if cte:
        cp = st.columns(4)
        cp[0].metric("Price", f"₹{cte['price']:,.0f}")
        cp[1].metric("Duration", f"{cte['duration_hours']}h")
        cp[2].metric("Status", "Published" if cte["is_published"] else "Draft")
        cp[3].metric("Tier", price_category(cte["price"]))
        st.markdown("")

        with st.form("edit_form"):
            e1, e2 = st.columns(2)
            with e1:
                edit_id_v      = st.number_input("Course ID", value=cte["id"], min_value=1, step=1)
                edit_title     = st.text_input("Title", value=cte["title"])
                edit_instructor= st.text_input("Instructor", value=cte["instructor"])
                edit_category  = st.text_input("Category", value=cte["category"])
            with e2:
                edit_price    = st.number_input("Price (₹)", value=float(cte["price"]), min_value=0.01, step=50.0)
                edit_duration = st.number_input("Duration (hours)", value=float(cte["duration_hours"]), min_value=0.5, step=0.5)
                edit_pub      = st.checkbox("Published", value=cte["is_published"])
                edit_discount = st.number_input("Discount %", value=float(cte["discount_percent"] or 0),
                                                min_value=0.0, max_value=100.0, step=0.5)
            st.markdown("")
            if st.form_submit_button("💾  Save Changes", use_container_width=True):
                discount_val = edit_discount if edit_discount > 0 else None
                updated = {
                    "id": int(edit_id_v), "title": edit_title, "instructor": edit_instructor,
                    "category": edit_category.lower().strip(), "price": float(edit_price),
                    "duration_hours": float(edit_duration), "is_published": edit_pub,
                    "discount_percent": discount_val,
                }
                errors = validate_course(updated, courses, edit_id=sel_id)
                if errors:
                    for e in errors: st.error(f"✖  {e}")
                else:
                    idx = next(i for i, c in enumerate(courses) if c["id"] == sel_id)
                    courses[idx] = updated
                    save_data(courses)
                    st.session_state.courses = courses
                    st.success("✦  Changes saved successfully!")
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — DELETE
# ══════════════════════════════════════════════════════════════════════════════
with tab_delete:
    st.markdown("""
    <div class="section-hdr">
        <h3>Delete Course</h3>
        <span class="pill-red">DANGER ZONE</span>
    </div>""", unsafe_allow_html=True)

    del_map   = {f"[{c['id']}]  {c['title']}": c["id"] for c in courses}
    del_label = st.selectbox("Select a course to remove", list(del_map.keys()), key="del_sel")
    del_id    = del_map[del_label] if del_label else None
    ctd       = next((c for c in courses if c["id"] == del_id), None)

    if ctd:
        st.markdown(f"""
        <div class="delete-zone">
            <p style="font-family:'Space Mono',monospace;font-size:11px;letter-spacing:0.1em;color:#FF6B6B;text-transform:uppercase;margin-bottom:12px;">⚠ You are about to delete</p>
            <p style="font-family:'Syne',sans-serif;font-size:20px;font-weight:700;color:#E8F4FD;margin-bottom:4px;">{ctd['title']}</p>
            <p style="color:#5A7A94;font-size:13px;margin:0;">by {ctd['instructor']} &nbsp;·&nbsp; {ctd['category'].title()} &nbsp;·&nbsp; ₹{ctd['price']:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)

        dp = st.columns(4)
        dp[0].metric("Price", f"₹{ctd['price']:,.0f}")
        dp[1].metric("Duration", f"{ctd['duration_hours']}h")
        dp[2].metric("Status", "Published" if ctd["is_published"] else "Draft")
        dp[3].metric("Tier", price_category(ctd["price"]))

        st.markdown("")
        st.warning("⚠️  This action is **permanent** and cannot be undone.")
        if st.button("🗑️  Permanently Delete This Course"):
            courses = [c for c in courses if c["id"] != del_id]
            save_data(courses)
            st.session_state.courses = courses
            st.success("✦  Course removed from the vault.")
            st.rerun()