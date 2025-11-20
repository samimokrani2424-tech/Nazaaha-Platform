import streamlit as st
import time
import random
import re
from datetime import datetime

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="بوابة الطالب | جامعة قسنطينة 3",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. قواعد البيانات (الهيكل الأكاديمي والترجمة) ---

# هيكل جامعة قسنطينة 3 (صالح بوبنيدر)
const_3_data = {
    "Faculté de Médecine": ["Médecine", "Pharmacie", "Médecine Dentaire"],
    "Faculté d'Architecture et d'Urbanisme": ["Architecture", "Urbanisme", "Gestion des Villes"],
    "Faculté des Arts et de la Culture": ["Arts Plastiques", "Arts Dramatiques", "Cinéma"],
    "Faculté de Génie des Procédés": ["Génie Chimique", "Génie Pharmaceutique"],
    "Faculté des Sciences Politiques": ["Sciences Politiques", "Relations Internationales"],
    "Faculté des NTIC": ["Informatique (GL)", "Informatique (SI)", "Réseaux et Télécom"],
    "Institut de Gestion des Techniques Urbaines": ["Génie Urbain", "Gestion de la ville"]
}

levels = ["Licence", "Master 1", "Master 2", "Doctorat", "École Supérieure"]

# قاموس الترجمة (عربي - فرنسي - إنجليزي)
tr = {
    "ar": {
        "login": "تسجيل الدخول",
        "signup": "تسجيل طالب جديد",
        "email": "البريد الإلكتروني الجامعي",
        "pass": "كلمة المرور",
        "name": "الاسم الكامل",
        "faculty": "الكلية",
        "specialty": "التخصص",
        "level": "المستوى الدراسي",
        "login_btn": "دخول آمن",
        "signup_btn": "إنشاء حساب أكاديمي",
        "verify_title": "التحقق الأمني",
        "verify_msg": "تم إرسال رمز التحقق إلى بريدك الإلكتروني: ",
        "code_label": "أدخل الرمز (4 أرقام)",
        "verify_btn": "تأكيد الدخول",
        "welcome": "مرحباً بك في فضاء المعرفة",
        "market": "المكتبة الرقمية",
        "upload": "نشر وتقييم (AI)",
        "quiz": "لعبة 'لخص لي'",
        "settings": "الإعدادات",
        "logout": "خروج",
        "buy": "شراء",
        "price": "السعر",
        "points": "نقطة",
        "downloads": "تحميل",
        "upload_title": "نشر محتوى أكاديمي",
        "upload_desc": "سيقوم الذكاء الاصطناعي بتحليل الملف وتحديد سعره.",
        "quiz_title": "اختبر فهمك واربح النقاط",
        "quiz_btn": "توليد كويز (AI)",
        "lang": "اللغة / Language",
        "fb_link": "ربط حساب Facebook",
        "interests": "الاهتمامات العلمية"
    },
    "fr": {
        "login": "Connexion",
        "signup": "Inscription",
        "email": "Email Universitaire",
        "pass": "Mot de passe",
        "name": "Nom Complet",
        "faculty": "Faculté",
        "specialty": "Spécialité",
        "level": "Niveau",
        "login_btn": "Connexion Sécurisée",
        "signup_btn": "Créer un compte",
        "verify_title": "Vérification de Sécurité",
        "verify_msg": "Code envoyé à votre email : ",
        "code_label": "Entrez le code (4 chiffres)",
        "verify_btn": "Confirmer",
        "welcome": "Bienvenue dans votre espace",
        "market": "Bibliothèque Numérique",
        "upload": "Publier & Évaluer (IA)",
        "quiz": "Jeu 'Résume-moi'",
        "settings": "Paramètres",
        "logout": "Déconnexion",
        "buy": "Acheter",
        "price": "Prix",
        "points": "pts",
        "downloads": "téléchargements",
        "upload_title": "Publier du contenu académique",
        "upload_desc": "L'IA analysera le fichier et fixera son prix.",
        "quiz_title": "Testez vos connaissances",
        "quiz_btn": "Générer Quiz (IA)",
        "lang": "Langue / Language",
        "fb_link": "Lier Facebook",
        "interests": "Intérêts Scientifiques"
    },
    "en": {
        "login": "Login",
        "signup": "New Student Registration",
        "email": "University Email",
        "pass": "Password",
        "name": "Full Name",
        "faculty": "Faculty",
        "specialty": "Major",
        "level": "Level",
        "login_btn": "Secure Login",
        "signup_btn": "Create Account",
        "verify_title": "Security Verification",
        "verify_msg": "Verification code sent to: ",
        "code_label": "Enter Code (4 digits)",
        "verify_btn": "Confirm",
        "welcome": "Welcome to Knowledge Space",
        "market": "Digital Library",
        "upload": "Upload & AI Rate",
        "quiz": "'Summarize Me' Game",
        "settings": "Settings",
        "logout": "Logout",
        "buy": "Buy",
        "price": "Price",
        "points": "pts",
        "downloads": "downloads",
        "upload_title": "Upload Academic Content",
        "upload_desc": "AI will analyze the file and set the price.",
        "quiz_title": "Test your knowledge",
        "quiz_btn": "Generate Quiz (AI)",
        "lang": "Language",
        "fb_link": "Link Facebook",
        "interests": "Scientific Interests"
    }
}

# --- 3. إدارة الحالة (Session State) ---
# تهيئة المتغيرات لضمان عدم حدوث أخطاء عند التحديث
if 'users' not in st.session_state:
    st.session_state['users'] = {}
if 'books' not in st.session_state:
    st.session_state['books'] = [
        {"id": 1, "title": "Architecture Islamique", "author": "System", "price": 45, "downloads": 12, "type": "PDF"},
        {"id": 2, "title": "Introduction à l'AI", "author": "System", "price": 55, "downloads": 30, "type": "PDF"},
    ]
if 'auth_state' not in st.session_state: st.session_state['auth_state'] = 'login' 
if 'current_user' not in st.session_state: st.session_state['current_user'] = None
if 'temp_email' not in st.session_state: st.session_state['temp_email'] = ''
if 'verification_code' not in st.session_state: st.session_state['verification_code'] = ''
if 'lang' not in st.session_state: st.session_state['lang'] = 'ar'

def t(key):
    return tr[st.session_state['lang']][key]

# --- 4. التصميم البصري (CSS) ---
def apply_css():
    font_family = "'Tajawal', sans-serif"
    # ضبط الاتجاه بناءً على اللغة المختارة
    direction = "rtl" if st.session_state['lang'] == 'ar' else "ltr"
    align = "right" if st.session_state['lang'] == 'ar' else "left"
    
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
        
        .stApp {{
            font-family: {font_family};
            background-color: #f3f4f6;
        }}
        
        h1, h2, h3, h4, p, div, span, button, input {{
            font-family: {font_family} !important;
            direction: {direction};
            text-align: {align};
        }}
        
        /* بطاقة تسجيل الدخول */
        .login-card {{
            background: white;
            padding: 3rem;
            border-radius: 25px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            border: 1px solid #e5e7eb;
        }}
        
        /* كروت الكتب */
        .book-card {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            transition: transform 0.3s ease;
            margin-bottom: 15px;
            border-right: 5px solid #3b82f6;
        }}
        .book-card:hover {{
            transform: translateY(-5px);
        }}
        
        /* الأزرار */
        .stButton button {{
            background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: all 0.3s;
        }}
        .stButton button:hover {{
            box-shadow: 0 5px 15px rgba(37, 99, 235, 0.3);
        }}
        
        /* شارات */
        .badge {{
            background-color: #dbeafe;
            color: #1e40af;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
        }}
        
        /* حقول الإدخال */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] {{
            border-radius: 10px;
            border: 1px solid #d1d5db;
        }}
    </style>
    """, unsafe_allow_html=True)

apply_css()

# --- 5. المنطق الوظيفي ---

def validate_email(email):
    # التحقق من صيغة الإيميل باستخدام Regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# --- 6. الواجهات ---

# أ) شاشة تسجيل الدخول والتسجيل
def login_view():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # العنوان الرئيسي
        st.markdown(f"<h1 style='color:#1e3a8a; text-align:center;'>Université Constantine 3</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:gray;'>Portal Étudiant / بوابة الطالب</p>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            
            # اختيار اللغة
            lang_choice = st.radio("", ["العربية", "Français", "English"], horizontal=True)
            if lang_choice == "العربية": st.session_state['lang'] = 'ar'
            elif lang_choice == "Français": st.session_state['lang'] = 'fr'
            else: st.session_state['lang'] = 'en'
            
            tab_login, tab_signup = st.tabs([t('login'), t('signup')])
            
            # --- تبويب الدخول ---
            with tab_login:
                email = st.text_input(t('email'), key="l_email")
                password = st.text_input(t('pass'), type="password", key="l_pass")
                
                if st.button(t('login_btn')):
                    if email in st.session_state['users'] and st.session_state['users'][email]['password'] == password:
                        # إرسال كود التحقق (محاكاة)
                        code = str(random.randint(1000, 9999))
                        st.session_state['verification_code'] = code
                        st.session_state['temp_email'] = email
                        st.session_state['auth_state'] = 'verify'
                        st.rerun()
                    else:
                        st.error("خطأ في البيانات (إذا كنت طالباً جديداً، يرجى التسجيل أولاً)")
            
            # --- تبويب التسجيل ---
            with tab_signup:
                s_email = st.text_input(t('email'), key="s_email")
                s_pass = st.text_input(t('pass'), type="password", key="s_pass")
                s_name = st.text_input(t('name'))
                
                # بيانات الجامعة (قسنطينة 3)
                s_fac = st.selectbox(t('faculty'), list(const_3_data.keys()))
                s_spec = st.selectbox(t('specialty'), const_3_data[s_fac])
                s_level = st.selectbox(t('level'), levels)
                
                s_interests = st.multiselect(t('interests'), ["AI", "Literature", "Architecture", "Politics", "Arts"])
                
                if st.button(t('signup_btn')):
                    if not validate_email(s_email):
                        st.error("صيغة البريد خاطئة")
                    elif s_email in st.session_state['users']:
                        st.error("الحساب موجود مسبقاً")
                    else:
                        # إنشاء الحساب
                        st.session_state['users'][s_email] = {
                            "name": s_name,
                            "password": s_pass,
                            "faculty": s_fac,
                            "specialty": s_spec,
                            "level": s_level,
                            "interests": s_interests,
                            "points": 100, # نقاط البداية المجانية
                            "my_books": [],
                            "avatar": "👨‍🎓",
                            "fb_linked": False
                        }
                        st.success("تم إنشاء الحساب بنجاح! يرجى الانتقال لتبويب 'تسجيل الدخول' للدخول.")
            
            st.markdown('</div>', unsafe_allow_html=True)

# ب) شاشة التحقق (Code Verification)
def verify_view():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<h2 style='text-align:center;'>{t('verify_title')} 🔐</h2>", unsafe_allow_html=True)
        st.info(f"{t('verify_msg')} **{st.session_state['temp_email']}**")
        
        # محاكاة وصول الإيميل (نعرض الكود للتجربة)
        st.warning(f"🔔 SYSTEM MSG: Your Verification Code is **{st.session_state['verification_code']}**")
        
        code = st.text_input(t('code_label'), max_chars=4)
        
        if st.button(t('verify_btn')):
            if code == st.session_state['verification_code']:
                st.session_state['current_user'] = st.session_state['users'][st.session_state['temp_email']]
                st.session_state['auth_state'] = 'dashboard'
                st.success("Access Granted!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("رمز خاطئ / Wrong Code")

# ج) لوحة التحكم (المنصة الكاملة)
def dashboard_view():
    user = st.session_state['current_user']
    email = st.session_state['temp_email'] # مفتاح المستخدم
    
    # --- القائمة الجانبية ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135768.png", width=100)
        st.markdown(f"### {user['name']}")
        st.markdown(f"**{user['faculty']}**")
        st.caption(f"{user['specialty']}")
        
        # عرض النقاط
        st.markdown(f"""
        <div style="background:#dbeafe; padding:10px; border-radius:10px; text-align:center; margin:10px 0;">
            <h2 style="color:#1e40af; margin:0;">{user['points']}</h2>
            <span style="color:#1e40af;">{t('points')} XP</span>
        </div>
        """, unsafe_allow_html=True)
        
        menu = st.radio("", [t('market'), t('upload'), t('quiz'), t('settings')])
        
        st.divider()
        if st.button(t('logout')):
            st.session_state['auth_state'] = 'login'
            st.session_state['current_user'] = None
            st.rerun()

    # --- المحتوى الرئيسي ---
    
    # 1. المكتبة (السوق)
    if menu == t('market'):
        st.title(f"📚 {t('market')}")
        st.markdown("---")
        
        cols = st.columns(2)
        for i, book in enumerate(st.session_state['books']):
            # السعر الديناميكي: كل تحميل يزيد السعر 1 نقطة
            dynamic_price = book['price'] + book['downloads']
            
            with cols[i % 2]:
                st.markdown(f"""
                <div class="book-card">
                    <h3 style="color:#1e3a8a; margin:0;">{book['title']}</h3>
                    <p style="color:gray; font-size:0.9rem;">{t('downloads')}: {book['downloads']}</p>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px;">
                        <span class="badge">{book['type']}</span>
                        <span style="font-weight:bold; color:#d97706;">{dynamic_price} {t('points')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # التحقق من الملكية
                is_owned = any(b['id'] == book['id'] for b in user['my_books'])
                
                if is_owned:
                    st.button("✅ تملكه / Owned", key=f"owned_{i}", disabled=True)
                else:
                    if st.button(f"{t('buy')} (-{dynamic_price})", key=f"buy_{i}"):
                        if user['points'] >= dynamic_price:
                            # خصم النقاط
                            user['points'] -= dynamic_price
                            user['my_books'].append(book)
                            book['downloads'] += 1
                            
                            # مكافأة المؤلف
                            if book['author'] in st.session_state['users']:
                                st.session_state['users'][book['author']]['points'] += dynamic_price
                                
                            st.success("تم الشراء!")
                            st.rerun()
                        else:
                            st.error("رصيدك غير كافٍ!")

    # 2. النشر (AI Evaluation)
    elif menu == t('upload'):
        st.title(f"📤 {t('upload_title')}")
        st.info(t('upload_desc'))
        
        uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
        book_title = st.text_input("عنوان الكتاب")
        
        if uploaded_file and st.button("🚀 بدء التحليل والنشر"):
            with st.spinner("جاري التحليل الأكاديمي بواسطة الذكاء الاصطناعي..."):
                time.sleep(2.5) # محاكاة الوقت
                
                # تقييم عشوائي للجودة (محاكاة AI)
                quality_score = random.randint(40, 100)
                
                if quality_score >= 50:
                    suggested_price = random.randint(40, 60)
                    st.balloons()
                    st.success(f"✅ تمت الموافقة! جودة المحتوى: {quality_score}%")
                    st.markdown(f"### السعر المقترح: {suggested_price} نقطة")
                    
                    new_book = {
                        "id": len(st.session_state['books']) + 1,
                        "title": book_title if book_title else "New Book",
                        "author": email, # صاحب الكتاب
                        "price": suggested_price,
                        "downloads": 0,
                        "type": "Upload"
                    }
                    st.session_state['books'].append(new_book)
                    user['points'] += 10 # مكافأة فورية
                    st.info("تمت إضافة الكتاب للسوق +10 نقاط مكافأة!")
                else:
                    st.error(f"❌ تم رفض المحتوى. الجودة ضعيفة ({quality_score}%)")

    # 3. لعبة الكويز
    elif menu == t('quiz'):
        st.title(f"🧠 {t('quiz_title')}")
        
        if not user['my_books']:
            st.warning("يجب أن تشتري كتباً أولاً لتلعب!")
        else:
            book_choice = st.selectbox("اختر كتاباً للمراجعة", [b['title'] for b in user['my_books']])
            
            if st.button(t('quiz_btn')):
                with st.status("AI يقرأ الكتاب ويولد الأسئلة..."):
                    time.sleep(1.5)
                    st.write("استخراج المفاهيم الأساسية...")
                    time.sleep(1)
                
                st.markdown(f"### سؤال حول: {book_choice}")
                st.write("س: ما هي الفكرة المحورية التي يعالجها الفصل الثالث من هذا الكتاب؟")
                
                ans = st.radio("الإجابة:", ["التحليل البنيوي للنص", "تطور العمارة الحديثة", "تأثير السياسة على الاقتصاد"])
                
                if st.button("تحقق من الإجابة"):
                    if random.random() > 0.5: # حظ 50%
                        reward = 20
                        user['points'] += reward
                        st.balloons()
                        st.success(f"إجابة صحيحة! +{reward} نقطة")
                    else:
                        penalty = 10
                        user['points'] -= penalty
                        st.error(f"إجابة خاطئة! -{penalty} نقطة. ركز جيداً.")

    # 4. الإعدادات
    elif menu == t('settings'):
        st.title(f"⚙️ {t('settings')}")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("### الملف الشخصي")
            new_av = st.selectbox("الصورة الرمزية", ["👨‍🎓", "👩‍🎓", "👨‍🏫", "👩‍🔬", "🎨", "💻"])
            if st.button("تحديث الصورة"):
                user['avatar'] = new_av
                st.success("تم التحديث!")
                st.rerun()
        
        with col_b:
            st.markdown("### الأمان والربط")
            if user['fb_linked']:
                st.success("✅ حسابك مرتبط بـ Facebook")
                if st.button("إلغاء الربط"):
                    user['fb_linked'] = False
                    st.rerun()
            else:
                if st.button(f"📘 {t('fb_link')}"):
                    with st.spinner("جاري الاتصال بـ Facebook API..."):
                        time.sleep(2)
                        user['fb_linked'] = True
                        st.success("تم الربط بنجاح!")
                        st.rerun()
                        
        st.markdown("---")
        st.markdown("### تغيير اللغة / Change Language")
        l_options = ["العربية", "Français", "English"]
        l_sel = st.radio("", l_options, horizontal=True)
        if st.button("تأكيد اللغة"):
            if l_sel == "العربية": st.session_state['lang'] = 'ar'
            elif l_sel == "Français": st.session_state['lang'] = 'fr'
            else: st.session_state['lang'] = 'en'
            st.rerun()

# --- 7. الموجه الرئيسي (Router) ---
if st.session_state['auth_state'] == 'login':
    login_view()
elif st.session_state['auth_state'] == 'verify':
    verify_view()
else:
    dashboard_view()
