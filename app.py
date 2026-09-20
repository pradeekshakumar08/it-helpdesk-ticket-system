import pandas as pd
import streamlit as st

import db

st.set_page_config(page_title="IT Helpdesk", page_icon="🛠️")
db.init_db()

st.title("IT Helpdesk Ticket System")

page = st.sidebar.radio("Go to", ["Raise a Ticket", "Manage Tickets", "Dashboard"])

if page == "Raise a Ticket":
    st.header("Raise a new ticket")
    title = st.text_input("Title")
    description = st.text_area("Describe the problem")
    category = st.selectbox("Category", db.CATEGORIES)
    priority = st.selectbox("Priority", db.PRIORITIES)

    if st.button("Submit ticket"):
        if title.strip() == "":
            st.error("Please enter a title.")
        else:
            db.add_ticket(title.strip(), description.strip(), category, priority)
            st.success("Ticket submitted!")

    st.subheader("Latest tickets")
    st.dataframe(db.get_tickets().head(10))

elif page == "Manage Tickets":
    st.header("Manage tickets")
    tickets = db.get_tickets()

    status_filter = st.selectbox("Show tickets with status", ["All"] + db.STATUSES)
    if status_filter == "All":
        shown = tickets
    else:
        shown = tickets[tickets["status"] == status_filter]
    st.dataframe(shown)

    st.subheader("Update a ticket")
    if tickets.empty:
        st.info("No tickets yet.")
    else:
        options = {}
        for row in tickets.itertuples():
            options[f"#{row.id} - {row.title} ({row.status})"] = int(row.id)
        chosen = st.selectbox("Choose a ticket", list(options.keys()))
        new_status = st.selectbox("New status", db.STATUSES)
        if st.button("Update status"):
            db.update_status(options[chosen], new_status)
            st.toast("Status updated!")
            st.rerun()

else:
    st.header("Dashboard")
    df = db.get_tickets()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total tickets", len(df))
    col2.metric("Open", int((df["status"] == "Open").sum()))
    col3.metric("In Progress", int((df["status"] == "In Progress").sum()))
    col4.metric("Resolved", int((df["status"] == "Resolved").sum()))

    resolved = df[df["status"] == "Resolved"]
    if not resolved.empty:
        hours = (
            pd.to_datetime(resolved["resolved_at"]) - pd.to_datetime(resolved["created_at"])
        ).dt.total_seconds() / 3600
        st.metric("Average resolution time (hours)", round(hours.mean(), 1))

    st.subheader("Tickets by category")
    st.bar_chart(df["category"].value_counts())

    st.subheader("Tickets by priority")
    st.bar_chart(df["priority"].value_counts())

    st.subheader("Most common issues")
    st.dataframe(df["title"].value_counts().head(5).rename("count"))
