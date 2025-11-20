import streamlit as st
import pandas as pd
import time
import random
import re
from datetime import datetime

# --- 1. إعدادات الصفحة (Professional Dashboard Layout) ---
st.set_page_config(
    page_title="LMS - Université Constantine 3",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. البيانات الهيكلية (Data Models) ---
FACULTIES = {
    "Faculté de Médecine": ["Médecine", "Pharmacie", "Dentaire"],
    "Faculté d'Architecture (Salah Boubnider)": ["Architecture", "Urbanisme", "Gestion des Villes"],
    "Faculté des NTIC": ["Génie Logiciel", "I.A", "Réseaux", "Systèmes Embarqués"],
    "Faculté des Arts": ["Arts Plastiques", "Cinéma", "Théâtre"],
    "Génie des Procédés": ["Chimie", "Biologie", "Pharmaceutique"]
}

# --- 3. المحرك البصري (Modern Python UI Engine) ---
def load_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;800&display=swap');
        
        :root {
            --primary: #2563eb;
            --secondary: #f8fafc;
            --text: #1e293b;
            --accent: #f59e0b;
        }

        /* Global Reset */
        .stApp {
            background-color: #f1f5f9;
            font-family: 'Tajawal', sans-serif;
            color: var(--text);
        }
        
        h1, h2, h3, h4, p, div, button, span {
            font-family: 'Tajawal', sans-serif !important;
        }

        /* Sidebar Professional Look */
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e2e8f0;
        }
        
        /* Cards & Containers */
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            border: 1px solid #e2e8f0;
            text-align: center;
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px rgba(0,0,0,0.05);
            border-color: var(--primary);
        }

        /* Course/Book Grid Item */
        .grid-item {
            background: white;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
            transition: transform 0.2s;
            margin-bottom: 20px;
        }
        .grid-item:hover {
            border-color: var(--primary);
            transform: scale(1.01);
        }
        .grid-header {
            height: 120px;
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
        }
        .grid-body {
            padding: 15px;
        }
        
        /* Custom Buttons */
        .stButton button {
            border-radius: 8px;
            font-weight: 600;
            border: none;
            transition: 0.2s;
        }
        
        /* Login Box */
        .auth-container {
            max-width: 400px;
            margin: 50px auto;
            padding: 40px;
            background: white;
            border-radius: 24px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
    </style>
    """, unsafe_allow_html=True)

load_custom_css()

# --- 4. إدارة الحالة (Session State) ---
if 'state' not in st.session_state:
    st.session_state['state'] = {
        'auth_status': 'login', # login, verify, authenticated
        'user': None,
        'lang': 'ar',
        'temp_email': '',
        'code': '',
        'users_db': {},
        'library': [
            {"id": 1, "title": "Python for Data Science", "author": "Dr. Amine", "price": 45, "downloads": 80, "icon": "🐍", "category": "NTIC"},
            {"id": 2, "title": "Urban Planning 101", "author": "Arch. Sara", "price": 55, "downloads": 25, "icon": "🏙️", "category": "Architecture"},
            {"id": 3, "title": "Clinical Anatomy", "author": "Fac. Médecine", "price": 70, "downloads": 150, "icon": "🫀", "category": "Médecine"}
        ]
    }

# اختصار للوصول للحالة
S = st.session_state['state']

# --- 5. الوظائف المنطقية (Backend Logic) ---
def verify_email_format(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def login_user(email, password):
    if email in S['users_db'] and S['users_db'][email]['password'] == password:
        S['temp_email'] = email
        S['code'] = str(random.randint(1000, 9999))
        S['auth_status'] = 'verify'
        return True
    return False

def register_user(name, email, password, fac, spec):
    if email in S['users_db']: return False
    S['users_db'][email] = {
        "name": name, "password": password, "faculty": fac, 
        "specialty": spec, "points": 100, "library": []
    }
    return True

# --- 6. واجهات المستخدم (UI Views) ---

def render_login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown("""
        <div class="auth-container">
            <div style="text-align:center; margin-bottom:20px;">
                <h1 style="color:#2563eb; margin:0;">UC3 Portal</h1>
                <p style="color:gray;">Student Academic Platform</p>
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            email = st.text_input("Email", key="l_email", placeholder="student@univ-constantine3.dz")
            password = st.text_input("Password", type="password", key="l_pass")
            if st.button("Secure Login", type="primary", use_container_width=True):
                if not login_user(email, password):
                    st.error("Invalid credentials or user not found.")
                else:
                    st.rerun()
        
        with tab2:
            r_name = st.text_input("Full Name")
            r_email = st.text_input("University Email", key="r_email")
            r_pass = st.text_input("New Password", type="password", key="r_pass")
            r_fac = st.selectbox("Faculty", list(FACULTIES.keys()))
            r_spec = st.selectbox("Major", FACULTIES[r_fac])
            
            if st.button("Create Account", type="secondary", use_container_width=True):
                if verify_email_format(r_email):
                    if register_user(r_name, r_email, r_pass, r_fac, r_spec):
                        st.success("Account created! Please login.")
                    else:
                        st.error("Email already exists.")
                else:
                    st.error("Invalid Email format.")
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_verify():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(f"""
        <div class="auth-container" style="text-align:center;">
            <h2>🔐 Security Check</h2>
            <p>We sent a code to <b>{S['temp_email']}</b></p>
            <div style="background:#fef9c3; padding:10px; border-radius:8px; margin:15px 0; color:#854d0e; font-weight:bold;">
                Simulation Code: {S['code']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        code_in = st.text_input("Enter 4-Digit Code", max_chars=4, key="v_code")
        if st.button("Verify Access", type="primary", use_container_width=True):
            if code_in == S['code']:
                S['user'] = S['users_db'][S['temp_email']]
                S['auth_status'] = 'authenticated'
                st.rerun()
            else:
                st.error("Wrong Code")

def render_app():
    user = S['user']
    
    # --- Sidebar ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135768.png", width=50)
        st.markdown(f"### {user['name']}")
        st.caption(f"{user['faculty']} | {user['specialty']}")
        
        # Live Wallet Widget
        st.markdown(f"""
        <div style="background:#eff6ff; padding:15px; border-radius:10px; border:1px solid #bfdbfe; margin-bottom:20px;">
            <p style="margin:0; color:#1e40af; font-size:0.8rem;">Current Balance</p>
            <h2 style="margin:0; color:#1d4ed8;">{user['points']} XP</h2>
        </div>
        """, unsafe_allow_html=True)
        
        nav = st.radio("MENU", ["Dashboard", "Library (Market)", "Upload Center (AI)", "Quiz Challenge", "Profile"], label_visibility="collapsed")
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            S['auth_status'] = 'login'
            S['user'] = None
            st.rerun()

    # --- Main Content Area ---
    
    # 1. Dashboard
    if nav == "Dashboard":
        st.title("📊 Dashboard Overview")
        
        # KPI Metrics
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total XP", user['points'], "+10 today")
        k2.metric("Library Books", len(user['library']), "Owned")
        k3.metric("Academic Rank", "Scholar", "Level 2")
        k4.metric("Completed Quizzes", "3", "+1 this week")
        
        st.markdown("### 📅 Recent Activity")
        st.info("Welcome back! New academic resources in 'Architecture' are trending.")

    # 2. Library (The Market)
    elif nav == "Library (Market)":
        st.title("📚 Academic Market")
        
        # Filter & Search
        col_s1, col_s2 = st.columns([3, 1])
        search = col_s1.text_input("Search resources...", placeholder="Python, Anatomy, etc.")
        sort = col_s2.selectbox("Sort by", ["Popularity", "Price: Low to High"])
        
        # Books Grid
        cols = st.columns(3)
        for i, book in enumerate(S['library']):
            dynamic_price = book['price'] + int(book['downloads'] * 0.1) # Dynamic pricing algorithm
            
            with cols[i % 3]:
                st.markdown(f"""
                <div class="grid-item">
                    <div class="grid-header">{book['icon']}</div>
                    <div class="grid-body">
                        <div style="display:flex; justify-content:space-between;">
                            <span style="background:#f1f5f9; padding:2px 8px; border-radius:10px; font-size:0.7rem;">{book['category']}</span>
                            <span style="color:gray; font-size:0.8rem;">⬇️ {book['downloads']}</span>
                        </div>
                        <h4 style="margin:10px 0; color:#1e293b;">{book['title']}</h4>
                        <p style="color:gray; font-size:0.9rem;">{book['author']}</p>
                        <h3 style="color:#d97706;">{dynamic_price} XP</h3>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Buy Logic
                is_owned = any(b['id'] == book['id'] for b in user['library'])
                if is_owned:
                    st.button("✅ Owned", key=f"btn_{i}", disabled=True, use_container_width=True)
                else:
                    if st.button(f"Buy Now", key=f"btn_{i}", use_container_width=True):
                        if user['points'] >= dynamic_price:
                            user['points'] -= dynamic_price
                            user['library'].append(book)
                            book['downloads'] += 1
                            st.toast(f"Successfully bought {book['title']}!", icon="🎉")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Insufficient XP Balance")

    # 3. Upload Center (AI Simulation)
    elif nav == "Upload Center (AI)":
        st.title("📤 AI Publication Center")
        
        col_u1, col_u2 = st.columns([1, 1])
        
        with col_u1:
            st.markdown("""
            <div class="metric-card" style="text-align:left;">
                <h3>How it works?</h3>
                <ol>
                    <li>Upload your PDF research/summary.</li>
                    <li><b>AI Engine</b> scans for academic relevance.</li>
                    <li>System assigns a <b>Quality Score</b>.</li>
                    <li>Price is set automatically based on score.</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        
        with col_u2:
            uploaded = st.file_uploader("Drop your PDF here", type="pdf")
            title = st.text_input("Resource Title")
            
            if uploaded and st.button("Start Analysis 🚀", use_container_width=True):
                progress = st.progress(0)
                status = st.empty()
                
                status.write("🔍 Scanning document structure...")
                time.sleep(1)
                progress.progress(30)
                
                status.write("🧠 Analyzing semantic content...")
                time.sleep(1)
                progress.progress(70)
                
                status.write("💰 Calculating market value...")
                time.sleep(1)
                progress.progress(100)
                
                # Results
                score = random.randint(65, 99)
                price = int(score * 0.8)
                
                st.success(f"Analysis Complete! Quality Score: {score}/100")
                st.metric("Market Value", f"{price} XP", "+10 XP Bonus for you")
                
                user['points'] += 10
                S['library'].append({
                    "id": len(S['library'])+1,
                    "title": title if title else "New User Upload",
                    "author": user['name'],
                    "price": price,
                    "downloads": 0,
                    "icon": "📄",
                    "category": user['specialty']
                })
                st.balloons()

    # 4. Quiz
    elif nav == "Quiz Challenge":
        st.title("🧠 Active Recall Quiz")
        
        if not user['library']:
            st.warning("Please purchase a book from the library first to generate a quiz.")
        else:
            selected_book = st.selectbox("Select a resource to review:", [b['title'] for b in user['library']])
            
            if st.button("Generate AI Quiz", type="primary"):
                with st.spinner("Generating questions..."):
                    time.sleep(1.5)
                
                st.markdown(f"### Topic: {selected_book}")
                st.markdown("**Q1: What is the core concept discussed in Chapter 1 regarding this topic?**")
                
                ans = st.radio("Select the best answer:", [
                    "The theoretical framework of modern systems.",
                    "The historical context of the 19th century.",
                    "The basic syntax and variable definitions."
                ])
                
                if st.button("Submit Answer"):
                    if random.choice([True, False]):
                        st.success("Correct! You earned +20 XP")
                        user['points'] += 20
                    else:
                        st.error("Incorrect. Try reading the summary again. -5 XP")
                        user['points'] -= 5

    # 5. Profile
    elif nav == "Profile":
        st.title("⚙️ Settings")
        st.text_input("Full Name", value=user['name'])
        st.text_input("Email", value=S['temp_email'], disabled=True)
        st.selectbox("Language", ["English", "Français", "العربية"])
        st.button("Save Changes")

# --- Main Execution Flow ---
if S['auth_status'] == 'login':
    render_login()
elif S['auth_status'] == 'verify':
    render_verify()
else:
    render_app()
