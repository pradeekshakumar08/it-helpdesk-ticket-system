# IT Helpdesk Ticket Management System

A web app where users raise IT support tickets and support agents track them from Open to Resolved, with a dashboard showing ticket trends.

**Live app:** [Open the IT Helpdesk app](https://pradeekshakumar08-it-helpdesk-ticket-system-app-aiw1a9.streamlit.app)

## Features

- **Raise a Ticket:** a form with title, description, category (Network, Software, Hardware, Email, Access/Password) and priority (Low, Medium, High).
- **Manage Tickets:** filter tickets by status and update a ticket to Open, In Progress or Resolved. The resolution time is recorded automatically.
- **Dashboard:** total, open, in-progress and resolved counts, average resolution time, tickets by category and priority, and the most common issues.

## Tech Stack

- Python
- SQLite (database)
- pandas
- Streamlit (web interface)
- GitHub and Streamlit Community Cloud (hosting)

## How It Works

- `db.py` creates a `tickets` table in SQLite and provides functions to add tickets, read tickets and update their status.
- `app.py` builds the three pages of the web app on top of those functions.
- On first run the app fills the database with 40 sample tickets so the dashboard has data to show.

## Run It Locally

1. Install the requirements: `pip install -r requirements.txt`
2. Start the app: `streamlit run app.py`

## Limitations

- The app uses SQLite on a free hosting plan, so the database resets to the sample data whenever the app restarts. A production version would use a hosted database such as PostgreSQL.
- There is no login. Anyone with the link can raise or update tickets.

## Future Improvements

- User login with separate roles for users and support agents
- Email notifications when a ticket status changes
- Hosted database so tickets are kept permanently
- SLA tracking, for example flagging tickets open for more than 48 hours

## Author

**Pradeeksha N**, B.Tech Electronics and Communication Engineering, Karunya Institute of Technology and Sciences
