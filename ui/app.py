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
import hashlib

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
    
    .student-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
        border-left: 5px solid #4b4bff;
    }
    
    .personal-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
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
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""  # 'student' or 'admin'
if 'student_id' not in st.session_state:
    st.session_state.student_id = ""

# --- Initialize Manager ---
manager = StudentManager("data/students.json")

# --- User Authentication System ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Sample user database (in real app, use proper database)
USER_DATABASE = {
    # Students - passwords are their student IDs
    "s001": {"password": hash_password("s001"), "role": "student", "student_id": "S001"},
    "s002": {"password": hash_password("s002"), "role": "student", "student_id": "S002"},
    "s003": {"password": hash_password("s003"), "role": "student", "student_id": "S003"},
    # Admin
    "admin": {"password": hash_password("admin123"), "role": "admin", "student_id": None}
}

def authenticate_user(username, password):
    """Authenticate user and return user info"""
    if username in USER_DATABASE:
        hashed_password = hash_password(password)
        if USER_DATABASE[username]["password"] == hashed_password:
            return USER_DATABASE[username]
    return None

def get_student_by_username(username):
    """Get student details by username"""
    if username in USER_DATABASE:
        student_id = USER_DATABASE[username]["student_id"]
        return manager.find_by_id(student_id)
    return None

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
    
    # Show login status and user info
    if st.session_state.logged_in:
        if st.session_state.user_role == "student":
            student = get_student_by_username(st.session_state.username)
            if student:
                st.success(f"👋 Welcome, {student.name}!")
                st.info(f"🎓 Grade: {student.grade} | 📚 Student ID: {student.id}")
        else:
            st.success(f"👑 Welcome, Admin!")
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
        if st.button("👤 Profile", use_container_width=True):
            st.session_state.page = "Profile"
            st.rerun()
    
    if st.session_state.user_role == "admin":
        if st.button("👥 All Students", use_container_width=True):
            st.session_state.page = "AllStudents"
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
            st.session_state.user_role = ""
            st.session_state.student_id = ""
            st.session_state.page = "Home"
            st.success("Logged out successfully!")
            time.sleep(1)
            st.rerun()
    
    st.markdown("---")
    
    # Quick Stats (only show for admin)
    if st.session_state.logged_in and st.session_state.user_role == "admin":
        students = manager.list_students()
        st.markdown("### 📊 Quick Stats")
        st.metric("Total Students", len(students))
        if students:
            avg_gpa = sum(s.gpa for s in students) / len(students)
            st.metric("Average GPA", f"{avg_gpa:.1f}")

# --- Page Content ---
def login_page():
    st.title("🔐 Student Login")
    st.markdown("---")
    
    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username and password:
                user_info = authenticate_user(username, password)
                if user_info:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_role = user_info["role"]
                    st.session_state.student_id = user_info["student_id"]
                    st.session_state.page = "Home"
                    st.success("✅ Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            else:
                st.error("❌ Please enter both username and password")
    
    # Demo credentials
    with st.expander("📋 Demo Credentials"):
        st.markdown("""
        **Students (Login with student ID as both username and password):**
        - Username: `s001` | Password: `s001`
        - Username: `s002` | Password: `s002` 
        - Username: `s003` | Password: `s003`
        
        **Admin:**
        - Username: `admin` | Password: `admin123`
        """)

def student_dashboard(student):
    """Display personalized student dashboard"""
    st.markdown("### 🎯 Your Dashboard")
    
    # Personal Info Card
    st.markdown(f"""
    <div class="personal-info">
        <h3>👤 {student.name}</h3>
        <p><strong>Student ID:</strong> {student.id} | <strong>Grade:</strong> {student.grade}</p>
        <p><strong>Age:</strong> {student.age} | <strong>GPA:</strong> {student.gpa}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Performance Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 GPA Score", f"{student.gpa}")
    
    with col2:
        st.metric("🎓 Grade", student.grade)
    
    with col3:
        st.metric("📅 Age", student.age)
    
    with col4:
        # GPA status indicator
        status = "Excellent" if student.gpa >= 90 else "Good" if student.gpa >= 75 else "Needs Improvement"
        st.metric("📈 Status", status)
    
    # Progress Chart
    st.markdown("### 📊 Your Performance")
    
    # Create a simple progress chart for the student
    fig = px.bar(
        x=["Your GPA", "Class Average"],
        y=[student.gpa, 75],  # Assuming class average is 75
        title="Your GPA vs Class Average",
        color=["Your GPA", "Class Average"],
        color_discrete_map={"Your GPA": "#4b4bff", "Class Average": "#ff6b6b"}
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def home_page():
    # Header with Logo
    col_logo, col_title = st.columns([1, 4])
    
    with col_logo:
        logo, _ = load_logo()
        if logo:
            st.image(logo, width=100)
    
    with col_title:
        st.title("📚 Learning Management System")
        if st.session_state.logged_in:
            if st.session_state.user_role == "student":
                student = get_student_by_username(st.session_state.username)
                if student:
                    st.subheader(f"Welcome back, {student.name}! 👋")
            else:
                st.subheader("Admin Dashboard 👑")
        else:
            st.subheader("Manage your academic journey!")
    
    if not st.session_state.logged_in:
        st.warning("🔒 Please login to access your personalized dashboard")
        return
    
    # Show different content based on user role
    if st.session_state.user_role == "student":
        student = get_student_by_username(st.session_state.username)
        if student:
            student_dashboard(student)
        else:
            st.error("Student record not found!")
    
    else:  # Admin view
        admin_dashboard()

def admin_dashboard():
    """Admin dashboard showing all students"""
    st.markdown("### 👑 Admin Dashboard")
    
    # Quick Actions
    st.markdown("#### 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 View All Students", use_container_width=True):
            st.session_state.page = "AllStudents"
            st.rerun()
    
    with col2:
        if st.button("➕ Add New Student", use_container_width=True):
            st.session_state.page = "AllStudents"
            st.rerun()
    
    with col3:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.page = "AllStudents"
            st.rerun()
    
    # Statistics
    students = manager.list_students()
    if students:
        st.markdown("### 📈 Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Students", len(students))
        
        with col2:
            avg_age = sum(s.age for s in students) / len(students)
            st.metric("Average Age", f"{avg_age:.1f}")
        
        with col3:
            avg_gpa = sum(s.gpa for s in students) / len(students)
            st.metric("Average GPA", f"{avg_gpa:.1f}")
        
        with col4:
            excellent = sum(1 for s in students if s.gpa >= 90)
            st.metric("Excellent (90+)", excellent)
        
        # Recent students
        st.markdown("### 👥 Recent Students")
        recent_students = students[-5:]  # Last 5 students
        for student in recent_students:
            with st.container():
                st.markdown(f"""
                <div class="student-card">
                    <h4>{student.name}</h4>
                    <p>ID: {student.id} | Grade: {student.grade} | Age: {student.age} | GPA: {student.gpa}</p>
                </div>
                """, unsafe_allow_html=True)

def profile_page():
    if not st.session_state.logged_in:
        st.warning("🔒 Please login to view your profile")
        return
    
    st.title("👤 Your Profile")
    st.markdown("---")
    
    if st.session_state.user_role == "student":
        student = get_student_by_username(st.session_state.username)
        if student:
            # Display student profile
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="font-size: 80px; margin-bottom: 20px;">🎓</div>
                    <h3>{student.name}</h3>
                    <p><strong>Student ID:</strong> {student.id}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 📋 Personal Information")
                st.write(f"**Full Name:** {student.name}")
                st.write(f"**Student ID:** {student.id}")
                st.write(f"**Age:** {student.age}")
                st.write(f"**Grade:** {student.grade}")
                st.write(f"**GPA Score:** {student.gpa}")
                st.write(f"**Notes:** {student.notes if student.notes else 'No notes available'}")
            
            # Academic performance
            st.markdown("### 📊 Academic Performance")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current GPA", f"{student.gpa}")
            
            with col2:
                # GPA interpretation
                if student.gpa >= 90:
                    status = "🎉 Excellent"
                    color = "green"
                elif student.gpa >= 75:
                    status = "👍 Good"
                    color = "blue"
                else:
                    status = "💪 Needs Improvement"
                    color = "orange"
                st.metric("Performance", status)
            
            with col3:
                st.metric("Grade Level", student.grade)
    
    else:  # Admin profile
        st.markdown("""
        <div style="text-align: center; padding: 40px;">
            <div style="font-size: 80px; margin-bottom: 20px;">👑</div>
            <h2>Administrator Account</h2>
            <p>You have full access to manage all student records and system settings.</p>
        </div>
        """, unsafe_allow_html=True)

def all_students_page():
    if not st.session_state.logged_in or st.session_state.user_role != "admin":
        st.error("🔒 Admin access required!")
        return
    
    # Your original student management code here (same as before)
    st.title("👥 Manage All Students")
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

def timetable_page():
    if not st.session_state.logged_in:
        st.warning("🔒 Please login to access timetable")
        return
    
    st.title("📅 Class Timetable")
    st.markdown("---")
    
    # Personalized timetable based on grade
    if st.session_state.user_role == "student":
        student = get_student_by_username(st.session_state.username)
        if student:
            st.info(f"📚 Your Timetable for Grade {student.grade}")
    
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

# --- Main App Logic ---
def main():
    # Show appropriate page based on session state
    if st.session_state.page == "Login":
        login_page()
    elif st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Profile":
        profile_page()
    elif st.session_state.page == "AllStudents":
        all_students_page()
    elif st.session_state.page == "Timetable":
        timetable_page()

if __name__ == "__main__":
    main()