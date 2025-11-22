# ui/app.py
import sys
import os
# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from services.manager import StudentManager
import pandas as pd
from PIL import Image
import plotly.express as px
import time

# --- Page Config ---
st.set_page_config(
    page_title="Learning Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        background-color: #f5f5f8;
    }
    
    h1, h2, h3 {
        color: #4b4bff;
        font-family: 'Arial Black', sans-serif;
    }
    
    .stButton > button {
        background-color: #4b4bff;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 8px 16px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #3a3aff;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .logo-placeholder {
        background: linear-gradient(135deg, #4b4bff, #6c63ff);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        color: white;
        margin: 10px 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    
    /* Navigation buttons */
    .nav-btn {
        width: 100%;
        margin: 5px 0;
        text-align: left;
        padding: 12px 15px;
        border-radius: 8px;
        border: none;
        background: white;
        color: #333;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .nav-btn:hover {
        background: #4b4bff;
        color: white;
        transform: translateX(5px);
    }
    
    .nav-btn.active {
        background: #4b4bff;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# --- Initialize Manager ---
manager = StudentManager("data/students.json")

# --- Logo Loading Function ---
def load_logo():
    """Try multiple paths to find the logo"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    possible_files = ["smit.png", "image.png", "logo.png"]
    possible_paths = []
    
    for filename in possible_files:
        possible_paths.extend([
            os.path.join(project_root, filename),
            os.path.join(current_dir, filename),
            os.path.join(project_root, "data", filename),
            filename,
            f"../{filename}",
            f"../../{filename}",
        ])
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                logo = Image.open(path)
                return logo, path
        except:
            continue
    return None, None

# --- Sidebar Navigation ---
with st.sidebar:
    # Logo in sidebar
    logo, logo_path = load_logo()
    if logo:
        st.image(logo, width=120)
    else:
        st.markdown("""
        <div style="text-align: center; background: linear-gradient(135deg, #4b4bff, #6c63ff); 
                    border-radius: 15px; padding: 15px; color: white; margin: 10px 0;">
            <h3>🏫 LMS</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Show login status
    if st.session_state.logged_in:
        st.success(f"👋 Welcome, {st.session_state.username}!")
        st.markdown("---")
    
    # Navigation Menu
    st.markdown("### 📱 Navigation")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
    
    with col2:
        if st.button("👥 Accounts", use_container_width=True):
            st.session_state.page = "Accounts"
            st.rerun()
    
    if st.button("📅 Timetable", use_container_width=True):
        st.session_state.page = "Timetable"
        st.rerun()
    
    # Login/Logout button
    if not st.session_state.logged_in:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()
    else:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.page = "Home"
            st.success("Logged out successfully!")
            time.sleep(1)
            st.rerun()
    
    st.markdown("---")
    
    # Quick Stats (only show when logged in)
    if st.session_state.logged_in:
        students = manager.list_students()
        st.markdown("### 📊 Quick Stats")
        st.metric("Total Students", len(students))
        if students:
            avg_gpa = sum(s.gpa for s in students) / len(students)
            st.metric("Average GPA", f"{avg_gpa:.1f}")

# --- Page Content ---
def login_page():
    st.title("🔐 Login")
    st.markdown("---")
    
    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username and password:
                # Simple authentication (in real app, use proper auth)
                if username == "admin" and password == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.page = "Home"
                    st.success("✅ Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            else:
                st.error("❌ Please enter both username and password")
    
    # Demo credentials
    with st.expander("Demo Credentials"):
        st.write("**Username:** admin")
        st.write("**Password:** admin123")

def home_page():
    # Header with Logo
    col_logo, col_title = st.columns([1, 4])
    
    with col_logo:
        logo, _ = load_logo()
        if logo:
            st.image(logo, width=100)
    
    with col_title:
        st.title("📚 Learning Management System")
        st.subheader("Manage your students easily!")
    
    # Welcome message
    if st.session_state.logged_in:
        st.success(f"Welcome back, {st.session_state.username}! 👋")
    else:
        st.warning("Please login to access all features")
    
    # Quick Actions
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 View Students", use_container_width=True):
            st.session_state.page = "Accounts"
            st.rerun()
    
    with col2:
        if st.button("➕ Add Student", use_container_width=True):
            st.session_state.page = "Accounts"
            st.rerun()
    
    with col3:
        if st.button("📅 Timetable", use_container_width=True):
            st.session_state.page = "Timetable"
            st.rerun()
    
    with col4:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.page = "Accounts"
            st.rerun()
    
    # Recent Activity/Stats
    if st.session_state.logged_in:
        students = manager.list_students()
        if students:
            st.markdown("### 📈 Overview")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Students", len(students))
            
            with col2:
                avg_age = sum(s.age for s in students) / len(students)
                st.metric("Average Age", f"{avg_age:.1f}")
            
            with col3:
                avg_gpa = sum(s.gpa for s in students) / len(students)
                st.metric("Average GPA", f"{avg_gpa:.1f}")

def accounts_page():
    if not st.session_state.logged_in:
        st.warning("🔒 Please login to access student accounts")
        return
    
    st.title("👥 Student Accounts")
    st.markdown("---")
    
    # Add student form
    with st.expander("➕ Add New Student", expanded=False):
        with st.form("add_student_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full name", placeholder="Enter student's full name")
                age = st.number_input("Age", min_value=3, max_value=120, value=15, step=1)
                grade = st.text_input("Grade (e.g., 10, A, Year 2)", placeholder="10")
            
            with col2:
                gpa = st.number_input("GPA / Score (0-100)", min_value=0.0, max_value=100.0, value=75.0, step=0.1)
                notes = st.text_area("Notes (optional)", placeholder="Additional notes about the student...")
            
            submitted = st.form_submit_button("🎯 Add Student")
            if submitted:
                if not name.strip():
                    st.error("❌ Please enter a student name")
                else:
                    try:
                        new = manager.add_student({
                            "id": "", "name": name.strip(), "age": int(age),
                            "grade": grade.strip(), "gpa": float(gpa), "notes": notes.strip()
                        })
                        st.success(f"✅ Student added: **{new.name}** (ID: {new.id})")
                    except Exception as e:
                        st.error(f"❌ Error adding student: {e}")

    # Search & Filter Section
    st.subheader("🔎 Search & Filters")
    
    search_col1, search_col2, search_col3, search_col4 = st.columns([3, 2, 2, 2])
    with search_col1:
        search_q = st.text_input("Search students", placeholder="Search by name, ID, grade, or notes...")
    with search_col2:
        min_age = st.number_input("Min age", min_value=0, max_value=200, value=0, step=1)
    with search_col3:
        max_age = st.number_input("Max age", min_value=0, max_value=200, value=100, step=1)
    with search_col4:
        min_gpa = st.number_input("Min score", min_value=0.0, max_value=100.0, value=0.0, step=0.1)

    grade_filter = st.text_input("Filter by grade", placeholder="Enter exact grade to filter...")

    # Process filters
    if search_q:
        students = manager.search(search_q)
    else:
        students = manager.list_students()

    students = manager.filter(
        min_age=(min_age if min_age > 0 else None),
        max_age=(max_age if max_age < 100 else None),
        min_gpa=(min_gpa if min_gpa > 0 else None),
        grade=(grade_filter if grade_filter.strip() else None)
    )

    # Display Results
    st.subheader(f"📋 Student Records ({len(students)} found)")

    if not students:
        st.info("👋 No students found. Add some students to get started!")
    else:
        df = pd.DataFrame([s.to_dict() for s in students])
        st.dataframe(df, use_container_width=True)
        
        # Charts Section
        st.markdown("---")
        st.subheader("📊 Student Analytics")
        
        if not df.empty:
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                fig_gpa = px.bar(df, x="name", y="gpa", color="grade", 
                                title="Student GPA Distribution", 
                                color_discrete_sequence=px.colors.qualitative.Bold)
                fig_gpa.update_layout(xaxis_title="Student Name", yaxis_title="GPA Score")
                st.plotly_chart(fig_gpa, use_container_width=True)
            
            with chart_col2:
                fig_age = px.pie(df, names="grade", title="Students by Grade Level",
                               color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig_age, use_container_width=True)

    # Update / Delete Section
    st.markdown("---")
    st.subheader("✏️ Update / Delete Student")

    all_students = manager.list_students()
    if all_students:
        options = {f"{s.name} (ID: {s.id}, Grade: {s.grade})": s.id for s in all_students}
        selected_key = st.selectbox("Choose student to edit", options=[""] + list(options.keys()))
        
        if selected_key:
            student_id = options[selected_key]
            student = manager.find_by_id(student_id)
            
            if student:
                with st.form("update_student_form"):
                    st.write(f"**Editing:** {student.name}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        name2 = st.text_input("Name", value=student.name)
                        age2 = st.number_input("Age", min_value=3, max_value=120, value=student.age)
                        grade2 = st.text_input("Grade", value=student.grade)
                    
                    with col2:
                        gpa2 = st.number_input("GPA / Score", min_value=0.0, max_value=100.0, value=student.gpa, step=0.1)
                        notes2 = st.text_area("Notes", value=student.notes)
                    
                    update_btn = st.form_submit_button("💾 Update Student")
                    delete_btn = st.form_submit_button("🗑️ Delete Student")
                    
                    if update_btn:
                        if not name2.strip():
                            st.error("❌ Please enter a student name")
                        else:
                            try:
                                updated = manager.update_student(student_id, {
                                    "name": name2.strip(), "age": int(age2), "grade": grade2.strip(),
                                    "gpa": float(gpa2), "notes": notes2.strip()
                                })
                                st.success(f"✅ Successfully updated **{updated.name}**")
                            except Exception as e:
                                st.error(f"❌ Update failed: {e}")
                    
                    if delete_btn:
                        if manager.delete_student(student_id):
                            st.success("✅ Student deleted successfully.")
                            st.rerun()
                        else:
                            st.error("❌ Delete failed.")
    else:
        st.info("No students available. Add some students to enable editing.")

def timetable_page():
    if not st.session_state.logged_in:
        st.warning("🔒 Please login to access timetable")
        return
    
    st.title("📅 Class Timetable")
    st.markdown("---")
    
    # Sample timetable data
    timetable_data = {
        "Time": ["9:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-1:00", "1:00-2:00", "2:00-3:00"],
        "Monday": ["Mathematics", "Science", "English", "Lunch", "History", "Art"],
        "Tuesday": ["English", "Mathematics", "Science", "Lunch", "PE", "Music"],
        "Wednesday": ["Science", "English", "Mathematics", "Lunch", "Geography", "Drama"],
        "Thursday": ["Mathematics", "Art", "Science", "Lunch", "English", "PE"],
        "Friday": ["English", "History", "Mathematics", "Lunch", "Science", "Club Activities"]
    }
    
    df_timetable = pd.DataFrame(timetable_data)
    st.dataframe(df_timetable, use_container_width=True)
    
    # Add timetable management
    with st.expander("🔄 Manage Timetable"):
        st.write("Add timetable management functionality here")
        new_class = st.text_input("Add new class")
        if st.button("Add Class"):
            if new_class:
                st.success(f"Added {new_class} to timetable")

# --- Main App Logic ---
def main():
    # Show appropriate page based on session state
    if st.session_state.page == "Login":
        login_page()
    elif st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Accounts":
        accounts_page()
    elif st.session_state.page == "Timetable":
        timetable_page()

if __name__ == "__main__":
    main()