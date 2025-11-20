import streamlit as st
import time
import random
import re
from datetime import datetime

# --- 1. إعدادات الصفحة (Wide Mode for LMS feel) ---
st.set_page_config(
    page_title="LMS - Université Constantine 3",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. قواعد البيانات والترجمة ---

# هيكل جامعة قسنطينة 3 (بيانات حقيقية)
const_3_data = {
    "Faculté de Médecine": ["Médecine", "Pharmacie", "Médecine Dentaire"],
    "Faculté d'Architecture et d'Urbanisme": ["Architecture", "Urbanisme", "Gestion des Villes"],
    "Faculté des Arts et de la Culture": ["Arts Plastiques", "Arts Dramatiques", "Cinéma"],
    "Faculté de Génie des Procédés": ["Génie Chimique", "Génie Pharmaceutique"],
    "Faculté des Sciences Politiques": ["Sciences Politiques", "Relations Internationales"],
    "Faculté des NTIC": ["Informatique (GL)", "Informatique (SI)", "Réseaux et Télécom"],
    "Institut de Gestion des Techniques Urbaines": ["Génie Urbain", "Gestion de la ville"]
}

levels = ["Licence 1", "Licence 2", "Licence 3", "Master 1", "Master 2", "Doctorat"]

tr = {
    "ar": {
        "dashboard": "لوحة القيادة",
        "market": "المكتبة الرقمية",
        "upload": "نشر الأبحاث (AI)",
        "quiz": "لعبة التلخيص",
        "settings": "الملف الشخصي",
        "logout": "خروج",
        "welcome": "أهلاً بك،",
        "points_balance": "رصيد المعرفة",
        "xp": "نقطة",
        "my_books_count": "كتبي",
        "level_status": "الحالة الأكاديمية",
        "active_student": "طالب نشط",
        "latest_books": "أحدث المصادر الأكاديمية",
        "buy": "شراء",
        "owned": "مملوك",
        "upload_title": "مركز رفع الأبحاث",
        "upload_sub": "سيقوم الذكاء الاصطناعي بتقييم المحتوى وتحديد سعره في السوق.",
        "login_title": "بوابة الدخول الموحد",
        "verify_msg": "رمز التحقق المرسل إلى: ",
        "faculty": "الكلية",
        "major": "التخصص"
    },
    "fr": {
        "dashboard": "Tableau de bord",
        "market": "Bibliothèque",
        "upload": "Publier (IA)",
        "quiz": "Jeu Résumé",
        "settings": "Profil",
        "logout": "Déconnexion",
        "welcome": "Bienvenue, ",
        "points_balance": "Solde de Points",
        "xp": "PTS",
        "my_books_count": "Mes Livres",
        "level_status": "Statut",
        "active_student": "Actif",
        "latest_books": "Dernières Ressources",
        "buy": "Acheter",
        "owned": "Acquis",
        "upload_title": "Centre de Publication",
        "upload_sub": "L'IA évaluera le contenu et fixera son prix.",
        "login_title": "Portail Authentification",
        "verify_msg": "Code envoyé à : ",
        "faculty": "Faculté",
        "major": "Spécialité"
    },
    "en": {
        "dashboard": "Dashboard",
        "market": "Library",
        "upload": "Upload (AI)",
        "quiz": "Quiz Game",
        "settings": "Profile",
        "logout": "Logout",
        "welcome": "Welcome, ",
        "points_balance": "Points Balance",
        "xp": "XP",
        "my_books_count": "My Books",
        "level_status": "Status",
        "active_student": "Active",
        "latest_books": "Latest Resources",
        "buy": "Buy",
        "owned": "Owned",
        "upload_title": "Upload Center",
        "upload_sub": "AI will evaluate content and set the price.",
        "login_title": "Login Portal",
        "verify_msg": "Code sent to: ",
        "faculty": "Faculty",
        "major": "Major"
    }
}

# --- 3. إدارة الحالة (Session State) ---
if 'users' not in st.session_state: st.session_state['users'] = {}
if 'books' not in st.session_state:
    st.session_state['books'] = [
        {"id": 1, "title": "Urbanisme Durable", "author": "Dr. Ahmed", "price": 50, "downloads": 120, "type": "PDF", "cover": "🏙️"},
        {"id": 2, "title": "Algorithmics 101", "author": "Prof. Sarah", "price": 60, "downloads": 45, "type": "PDF", "cover": "💻"},
        {"id": 3, "title": "Anatomie Générale", "author": "Faculté Méd", "price": 75, "downloads": 300, "type": "PDF", "cover": "🫀"},
        {"id": 4, "title": "Histoire de l'Art", "author": "Library", "price": 40, "downloads": 20, "type": "PDF", "cover": "🎨"}
    ]
if 'auth_state' not in st.session_state: st.session_state['auth_state'] = 'login'
if 'current_user' not in st.session_state: st.session_state['current_user'] = None
if 'lang' not in st.session_state: st.session_state['lang'] = 'ar'
if 'temp_email' not in st.session_state: st.session_state['temp_email'] = ''
if 'verification_code' not in st.session_state: st.session_state['verification_code'] = ''

def t(key): return tr[st.session_state['lang']][key]

# --- 4. التصميم الاحترافي (Moodle/LMS Style) ---
def apply_lms_css():
    font = "'Tajawal', sans-serif"
    direction = "rtl" if st.session_state['lang'] == 'ar' else "ltr"
    align = "right" if st.session_state['lang'] == 'ar' else "left"
    
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
        
        /* الهيكل العام */
        .stApp {{
            background-color: #f5f7fa; /* لون خلفية Moodle الرمادي الفاتح */
            font-family: {font};
        }}
        
        h1, h2, h3, h4, p, span, div {{
            font-family: {font} !important;
            direction: {direction};
            text-align: {align};
        }}

        /* القائمة الجانبية */
        section[data-testid="stSidebar"] {{
            background-color: #2c3e50; /* لون داكن احترافي */
            color: white;
        }}
        
        /* بطاقات الداشبورد (Stats Cards) */
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            border-left: 5px solid #3b82f6;
            margin-bottom: 20px;
        }}
        
        /* بطاقات الكتب (Course Cards) */
        .course-card {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            overflow: hidden;
            border: 1px solid #e1e4e8;
            height: 100%;
        }}
        .course-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        .card-header {{
            height: 100px;
            background: linear-gradient(135deg, #3b82f6, #1e3a8a);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
        }}
        .card-body {{
            padding: 15px;
        }}
        
        /* الأزرار */
        .stButton button {{
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
        }}
        
        /* شريط علوي (Fake Navbar) */
        .top-nav {{
            background: white;
            padding: 15px 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }}
        
        /* صفحة الدخول */
        .login-container {{
            max-width: 450px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
    </style>
    """, unsafe_allow_html=True)

apply_lms_css()

# --- 5. المنطق (Logic) ---
def validate_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

# --- 6. الواجهات (Views) ---

def login_view():
    # تصميم صفحة دخول مركزية ونظيفة
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="login-container">
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="color:#1e3a8a; margin:0;">Université Constantine 3</h1>
                <p style="color:#64748b;">Salah Boubnider | LMS Platform</p>
            </div>
        """, unsafe_allow_html=True)
        
        # اختيار اللغة
        l_col1, l_col2, l_col3 = st.columns(3)
        if l_col1.button("العربية"): st.session_state['lang'] = 'ar'; st.rerun()
        if l_col2.button("Français"): st.session_state['lang'] = 'fr'; st.rerun()
        if l_col3.button("English"): st.session_state['lang'] = 'en'; st.rerun()

        tab1, tab2 = st.tabs([t('login_title'), "تسجيل جديد"])
        
        with tab1:
            email = st.text_input("Email", key="l_email")
            password = st.text_input("Password", type="password", key="l_pass")
            if st.button("الدخول", type="primary"):
                if email in st.session_state['users'] and st.session_state['users'][email]['password'] == password:
                    code = str(random.randint(1000, 9999))
                    st.session_state['verification_code'] = code
                    st.session_state['temp_email'] = email
                    st.session_state['auth_state'] = 'verify'
                    st.rerun()
                else:
                    st.error("بيانات خاطئة")
        
        with tab2:
            s_name = st.text_input("الاسم الكامل")
            s_email = st.text_input("Email", key="s_email")
            s_pass = st.text_input("Password", type="password", key="s_pass")
            
            s_fac = st.selectbox(t('faculty'), list(const_3_data.keys()))
            s_spec = st.selectbox(t('major'), const_3_data[s_fac])
            s_lvl = st.selectbox("Level", levels)
            
            if st.button("إنشاء حساب"):
                if validate_email(s_email) and s_email not in st.session_state['users']:
                    st.session_state['users'][s_email] = {
                        "name": s_name, "password": s_pass, "faculty": s_fac,
                        "specialty": s_spec, "level": s_lvl, "points": 100,
                        "my_books": [], "avatar": "🎓"
                    }
                    st.success("تم التسجيل! سجل دخولك الآن.")
                else:
                    st.error("خطأ في البيانات")
        
        st.markdown("</div>", unsafe_allow_html=True)

def verify_view():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="login-container" style="text-align:center;">
            <h2>🔐 التحقق الأمني</h2>
            <p>{t('verify_msg')} <b>{st.session_state['temp_email']}</b></p>
            <div style="background:#fef3c7; padding:10px; border-radius:5px; margin:10px 0;">
                كود المحاكاة: <b>{st.session_state['verification_code']}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        code = st.text_input("Code", max_chars=4)
        if st.button("تأكيد"):
            if code == st.session_state['verification_code']:
                st.session_state['current_user'] = st.session_state['users'][st.session_state['temp_email']]
                st.session_state['auth_state'] = 'dashboard'
                st.rerun()
            else:
                st.error("الكود خاطئ")

def main_app():
    user = st.session_state['current_user']
    
    # --- Sidebar (LMS Navigation) ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135768.png", width=80)
        st.markdown(f"### {user['name']}")
        st.caption(f"{user['faculty']}")
        st.divider()
        
        # قائمة تنقل مثل Moodle
        menu = st.radio("", 
            [t('dashboard'), t('market'), t('upload'), t('quiz'), t('settings')],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button(t('logout')):
            st.session_state['auth_state'] = 'login'
            st.session_state['current_user'] = None
            st.rerun()

    # --- Top Navbar Simulation ---
    st.markdown(f"""
    <div class="top-nav">
        <div>
            <h3 style="margin:0; color:#1e3a8a;">🏛️ Université Constantine 3 LMS</h3>
        </div>
        <div style="display:flex; gap:20px; align-items:center;">
            <span style="background:#eff6ff; padding:5px 15px; border-radius:20px; color:#1e40af; font-weight:bold;">
                {user['points']} {t('xp')} 💎
            </span>
            <span>{user['avatar']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 1. Dashboard (لوحة القيادة) ---
    if menu == t('dashboard'):
        # بطاقات الإحصائيات
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <h4 style="color:gray;">{t('points_balance')}</h4>
                <h2 style="color:#3b82f6; margin:0;">{user['points']}</h2>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card" style="border-left-color: #10b981;">
                <h4 style="color:gray;">{t('my_books_count')}</h4>
                <h2 style="color:#10b981; margin:0;">{len(user['my_books'])}</h2>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stat-card" style="border-left-color: #f59e0b;">
                <h4 style="color:gray;">{t('level_status')}</h4>
                <h4 style="color:#f59e0b; margin:0;">{t('active_student')}</h4>
            </div>""", unsafe_allow_html=True)

        st.subheader(f"📚 {t('latest_books')}")
        
        # عرض الكتب بشكل شبكة (Grid)
        cols = st.columns(3)
        for i, book in enumerate(st.session_state['books'][:6]): # عرض أول 6 كتب فقط
            with cols[i % 3]:
                dyn_price = book['price'] + book['downloads']
                st.markdown(f"""
                <div class="course-card">
                    <div class="card-header">{book['cover']}</div>
                    <div class="card-body">
                        <h4>{book['title']}</h4>
                        <p style="font-size:0.8rem; color:gray;">{book['author']} | ⬇️ {book['downloads']}</p>
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="color:#d97706; font-weight:bold;">{dyn_price} XP</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                is_owned = any(b['id'] == book['id'] for b in user['my_books'])
                if is_owned:
                    st.button(f"✅ {t('owned')}", key=f"db_btn_{i}", disabled=True)
                else:
                    if st.button(f"{t('buy')}", key=f"db_btn_{i}"):
                        if user['points'] >= dyn_price:
                            user['points'] -= dyn_price
                            user['my_books'].append(book)
                            book['downloads'] += 1
                            st.toast("Added to library!", icon="🎉")
                            st.rerun()
                        else:
                            st.error("No points")
                st.write("") # Spacer

    # --- 2. Market (المكتبة) ---
    elif menu == t('market'):
        st.title(t('market'))
        # نفس منطق عرض الكتب ولكن لكل الكتب
        cols = st.columns(4)
        for i, book in enumerate(st.session_state['books']):
            with cols[i % 4]:
                dyn_price = book['price'] + book['downloads']
                st.markdown(f"""
                <div class="course-card">
                    <div class="card-header">{book['cover']}</div>
                    <div class="card-body">
                        <h5>{book['title']}</h5>
                        <p style="font-size:0.8rem;">{dyn_price} XP</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if not any(b['id'] == book['id'] for b in user['my_books']):
                    if st.button(t('buy'), key=f"mkt_{i}"):
                         if user['points'] >= dyn_price:
                            user['points'] -= dyn_price
                            user['my_books'].append(book)
                            book['downloads'] += 1
                            st.rerun()
                else:
                    st.button("✅", key=f"mkt_{i}", disabled=True)

    # --- 3. Upload (النشر) ---
    elif menu == t('upload'):
        st.markdown(f"""
        <div style="background:white; padding:30px; border-radius:15px; border:2px dashed #cbd5e1; text-align:center;">
            <h1>📤 {t('upload_title')}</h1>
            <p>{t('upload_desc')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        file = st.file_uploader("", type="pdf")
        title = st.text_input("Title / العنوان")
        
        if file and st.button("Start AI Analysis 🤖"):
            with st.spinner("AI analyzing academic quality..."):
                time.sleep(2)
                score = random.randint(60, 100)
                price = random.randint(40, 80)
                
                st.success(f"Approved! Quality Score: {score}%")
                st.info(f"Market Price set to: {price} XP")
                
                st.session_state['books'].append({
                    "id": len(st.session_state['books'])+1,
                    "title": title if title else "New Doc",
                    "author": user['name'],
                    "price": price,
                    "downloads": 0,
                    "type": "PDF",
                    "cover": "📄"
                })
                user['points'] += 15
                st.balloons()

    # --- 4. Quiz ---
    elif menu == t('quiz'):
        st.title(f"🧠 {t('quiz')}")
        if not user['my_books']:
            st.warning("Please buy books first.")
        else:
            bk = st.selectbox("Choose Book", [b['title'] for b in user['my_books']])
            if st.button("Generate AI Quiz"):
                with st.spinner("Reading book content..."):
                    time.sleep(1.5)
                st.markdown(f"### Question about: {bk}")
                st.write("What is the main hypothesis discussed in Chapter 2?")
                st.radio("Answer:", ["Option A", "Option B", "Option C"])
                if st.button("Submit Answer"):
                    if random.choice([True, False]):
                        user['points'] += 20
                        st.success("Correct! +20 XP")
                    else:
                        user['points'] -= 5
                        st.error("Wrong! -5 XP")

    # --- 5. Settings ---
    elif menu == t('settings'):
        st.title(t('settings'))
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Change Language")
            lc = st.radio("", ["العربية", "Français", "English"])
            if st.button("Save Language"):
                if lc == "العربية": st.session_state['lang'] = 'ar'
                elif lc == "Français": st.session_state['lang'] = 'fr'
                else: st.session_state['lang'] = 'en'
                st.rerun()
        with c2:
            st.markdown("### Profile Pic")
            av = st.selectbox("Avatar", ["🎓", "👨‍🏫", "👩‍🔬", "💻"])
            if st.button("Update Avatar"):
                user['avatar'] = av
                st.rerun()

# --- التشغيل الرئيسي ---
if st.session_state['auth_state'] == 'login':
    login_view()
elif st.session_state['auth_state'] == 'verify':
    verify_view()
else:
    main_app()
