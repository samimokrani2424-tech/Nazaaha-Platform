import streamlit as st
import time
import random

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="منصة نزاهة | جامعة قسنطينة 3",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- قاموس الترجمة ---
TRANSLATIONS = {
    "ar": {
        "dir": "rtl",
        "title": "منصة نزاهة الأكاديمية",
        "tagline": "بوابتك نحو التميز الأكاديمي - جامعة قسنطينة 3",
        "login": "تسجيل الدخول",
        "signup": "إنشاء حساب",
        "email": "البريد الإلكتروني",
        "password": "كلمة المرور",
        "dashboard": "لوحة القيادة",
        "library": "المكتبة الرقمية",
        "upload": "مركز النشر",
        "quiz": "تحدي المعرفة",
        "settings": "الإعدادات",
        "points": "نقاط المعرفة",
        "buy": "شراء",
        "owned": "مملوك",
        "welcome": "مرحباً،",
        "logout": "خروج",
        "price": "السعر",
        "quality": "الجودة العلمية",
        "upload_text": "ارفع ملفاتك وسيقوم الذكاء الاصطناعي بتقييمها",
        "download": "تحميل وقراءة",
        "search": "بحث في المكتبة...",
        "no_books": "لم تقم بشراء أي كتب بعد.",
        "go_library": "اذهب للمكتبة",
        "correct": "إجابة صحيحة! +10 نقاط",
        "wrong": "إجابة خاطئة، حاول مرة أخرى",
        "gen_quiz": "توليد اختبار",
        "quiz_ready": "هل أنت مستعد لاختبار معرفتك؟",
        "analyzing": "جاري التحليل بالذكاء الاصطناعي...",
        "publish": "نشر في المكتبة (+20 نقطة)",
        "cancel": "إلغاء",
        "low_quality": "محتوى ضعيف الجودة",
        "high_quality": "محتوى أكاديمي مقبول",
        "full_name": "الاسم الكامل",
        "faculty": "الكلية",
        "choose_faculty": "اختر الكلية...",
        "success_buy": "تم شراء الكتاب بنجاح!",
        "error_points": "رصيدك غير كافٍ!",
        "recent_books": "أحدث الكتب",
        "my_uploads": "ملفاتي",
        "level": "المستوى"
    },
    "fr": {
        "dir": "ltr",
        "title": "Plateforme Académique Nazaha",
        "tagline": "Votre portail vers l'excellence - Université Constantine 3",
        "login": "Connexion",
        "signup": "Inscription",
        "email": "Email",
        "password": "Mot de passe",
        "dashboard": "Tableau de bord",
        "library": "Bibliothèque",
        "upload": "Centre de Publication",
        "quiz": "Quiz de Connaissance",
        "settings": "Paramètres",
        "points": "Points de Savoir",
        "buy": "Acheter",
        "owned": "Acquis",
        "welcome": "Bienvenue, ",
        "logout": "Déconnexion",
        "price": "Prix",
        "quality": "Qualité",
        "upload_text": "Téléchargez vos fichiers, l'IA les évaluera",
        "download": "Télécharger",
        "search": "Rechercher...",
        "no_books": "Vous n'avez pas encore acheté de livres.",
        "go_library": "Aller à la bibliothèque",
        "correct": "Correct! +10 XP",
        "wrong": "Faux, essayez encore",
        "gen_quiz": "Générer un Quiz",
        "quiz_ready": "Prêt à tester vos connaissances ?",
        "analyzing": "Analyse par IA en cours...",
        "publish": "Publier (+20 XP)",
        "cancel": "Annuler",
        "low_quality": "Contenu de faible qualité",
        "high_quality": "Contenu académique approuvé",
        "full_name": "Nom Complet",
        "faculty": "Faculté",
        "choose_faculty": "Choisir Faculté...",
        "success_buy": "Livre acheté avec succès !",
        "error_points": "Points insuffisants !",
        "recent_books": "Livres Récents",
        "my_uploads": "Mes Uploads",
        "level": "Niveau"
    },
    "en": {
        "dir": "ltr",
        "title": "Nazaha Academic Platform",
        "tagline": "Your gateway to excellence - Constantine 3 University",
        "login": "Login",
        "signup": "Sign Up",
        "email": "Email",
        "password": "Password",
        "dashboard": "Dashboard",
        "library": "Library",
        "upload": "Upload Center",
        "quiz": "Knowledge Quiz",
        "settings": "Settings",
        "points": "Knowledge Points",
        "buy": "Buy",
        "owned": "Owned",
        "welcome": "Welcome, ",
        "logout": "Logout",
        "price": "Price",
        "quality": "Quality",
        "upload_text": "Upload files, AI will evaluate them",
        "download": "Download",
        "search": "Search...",
        "no_books": "You haven't bought any books yet.",
        "go_library": "Go to Library",
        "correct": "Correct! +10 XP",
        "wrong": "Wrong answer",
        "gen_quiz": "Generate Quiz",
        "quiz_ready": "Ready to test your knowledge?",
        "analyzing": "AI Analyzing...",
        "publish": "Publish (+20 XP)",
        "cancel": "Cancel",
        "low_quality": "Low Quality Content",
        "high_quality": "Academic Content Approved",
        "full_name": "Full Name",
        "faculty": "Faculty",
        "choose_faculty": "Choose Faculty...",
        "success_buy": "Book purchased successfully!",
        "error_points": "Insufficient points!",
        "recent_books": "Recent Books",
        "my_uploads": "My Uploads",
        "level": "Level"
    }
}

# --- البيانات الأولية ---
INITIAL_BOOKS = [
    {"id": 1, "title": "Introduction à l'Architecture", "author": "Dr. Amine", "faculty": "Architecture", "price": 45, "downloads": 120, "category": "Architecture"},
    {"id": 2, "title": "Algorithmique Avancée", "author": "Prof. Sara", "faculty": "NTIC", "price": 60, "downloads": 45, "category": "Informatique"},
    {"id": 3, "title": "Anatomie Humaine", "author": "Faculté Méd", "faculty": "Médecine", "price": 75, "downloads": 300, "category": "Médecine"}
]

FACULTIES = [
    "Faculté de Médecine", "Faculté d'Architecture", "Faculté des Arts", 
    "Génie des Procédés", "Sciences Politiques", "Faculté des NTIC"
]

# --- إدارة الحالة (Session State) ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'
if 'view' not in st.session_state:
    st.session_state.view = 'login'
if 'user' not in st.session_state:
    st.session_state.user = None
if 'books' not in st.session_state:
    st.session_state.books = INITIAL_BOOKS
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None

# --- دوال مساعدة ---
def t(key):
    return TRANSLATIONS[st.session_state.lang].get(key, key)

def set_lang(l):
    st.session_state.lang = l

def set_view(v):
    st.session_state.view = v

# --- تصميم مخصص لتوجيه النص (RTL/LTR) ---
direction = TRANSLATIONS[st.session_state.lang]['dir']
st.markdown(f"""
<style>
    .main {{ direction: {direction}; text-align: {'right' if direction == 'rtl' else 'left'}; }}
    .stButton button {{ width: 100%; }}
    .block-container {{ direction: {direction}; }}
    div[data-testid="stMetricValue"] {{ direction: ltr; }}
</style>
""", unsafe_allow_html=True)


# --- الواجهات ---

def auth_view():
    st.markdown(f"<h1 style='text-align: center; color: #1e3a8a;'>{t('title')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: gray;'>{t('tagline')}</p>", unsafe_allow_html=True)
    
    # أزرار اللغة
    c1, c2, c3, c4, c5 = st.columns(5)
    with c2:
        if st.button("AR"): set_lang("ar")
    with c3:
        if st.button("FR"): set_lang("fr")
    with c4:
        if st.button("EN"): set_lang("en")

    tab1, tab2 = st.tabs([t('login'), t('signup')])

    with tab1:
        with st.form("login_form"):
            email = st.text_input(t('email'))
            password = st.text_input(t('password'), type="password")
            submit = st.form_submit_button(t('login'))
            
            if submit:
                # محاكاة تسجيل دخول بسيط
                if email and password:
                    st.session_state.user = {
                        "name": "Student User", 
                        "email": email, 
                        "points": 150, 
                        "library": [], 
                        "uploads": [],
                        "faculty": "NTIC",
                        "level": "Master 1"
                    }
                    st.session_state.view = 'dashboard'
                    st.rerun()
                else:
                    st.error("Please enter credentials")

    with tab2:
        with st.form("signup_form"):
            name = st.text_input(t('full_name'))
            email_reg = st.text_input(t('email'))
            pass_reg = st.text_input(t('password'), type="password")
            faculty = st.selectbox(t('faculty'), FACULTIES)
            submit_reg = st.form_submit_button(t('signup'))
            
            if submit_reg:
                if name and email_reg:
                    st.session_state.user = {
                        "name": name, 
                        "email": email_reg, 
                        "points": 150, 
                        "library": [], 
                        "uploads": [],
                        "faculty": faculty,
                        "level": "Licence 1"
                    }
                    st.session_state.view = 'dashboard'
                    st.success("Account created!")
                    time.sleep(1)
                    st.rerun()

def sidebar_menu():
    user = st.session_state.user
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2995/2995620.png", width=50)
        st.title("Nazaha LMS")
        
        if user:
            st.info(f"{t('welcome')} {user['name']}\n\n🏆 {user['points']} XP")
        
        st.markdown("---")
        
        if st.button(f"📊 {t('dashboard')}"): set_view('dashboard')
        if st.button(f"📚 {t('library')}"): set_view('library')
        if st.button(f"📤 {t('upload')}"): set_view('upload')
        if st.button(f"🧠 {t('quiz')}"): set_view('quiz')
        if st.button(f"⚙️ {t('settings')}"): set_view('settings')
        
        st.markdown("---")
        if st.button(f"🚪 {t('logout')}", type="primary"):
            st.session_state.user = None
            st.session_state.view = 'login'
            st.rerun()

def dashboard_view():
    user = st.session_state.user
    st.title(t('dashboard'))
    
    col1, col2, col3 = st.columns(3)
    col1.metric(t('library'), len(user['library']))
    col2.metric(t('my_uploads'), len(user['uploads']))
    col3.metric(t('level'), user['level'])
    
    st.subheader(t('recent_books'))
    if not user['library']:
        st.warning(t('no_books'))
        if st.button(t('go_library')):
            set_view('library')
            st.rerun()
    else:
        for book in user['library']:
            with st.expander(f"📄 {book['title']}"):
                st.write(f"👤 {book['author']}")
                st.button(t('download'), key=f"dl_{book['id']}")

def library_view():
    st.title(t('library'))
    user = st.session_state.user
    
    search = st.text_input(t('search'))
    
    # تصفية الكتب
    filtered_books = [b for b in st.session_state.books if search.lower() in b['title'].lower()]
    
    # عرض الكتب في شبكة
    cols = st.columns(3)
    for i, book in enumerate(filtered_books):
        with cols[i % 3]:
            with st.container(border=True):
                st.subheader(book['title'])
                st.caption(f"{book['author']} | {book['faculty']}")
                st.write(f"📥 {book['downloads']} | ⭐ {t(book['category'])}")
                
                is_owned = any(b['id'] == book['id'] for b in user['library'])
                price = int(book['price'] + (book['downloads'] * 0.2))
                
                if is_owned:
                    st.success(f"✅ {t('owned')}")
                else:
                    st.markdown(f"**{price} XP**")
                    if st.button(t('buy'), key=f"buy_{book['id']}"):
                        if user['points'] >= price:
                            user['points'] -= price
                            user['library'].append(book)
                            book['downloads'] += 1
                            st.toast(t('success_buy'))
                            st.rerun()
                        else:
                            st.error(t('error_points'))

def upload_view():
    st.title(t('upload'))
    st.info(t('upload_text'))
    
    title = st.text_input("عنوان الملف / الكتاب")
    uploaded_file = st.file_uploader("اختر ملف PDF", type="pdf")
    
    if uploaded_file and title:
        if st.button("تحليل وتقييم (AI Analysis)"):
            with st.spinner(t('analyzing')):
                time.sleep(2) # محاكاة الانتظار
                
                # محاكاة الذكاء الاصطناعي
                score = random.randint(40, 99)
                is_academic = score > 50
                price = int(score * 0.8)
                
                st.session_state.upload_result = {
                    "score": score,
                    "is_academic": is_academic,
                    "price": price,
                    "title": title
                }
    
    if 'upload_result' in st.session_state:
        res = st.session_state.upload_result
        if res['is_academic']:
            st.success(f"{t('high_quality')} (Score: {res['score']}%)")
            st.metric(t('price'), f"{res['price']} XP")
            
            if st.button(t('publish')):
                new_book = {
                    "id": int(time.time()),
                    "title": res['title'],
                    "author": st.session_state.user['name'],
                    "faculty": st.session_state.user['faculty'],
                    "price": res['price'],
                    "downloads": 0,
                    "category": "General"
                }
                st.session_state.books.append(new_book)
                st.session_state.user['uploads'].append(new_book)
                st.session_state.user['points'] += 20
                del st.session_state.upload_result
                st.balloons()
                st.toast("Published! +20 XP")
                time.sleep(1)
                st.rerun()
        else:
            st.error(t('low_quality'))
            if st.button(t('cancel')):
                del st.session_state.upload_result
                st.rerun()

def quiz_view():
    st.title(t('quiz'))
    user = st.session_state.user
    
    if not user['library']:
        st.warning(t('no_books'))
        return

    if st.session_state.quiz_data is None:
        st.write(t('quiz_ready'))
        if st.button(t('gen_quiz')):
            book = random.choice(user['library'])
            st.session_state.quiz_data = {
                "question": f"في سياق كتاب '{book['title']}'، ما هو المنهج الأساسي الذي تمت مناقشته؟",
                "options": ["التحليل الكمي", "المسح النوعي", "دراسة الحالة", "المنهج المختلط"],
                "correct": "التحليل الكمي"
            }
            st.rerun()
    else:
        q = st.session_state.quiz_data
        st.subheader(q['question'])
        answer = st.radio("اختر الإجابة:", q['options'])
        
        if st.button("تأكيد الإجابة"):
            if answer == q['correct']:
                st.success(t('correct'))
                user['points'] += 10
            else:
                st.error(t('wrong'))
            st.session_state.quiz_data = None
            time.sleep(2)
            st.rerun()

def settings_view():
    st.title(t('settings'))
    st.write("Language / اللغة / Langue")
    c1, c2, c3 = st.columns([1,1,1])
    if c1.button("العربية"): set_lang('ar'); st.rerun()
    if c2.button("Français"): set_lang('fr'); st.rerun()
    if c3.button("English"): set_lang('en'); st.rerun()

# --- المحرك الرئيسي ---
if st.session_state.user is None:
    auth_view()
else:
    sidebar_menu()
    
    if st.session_state.view == 'dashboard':
        dashboard_view()
    elif st.session_state.view == 'library':
        library_view()
    elif st.session_state.view == 'upload':
        upload_view()
    elif st.session_state.view == 'quiz':
        quiz_view()
    elif st.session_state.view == 'settings':
        settings_view()
