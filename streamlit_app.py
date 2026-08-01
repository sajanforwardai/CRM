import streamlit as st
import sqlite3
from datetime import datetime
import os

# Page config
st.set_page_config(page_title="ForwardAI CRM", layout="wide")

# Database setup
DB_PATH = "/tmp/forwardai_crm.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    cur = conn.cursor()

    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            display_name TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Clients table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            industry TEXT,
            contact_email TEXT,
            contact_phone TEXT,
            annual_value REAL DEFAULT 0,
            status TEXT DEFAULT 'prospect',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Projects table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'proposal',
            start_date DATE,
            end_date DATE,
            estimated_hours INTEGER DEFAULT 0,
            actual_hours INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    """)

    conn.commit()
    cur.close()

# Initialize database on load
try:
    init_db()
except Exception as e:
    st.error(f"Database error: {e}")

# Sidebar navigation
st.sidebar.title("🚀 ForwardAI CRM")
page = st.sidebar.radio("Navigate", ["Dashboard", "Clients", "Projects", "Settings"])

if page == "Dashboard":
    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Total clients
        cur.execute("SELECT COUNT(*) as count FROM clients")
        client_count = cur.fetchone()[0]
        col1.metric("Total Clients", client_count)

        # Active projects
        cur.execute("SELECT COUNT(*) as count FROM projects WHERE status = 'active'")
        project_count = cur.fetchone()[0]
        col2.metric("Active Projects", project_count)

        # Pipeline value
        cur.execute("SELECT COALESCE(SUM(annual_value), 0) as total FROM clients WHERE status = 'prospect'")
        pipeline_value = cur.fetchone()[0]
        col3.metric("Pipeline Value", f"${pipeline_value:,.0f}")

        cur.close()
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

    st.write("---")
    st.write("Welcome to ForwardAI CRM. Use the sidebar to manage clients and projects.")

elif page == "Clients":
    st.title("👥 Clients")

    tab1, tab2 = st.tabs(["View", "Add New"])

    with tab1:
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("SELECT * FROM clients ORDER BY created_at DESC")
            clients = cur.fetchall()

            if clients:
                for client in clients:
                    with st.expander(f"**{client['name']}** • {client['status']}"):
                        col1, col2 = st.columns(2)
                        col1.write(f"📧 {client['contact_email']}")
                        col2.write(f"💼 {client['industry']}")
                        st.write(f"💰 Annual Value: ${client['annual_value']:,.0f}")
                        st.write(f"📅 Created: {client['created_at']}")
            else:
                st.info("No clients yet. Add one using the 'Add New' tab.")

            cur.close()
        except Exception as e:
            st.error(f"Error loading clients: {e}")

    with tab2:
        with st.form("add_client"):
            name = st.text_input("Company Name")
            industry = st.text_input("Industry")
            email = st.text_input("Contact Email")
            phone = st.text_input("Contact Phone")
            annual_value = st.number_input("Annual Value ($)", min_value=0.0, step=1000.0)
            status = st.selectbox("Status", ["prospect", "active", "closed"])

            if st.form_submit_button("Add Client"):
                if not name:
                    st.error("Company name is required")
                else:
                    try:
                        conn = get_db_connection()
                        cur = conn.cursor()

                        cur.execute("""
                            INSERT INTO clients (name, industry, contact_email, contact_phone, annual_value, status)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (name, industry, email, phone, annual_value, status))

                        conn.commit()
                        cur.close()
                        st.success(f"✅ {name} added!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding client: {e}")

elif page == "Projects":
    st.title("🚀 Projects")

    tab1, tab2 = st.tabs(["View", "Add New"])

    with tab1:
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("""
                SELECT p.*, c.name as client_name
                FROM projects p
                LEFT JOIN clients c ON p.client_id = c.id
                ORDER BY p.created_at DESC
            """)
            projects = cur.fetchall()

            if projects:
                for project in projects:
                    with st.expander(f"**{project['title']}** • {project['status']}"):
                        st.write(f"📋 Client: {project['client_name']}")
                        st.write(f"📝 {project['description']}")
                        col1, col2 = st.columns(2)
                        col1.write(f"⏱️ Estimated: {project['estimated_hours']}h")
                        col2.write(f"✅ Actual: {project['actual_hours']}h")
            else:
                st.info("No projects yet. Add one using the 'Add New' tab.")

            cur.close()
        except Exception as e:
            st.error(f"Error loading projects: {e}")

    with tab2:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM clients")
            clients = {c['id']: c['name'] for c in cur.fetchall()}
            cur.close()

            if not clients:
                st.warning("No clients yet. Add one in the Clients tab first.")
            else:
                with st.form("add_project"):
                    title = st.text_input("Project Title")
                    client_id = st.selectbox("Client", options=list(clients.keys()), format_func=lambda x: clients[x])
                    description = st.text_area("Description")
                    status = st.selectbox("Status", ["proposal", "active", "completed"])
                    estimated_hours = st.number_input("Estimated Hours", min_value=0, step=10)

                    if st.form_submit_button("Add Project"):
                        if not title:
                            st.error("Project title is required")
                        else:
                            try:
                                conn = get_db_connection()
                                cur = conn.cursor()

                                cur.execute("""
                                    INSERT INTO projects (client_id, title, description, status, estimated_hours)
                                    VALUES (?, ?, ?, ?, ?)
                                """, (client_id, title, description, status, estimated_hours))

                                conn.commit()
                                cur.close()
                                st.success(f"✅ {title} added!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error adding project: {e}")
        except Exception as e:
            st.error(f"Error loading clients: {e}")

elif page == "Settings":
    st.title("⚙️ Settings")
    st.write("✅ Database: SQLite")
    st.write(f"📍 Database Path: {DB_PATH}")
    st.write("Ready to deploy and iterate!")
