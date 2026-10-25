
import sqlite3
from pathlib import Path
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------- CONFIGURATION ----------------

st.set_page_config(
    page_title="CareerPilot | Job Tracker",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "jobs.db"

STATUSES = [
    "Applied",
    "Interview",
    "Selected",
    "Rejected",
    "Offer Received",
]

# ---------------- DATABASE ----------------

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                location TEXT DEFAULT '',
                job_type TEXT DEFAULT 'Full-time',
                status TEXT NOT NULL DEFAULT 'Applied',
                applied_date TEXT NOT NULL,
                deadline TEXT DEFAULT '',
                job_link TEXT DEFAULT '',
                notes TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

def load_applications():
    with get_connection() as conn:
        return pd.read_sql_query(
            "SELECT * FROM applications ORDER BY id DESC",
            conn,
        )

def add_application(data):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO applications (
                company, role, location, job_type, status,
                applied_date, deadline, job_link, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["company"],
            data["role"],
            data["location"],
            data["job_type"],
            data["status"],
            data["applied_date"],
            data["deadline"],
            data["job_link"],
            data["notes"],
        ))

def update_application(application_id, data):
    with get_connection() as conn:
        conn.execute("""
            UPDATE applications
            SET company = ?, role = ?, location = ?,
                job_type = ?, status = ?, applied_date = ?,
                deadline = ?, job_link = ?, notes = ?
            WHERE id = ?
        """, (
            data["company"],
            data["role"],
            data["location"],
            data["job_type"],
            data["status"],
            data["applied_date"],
            data["deadline"],
            data["job_link"],
            data["notes"],
            application_id,
        ))

def delete_application(application_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM applications WHERE id = ?",
            (application_id,),
        )

initialize_database()

# ---------------- CUSTOM UI ----------------

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f7f9ff 0%, #eef3ff 100%);
    }
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }
    [data-testid="stSidebar"] {
        background: #111b35;
    }
    [data-testid="stSidebar"] * {
        color: #f4f7ff;
    }
    .hero {
        background: linear-gradient(120deg, #172554, #2563eb);
        color: white;
        padding: 28px;
        border-radius: 20px;
        margin-bottom: 24px;
        box-shadow: 0 12px 32px rgba(37, 99, 235, .18);
    }
    .hero h1 {
        font-size: 34px;
        margin: 0 0 8px 0;
        color: white;
    }
    .hero p {
        color: #dbeafe;
        margin-bottom: 0;
    }
    div[data-testid="stMetric"] {
        background: white;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #e3eaf7;
        box-shadow: 0 5px 15px rgba(30, 64, 175, .05);
    }
    div[data-testid="stForm"] {
        background: white;
        border: 1px solid #e3eaf7;
        border-radius: 16px;
        padding: 18px;
    }
    div.stButton > button,
    div.stFormSubmitButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all .2s ease;
    }
    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        transform: translateY(-2px);
    }
    h2, h3 {
        color: #172554;
    }
    .small-note {
        color: #64748b;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("# 💼 CareerPilot")
    st.caption("Your personal job search workspace")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Add Application",
            "Manage Applications",
            "Reports & Export",
        ],
    )

    st.divider()
    st.markdown("### 🎯 Career goal")
    st.write("Stay organized. Follow up. Get hired.")
    st.caption("CareerPilot • Python Portfolio Project")

# ---------------- LOAD DATA ----------------

df = load_applications()

# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>CareerPilot 🚀</h1>
    <p>Track applications, organize interviews, and manage your job search in one place.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------

if page == "Dashboard":
    st.subheader("Your career dashboard")
    st.caption(f"Today: {date.today().strftime('%d %B %Y')}")

    total = len(df)
    interviews = int((df["status"] == "Interview").sum()) if total else 0
    selected = int(df["status"].isin(
        ["Selected", "Offer Received"]
    ).sum()) if total else 0
    rejected = int((df["status"] == "Rejected").sum()) if total else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📨 Total Applications", total)
    col2.metric("🎤 Interviews", interviews)
    col3.metric("🏆 Selected / Offers", selected)
    col4.metric("❌ Rejected", rejected)

    st.divider()
    left, right = st.columns(2)

    with left:
        st.subheader("Application status")
        if total:
            status_counts = (
                df["status"].value_counts()
                .rename_axis("Status")
                .reset_index(name="Applications")
            )
            fig = px.pie(
                status_counts,
                names="Status",
                values="Applications",
                hole=0.58,
                title="Where your applications stand",
            )
            fig.update_layout(
                margin=dict(t=55, b=15, l=10, r=10),
                legend_title_text="Status",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No applications yet. Add your first application!")

    with right:
        st.subheader("Recent applications")
        if total:
            recent = df.head(5)[
                ["company", "role", "status", "applied_date"]
            ].copy()
            recent.columns = [
                "Company", "Role", "Status", "Applied date"
            ]
            st.dataframe(
                recent,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.write("Your latest applications will appear here.")

    st.divider()
    st.subheader("📅 Upcoming deadlines")

    if total:
        deadlines = df[df["deadline"].fillna("").str.strip() != ""].copy()
        if not deadlines.empty:
            deadlines["deadline_date"] = pd.to_datetime(
                deadlines["deadline"], errors="coerce"
            ).dt.date
            today = date.today()
            limit = today + timedelta(days=14)

            upcoming = deadlines[
                (deadlines["deadline_date"] >= today)
                & (deadlines["deadline_date"] <= limit)
            ].sort_values("deadline_date")

            if not upcoming.empty:
                st.dataframe(
                    upcoming[
                        ["company", "role", "deadline", "status"]
                    ].rename(columns={
                        "company": "Company",
                        "role": "Role",
                        "deadline": "Deadline",
                        "status": "Status",
                    }),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.success("No upcoming deadlines in the next 14 days.")
        else:
            st.caption("Add deadlines to keep track of important dates.")
    else:
        st.caption("Add an application to start tracking deadlines.")

# ---------------- ADD APPLICATION ----------------

elif page == "Add Application":
    st.subheader("➕ Add a job application")
    st.write("Record the details so you can follow up later.")

    with st.form("add_application_form", clear_on_submit=True):
        c1, c2 = st.columns(2)

        with c1:
            company = st.text_input(
                "Company name *",
                placeholder="e.g. Infosys",
            )
            role = st.text_input(
                "Job role *",
                placeholder="e.g. Python Developer",
            )
            location = st.text_input(
                "Location",
                placeholder="e.g. Nashik / Pune / Remote",
            )
            job_type = st.selectbox(
                "Job type",
                ["Full-time", "Internship", "Part-time", "Contract"],
            )

        with c2:
            status = st.selectbox("Application status", STATUSES)
            applied_date = st.date_input(
                "Application date",
                value=date.today(),
            )
            has_deadline = st.checkbox("Add a deadline")
            deadline_date = st.date_input(
                "Deadline",
                value=date.today() + timedelta(days=7),
                disabled=not has_deadline,
            )
            job_link = st.text_input(
                "Job posting URL",
                placeholder="https://...",
            )

        notes = st.text_area(
            "Notes",
            placeholder="Recruiter details, interview preparation, follow-up plan...",
        )

        submitted = st.form_submit_button(
            "Save application",
            use_container_width=True,
        )

        if submitted:
            if not company.strip() or not role.strip():
                st.error("Company name and job role are required.")
            elif job_link.strip() and not (
                job_link.strip().startswith("https://")
                or job_link.strip().startswith("http://")
            ):
                st.error("Enter a valid URL beginning with http:// or https://.")
            elif has_deadline and deadline_date < applied_date:
                st.error("Deadline cannot be earlier than the application date.")
            else:
                add_application({
                    "company": company.strip(),
                    "role": role.strip(),
                    "location": location.strip(),
                    "job_type": job_type,
                    "status": status,
                    "applied_date": applied_date.isoformat(),
                    "deadline": (
                        deadline_date.isoformat()
                        if has_deadline else ""
                    ),
                    "job_link": job_link.strip(),
                    "notes": notes.strip(),
                })
                st.success(f"Application at {company.strip()} saved!")
                st.rerun()

# ---------------- MANAGE APPLICATIONS ----------------

elif page == "Manage Applications":
    st.subheader("🗂️ Manage applications")

    if df.empty:
        st.info("No applications found. Add an application first.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            search = st.text_input(
                "🔍 Search",
                placeholder="Search company, role, or location",
            )
        with c2:
            status_filter = st.multiselect(
                "Filter by status",
                STATUSES,
                default=[],
            )

        filtered = df.copy()

        if search.strip():
            search_text = search.strip()
            mask = (
                filtered["company"].fillna("").str.contains(
                    search_text, case=False, regex=False
                )
                | filtered["role"].fillna("").str.contains(
                    search_text, case=False, regex=False
                )
                | filtered["location"].fillna("").str.contains(
                    search_text, case=False, regex=False
                )
            )
            filtered = filtered[mask]

        if status_filter:
            filtered = filtered[
                filtered["status"].isin(status_filter)
            ]

        st.caption(f"{len(filtered)} application(s) shown")
        display = filtered[
            ["id", "company", "role", "location", "status",
             "applied_date", "deadline", "job_link"]
        ].copy()
        display.columns = [
            "ID", "Company", "Role", "Location", "Status",
            "Applied date", "Deadline", "Job link"
        ]
        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Job link": st.column_config.LinkColumn(
                    "Job posting",
                    display_text="Open job",
                ),
            },
        )

        st.divider()
        st.subheader("✏️ Edit an application")

        ids = filtered["id"].tolist()
        if ids:
            selected_id = st.selectbox(
                "Choose application ID",
                ids,
                format_func=lambda x: (
                    f"#{x} — "
                    f"{df.loc[df['id'] == x, 'company'].iloc[0]} "
                    f"| {df.loc[df['id'] == x, 'role'].iloc[0]}"
                ),
            )
            record = df.loc[df["id"] == selected_id].iloc[0]

            with st.form("edit_application_form"):
                a, b = st.columns(2)

                with a:
                    edit_company = st.text_input(
                        "Company",
                        value=str(record["company"]),
                    )
                    edit_role = st.text_input(
                        "Role",
                        value=str(record["role"]),
                    )
                    edit_location = st.text_input(
                        "Location",
                        value=str(record["location"] or ""),
                    )
                    edit_type = st.selectbox(
                        "Job type",
                        ["Full-time", "Internship", "Part-time", "Contract"],
                        index=(
                            ["Full-time", "Internship", "Part-time", "Contract"]
                            .index(record["job_type"])
                            if record["job_type"] in
                            ["Full-time", "Internship", "Part-time", "Contract"]
                            else 0
                        ),
                    )

                with b:
                    current_status = (
                        record["status"]
                        if record["status"] in STATUSES else "Applied"
                    )
                    edit_status = st.selectbox(
                        "Status",
                        STATUSES,
                        index=STATUSES.index(current_status),
                    )
                    try:
                        initial_applied = date.fromisoformat(
                            str(record["applied_date"])
                        )
                    except ValueError:
                        initial_applied = date.today()

                    edit_applied = st.date_input(
                        "Applied date",
                        value=initial_applied,
                    )
                    current_deadline = str(record["deadline"] or "")
                    has_edit_deadline = st.checkbox(
                        "Keep/add deadline",
                        value=bool(current_deadline),
                    )

                    try:
                        initial_deadline = date.fromisoformat(
                            current_deadline
                        ) if current_deadline else date.today() + timedelta(days=7)
                    except ValueError:
                        initial_deadline = date.today() + timedelta(days=7)

                    edit_deadline = st.date_input(
                        "Deadline",
                        value=initial_deadline,
                        disabled=not has_edit_deadline,
                    )
                    edit_link = st.text_input(
                        "Job posting URL",
                        value=str(record["job_link"] or ""),
                    )

                edit_notes = st.text_area(
                    "Notes",
                    value=str(record["notes"] or ""),
                )

                save_edit = st.form_submit_button(
                    "Update application",
                    use_container_width=True,
                )

                if save_edit:
                    if not edit_company.strip() or not edit_role.strip():
                        st.error("Company and role are required.")
                    elif edit_link.strip() and not (
                        edit_link.strip().startswith("https://")
                        or edit_link.strip().startswith("http://")
                    ):
                        st.error("Enter a valid job URL.")
                    elif has_edit_deadline and edit_deadline < edit_applied:
                        st.error("Deadline cannot be earlier than applied date.")
                    else:
                        update_application(selected_id, {
                            "company": edit_company.strip(),
                            "role": edit_role.strip(),
                            "location": edit_location.strip(),
                            "job_type": edit_type,
                            "status": edit_status,
                            "applied_date": edit_applied.isoformat(),
                            "deadline": (
                                edit_deadline.isoformat()
                                if has_edit_deadline else ""
                            ),
                            "job_link": edit_link.strip(),
                            "notes": edit_notes.strip(),
                        })
                        st.success("Application updated.")
                        st.rerun()

        st.divider()
        st.subheader("🗑️ Delete an application")
        delete_id = st.selectbox(
            "Select application to delete",
            df["id"].tolist(),
            format_func=lambda x: (
                f"#{x} — {df.loc[df['id'] == x, 'company'].iloc[0]}"
                f" | {df.loc[df['id'] == x, 'role'].iloc[0]}"
            ),
            key="delete_application_id",
        )

        confirm_delete = st.checkbox(
            "I confirm that I want to permanently delete this application."
        )

        if st.button("Delete application", type="secondary"):
            if confirm_delete:
                delete_application(delete_id)
                st.success("Application deleted.")
                st.rerun()
            else:
                st.warning("Tick the confirmation box before deleting.")

# ---------------- REPORTS & EXPORT ----------------

elif page == "Reports & Export":
    st.subheader("📊 Reports & export")
    st.write("Review your job search activity and export your records.")

    if df.empty:
        st.info("Add applications to generate reports.")
    else:
        left, right = st.columns(2)

        with left:
            counts = (
                df["status"].value_counts()
                .rename_axis("Status")
                .reset_index(name="Count")
            )
            fig = px.bar(
                counts,
                x="Status",
                y="Count",
                title="Applications by status",
                text="Count",
            )
            fig.update_layout(
                xaxis_title="Application status",
                yaxis_title="Number of applications",
            )
            st.plotly_chart(fig, use_container_width=True)

        with right:
            monthly = df.copy()
            monthly["Month"] = pd.to_datetime(
                monthly["applied_date"], errors="coerce"
            ).dt.to_period("M").astype(str)
            monthly = (
                monthly.dropna(subset=["Month"])
                .groupby("Month")
                .size()
                .reset_index(name="Applications")
                .sort_values("Month")
            )
            fig2 = px.line(
                monthly,
                x="Month",
                y="Applications",
                markers=True,
                title="Applications over time",
            )
            st.plotly_chart(fig2, use_container_width=True)

        csv_data = df.drop(columns=["created_at"], errors="ignore").to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download applications as CSV",
            data=csv_data,
            file_name="job_applications.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.caption(
            "Tip: Open the CSV file with Microsoft Excel or Google Sheets."
        )

# ---------------- FOOTER ----------------

st.divider()
st.markdown(
    "<p class='small-note'>CareerPilot · Built with Python, "
    "Streamlit, SQLite and Plotly</p>",
    unsafe_allow_html=True,
)
