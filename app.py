import streamlit as st
import time
import random
import google.generativeai as genai
import os

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="منصة نزاهة | جامعة قسنطينة 3",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- إعداد Gemini AI (اختياري) ---
# للحصول على ذكاء اصطناعي حقيقي، يفضل وضع المفتاح في st.secrets
# إذا لم يوجد مفتاح، سيعمل النظام بمحاكي ذكي متطور
api_key = os.environ.get("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

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
        "ai_chat": "مدرب النزاهة (AI)",
        "profile": "الملف الشخصي",
        "points": "نقاط المعرفة",
        "buy": "شراء",
        "owned": "مملوك",
        "welcome": "مرحباً،",
        "logout": "خروج",
        "price": "السعر",
        "download": "تحميل الملف",
        "search": "بحث في المكتبة...",
        "no_books": "لم تقم بشراء أي كتب بعد.",
        "go_library": "اذهب للمكتبة",
        "correct": "إجابة صحيحة! +10 نقاط",
        "wrong": "إجابة خاطئة، حاول مرة أخرى",
        "gen_quiz": "توليد اختبار جديد",
        "full_name": "الاسم الكامل",
        "faculty": "الكلية",
        "specialty": "التخصص",
        "year_study": "السنة الدراسية",
        "success_buy": "تم الشراء! يمكنك التحميل الآن.",
        "error_points": "رصيدك غير كافٍ!",
        "recent_books": "مكتبتي",
        "my_uploads": "ملفاتي",
        "level": "المستوى",
        "summarize": "تلخيص الكتاب (AI)",
        "summary_result": "ملخص الذكاء الاصطناعي:",
        "comments": "التعليقات",
        "add_comment": "أضف تعليقك...",
        "post_comment": "نشر التعليق",
        "chat_intro": "مرحباً بك في مساعد النزاهة. أنا هنا لمساعدتك في صياغة الأوامر (Prompts) وتوجيه بحثك العلمي.",
        "user_prompt": "أدخل الأمر (Prompt) أو سؤالك هنا...",
        "change_pass": "تغيير كلمة المرور",
        "old_pass": "كلمة المرور الحالية",
        "new_pass": "كلمة المرور الجديدة",
        "confirm_pass": "تأكيد كلمة المرور",
        "save_changes": "حفظ التغييرات",
        "link_accounts": "ربط الحسابات",
        "clear_chat": "مسح سجل الدردشة",
        "bio": "نبذة عني",
        "edit_profile": "تعديل الملف"
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
        "ai_chat": "Coach Nazaha (AI)",
        "profile": "Profil",
        "points": "Points de Savoir",
        "buy": "Acheter",
        "owned": "Acquis",
        "welcome": "Bienvenue, ",
        "logout": "Déconnexion",
        "price": "Prix",
        "download": "Télécharger",
        "search": "Rechercher...",
        "no_books": "Vous n'avez pas encore acheté de livres.",
        "go_library": "Aller à la bibliothèque",
        "correct": "Correct! +10 XP",
        "wrong": "Faux, essayez encore",
        "gen_quiz": "Générer un Quiz",
        "full_name": "Nom Complet",
        "faculty": "Faculté",
        "specialty": "Spécialité",
        "year_study": "Année d'étude",
        "success_buy": "Acheté! Téléchargement disponible.",
        "error_points": "Points insuffisants !",
        "recent_books": "Ma Bibliothèque",
        "my_uploads": "Mes Uploads",
        "level": "Niveau",
        "summarize": "Résumer (IA)",
        "summary_result": "Résumé IA:",
        "comments": "Commentaires",
        "add_comment": "Ajouter un commentaire...",
        "post_comment": "Publier",
        "chat_intro": "Bienvenue sur Nazaha Coach. Je suis là pour guider votre recherche.",
        "user_prompt": "Entrez votre prompt...",
        "change_pass": "Changer le mot de passe",
        "old_pass": "Ancien mot de passe",
        "new_pass": "Nouveau mot de passe",
        "confirm_pass": "Confirmer",
        "save_changes": "Sauvegarder",
        "link_accounts": "Lier les comptes",
        "clear_chat": "Effacer le chat",
        "bio": "Biographie",
        "edit_profile": "Modifier le profil"
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
        "ai_chat": "Nazaha Coach (AI)",
        "profile": "Profile",
        "points": "Knowledge Points",
        "buy": "Buy",
        "owned": "Owned",
        "welcome": "Welcome, ",
        "logout": "Logout",
        "price": "Price",
        "download": "Download",
        "search": "Search...",
        "no_books": "You haven't bought any books yet.",
        "go_library": "Go to Library",
        "correct": "Correct! +10 XP",
        "wrong": "Wrong answer",
        "gen_quiz": "Generate Quiz",
        "full_name": "Full Name",
        "faculty": "Faculty",
        "specialty": "Specialty",
        "year_study": "Year of Study",
        "success_buy": "Purchased! Download available.",
        "error_points": "Insufficient points!",
        "recent_books": "My Library",
        "my_uploads": "My Uploads",
        "level": "Level",
        "summarize": "Summarize (AI)",
        "summary_result": "AI Summary:",
        "comments": "Comments",
        "add_comment": "Add a comment...",
        "post_comment": "Post",
        "chat_intro": "Welcome to Nazaha Coach. I'm here to guide your research.",
        "user_prompt": "Enter your prompt...",
        "change_pass": "Change Password",
        "old_pass": "Old Password",
        "new_pass": "New Password",
        "confirm_pass": "Confirm Password",
        "save_changes": "Save Changes",
        "link_accounts": "Link Accounts",
        "clear_chat": "Clear Chat History",
        "bio": "Bio",
        "edit_profile": "Edit Profile"
    }
}

# --- البيانات الهيكلية (جامعة قسنطينة 3) ---
FACULTY_SPECIALTIES = {
    "Faculté de Médecine": ["Médecine", "Pharmacie", "Médecine Dentaire"],
    "Faculté d'Architecture et d'Urbanisme": ["Architecture", "Urbanisme", "Gestion des Villes"],
    "Faculté des Arts et de la Culture": ["Arts Plastiques", "Arts Dramatiques", "Cinéma", "Design"],
    "Faculté de Génie des Procédés": ["Génie Chimique", "Génie Pharmaceutique", "Génie de l'Environnement"],
    "Faculté des Sciences Politiques": ["Sciences Politiques", "Relations Internationales", "Organisation Administrative"],
    "Faculté des NTIC": ["Informatique (GL)", "Informatique (SI)", "Réseaux et Télécom (RSD)", "Technologies Web (STIC)"],
    "Institut de Gestion des Techniques Urbaines": ["Génie Urbain", "Gestion de la ville"]
}

STUDY_YEARS = ["Licence 1", "Licence 2", "Licence 3", "Master 1", "Master 2", "Doctorat"]

# --- البيانات الأولية ---
INITIAL_BOOKS = [
    {"id": 1, "title": "Introduction à l'Architecture", "author": "Dr. Amine", "faculty": "Architecture", "price": 45, "downloads": 120, "category": "Architecture", "comments": [{"user": "Ali", "text": "كتاب ممتاز للمبتدئين"}]},
    {"id": 2, "title": "Algorithmique Avancée", "author": "Prof. Sara", "faculty": "NTIC", "price": 60, "downloads": 45, "category": "Informatique", "comments": []},
    {"id": 3, "title": "Anatomie Humaine", "author": "Faculté Méd", "faculty": "Médecine", "price": 75, "downloads": 300, "category": "Médecine", "comments": [{"user": "Sami", "text": "الصور واضحة جداً"}]}
]

# --- إدارة الحالة (Session State) ---
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'view' not in st.session_state: st.session_state.view = 'login'
if 'user' not in st.session_state: st.session_state.user = None
if 'books' not in st.session_state: st.session_state.books = INITIAL_BOOKS
if 'quiz_data' not in st.session_state: st.session_state.quiz_data = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- دوال مساعدة ---
def t(key): return TRANSLATIONS[st.session_state.lang].get(key, key)
def set_lang(l): st.session_state.lang = l
def set_view(v): st.session_state.view = v

def get_mock_file_data(book_title):
    return f"هذا محتوى تجريبي للكتاب: {book_title}\n\nحقوق النشر محفوظة لجامعة قسنطينة 3.\nمنصة نزاهة.".encode('utf-8')

# ذكاء اصطناعي محاكي (في حال عدم وجود مفتاح API)
def mock_ai_response(prompt):
    prompt = prompt.lower()
    if "بحث" in prompt or "research" in prompt:
        return "للبدء في بحث أكاديمي جيد، ابدأ بصياغة سؤال البحث الرئيسي. هل يمكنك تحديد الموضوع بدقة؟ سأساعدك في كتابة المقدمة."
    elif "برومبت" in prompt or "prompt" in prompt:
        return "كتابة البرومبت (Prompt Engineering) تتطلب تحديد: الدور (أنت باحث)، المهمة (لخص)، والسياق. حاول إعادة صياغة طلبك بهذه الطريقة."
    elif "سرقة" in prompt or "plagiaris" in prompt:
        return "تجنب السرقة العلمية يكون عبر التوثيق الجيد (APA/IEEE) وإعادة الصياغة بأسلوبك الخاص. هل تريدني أن أراجع فقرة لك؟"
    elif "python" in prompt or "code" in prompt:
        return "يمكنني مساعدتك في البرمجة. تأكد من فهم الكود قبل نسخه. ما هي المشكلة التي تواجهها في الكود؟"
    else:
        return "هذا موضوع مثير! بصفتي مساعدك الأكاديمي في جامعة قسنطينة 3، أنصحك بالتركيز على المراجع الحديثة. هل لديك أي أسئلة محددة؟"

# استدعاء الذكاء الاصطناعي (الحقيقي أو المحاكي)
def generate_ai_response(prompt):
    if api_key:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"حدث خطأ في الاتصال بـ Gemini: {e}. سأستخدم النظام الاحتياطي.\n\n{mock_ai_response(prompt)}"
    else:
        # تأخير بسيط لمحاكاة التفكير
        time.sleep(1.5)
        return mock_ai_response(prompt)

# --- CSS مخصص ---
direction = TRANSLATIONS[st.session_state.lang]['dir']
st.markdown(f"""
<style>
    .main {{ direction: {direction}; text-align: {'right' if direction == 'rtl' else 'left'}; }}
    .stButton button {{ width: 100%; }}
    .block-container {{ direction: {direction}; }}
    div[data-testid="stMetricValue"] {{ direction: ltr; }}
    .stChatMessage {{ direction: {direction}; }}
    /* تحسين مظهر الملف الشخصي */
    .profile-card {{
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
    }}
</style>
""", unsafe_allow_html=True)

# --- الواجهات ---

def auth_view():
    st.markdown(f"<h1 style='text-align: center; color: #1e3a8a;'>{t('title')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: gray;'>{t('tagline')}</p>", unsafe_allow_html=True)
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c2:
        if st.button("AR"): set_lang("ar"); st.rerun()
    with c3:
        if st.button("FR"): set_lang("fr"); st.rerun()
    with c4:
        if st.button("EN"): set_lang("en"); st.rerun()

    tab1, tab2 = st.tabs([t('login'), t('signup')])

    with tab1:
        with st.form("login_form"):
            email = st.text_input(t('email'))
            password = st.text_input(t('password'), type="password")
            submit = st.form_submit_button(t('login'))
            
            if submit:
                if email and password:
                    # محاكاة الدخول
                    st.session_state.user = {
                        "name": "طالب تجريبي", 
                        "email": email, 
                        "points": 200, 
                        "library": [], 
                        "uploads": [],
                        "faculty": "NTIC",
                        "specialty": "GL",
                        "level": "Master 1",
                        "bio": "طالب باحث مهتم بالذكاء الاصطناعي."
                    }
                    st.session_state.view = 'ai_chat' # التوجيه المباشر للدردشة
                    st.rerun()
                else:
                    st.error("الرجاء إدخال البيانات")

    with tab2:
        st.markdown("### " + t('signup'))
        # إزالة st.form هنا لحل مشكلة تحديث التخصصات
        # يتم استخدام حاوية عادية للتفاعل الفوري
        
        name = st.text_input(t('full_name'))
        email_reg = st.text_input(t('email'))
        pass_reg = st.text_input(t('password'), type="password")
        
        # اختيار الكلية (ديناميكي)
        faculty_list = list(FACULTY_SPECIALTIES.keys())
        faculty = st.selectbox(t('faculty'), faculty_list, index=0)
        
        # تحديث التخصصات بناءً على الكلية المختارة فوراً
        specialties_list = FACULTY_SPECIALTIES.get(faculty, [])
        specialty = st.selectbox(t('specialty'), specialties_list)
        
        level = st.selectbox(t('year_study'), STUDY_YEARS)
        
        if st.button(t('signup'), type="primary"):
            if name and email_reg and pass_reg:
                st.session_state.user = {
                    "name": name, 
                    "email": email_reg, 
                    "points": 150, 
                    "library": [], 
                    "uploads": [],
                    "faculty": faculty,
                    "specialty": specialty,
                    "level": level,
                    "bio": "طالب جديد في المنصة."
                }
                st.session_state.view = 'ai_chat' # التوجيه المباشر للدردشة
                st.success("تم إنشاء الحساب بنجاح!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("الرجاء ملء جميع الحقول")

def sidebar_menu():
    user = st.session_state.user
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2995/2995620.png", width=50)
        st.title("Nazaha LMS")
        
        if user:
            st.info(f"{t('welcome')} {user['name']}\n\n🏆 {user['points']} XP")
        
        st.markdown("---")
        
        # ترتيب الأزرار حسب الأهمية
        if st.button(f"🤖 {t('ai_chat')}"): set_view('ai_chat')
        if st.button(f"👤 {t('profile')}"): set_view('profile') # زر جديد
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

def profile_view():
    user = st.session_state.user
    st.title(f"👤 {t('profile')}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)
        st.metric(label="XP", value=user['points'])
        
    with col2:
        st.markdown(f"""
        <div class="profile-card">
            <h3>{user['name']}</h3>
            <p><strong>{t('email')}:</strong> {user['email']}</p>
            <p><strong>{t('faculty')}:</strong> {user['faculty']}</p>
            <p><strong>{t('specialty')}:</strong> {user['specialty']}</p>
            <p><strong>{t('level')}:</strong> {user['level']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### " + t('bio'))
        new_bio = st.text_area("", value=user.get('bio', ''), height=100)
        if st.button(t('save_changes'), key="save_bio"):
            user['bio'] = new_bio
            st.success("تم تحديث النبذة التعريفية")

def ai_chat_view():
    st.title(f"🤖 {t('ai_chat')}")
    
    # عرض التنبيه فقط إذا كانت الدردشة فارغة
    if not st.session_state.chat_history:
        st.info(t('chat_intro'))
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(t('user_prompt')):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # استدعاء دالة الذكاء الاصطناعي (الحقيقي أو المحاكي)
            ai_reply = generate_ai_response(prompt)
            
            # محاكاة الكتابة (Streaming effect)
            for chunk in ai_reply.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

def library_view():
    st.title(t('library'))
    user = st.session_state.user
    search = st.text_input(t('search'))
    
    filtered_books = [b for b in st.session_state.books if search.lower() in b['title'].lower()]
    
    cols = st.columns(2)
    for i, book in enumerate(filtered_books):
        with cols[i % 2]:
            with st.container(border=True):
                st.subheader(book['title'])
                st.caption(f"{book['author']} | {book['faculty']}")
                
                is_owned = any(b['id'] == book['id'] for b in user['library'])
                
                # زر التلخيص
                if st.button(f"✨ {t('summarize')}", key=f"sum_{book['id']}"):
                    with st.spinner(t('analyzing')):
                        time.sleep(1.5)
                        st.info(f"**{t('summary_result')}**\n\nملخص حول {book['title']}...")

                if is_owned:
                    st.success(f"✅ {t('owned')}")
                    # زر التحميل يظهر دائماً للمحتوى المملوك
                    file_data = get_mock_file_data(book['title'])
                    st.download_button(
                        label=f"⬇️ {t('download')}",
                        data=file_data,
                        file_name=f"{book['title']}.txt",
                        mime="text/plain",
                        key=f"lib_dl_{book['id']}",
                        use_container_width=True
                    )
                else:
                    price = int(book['price'] + (book['downloads'] * 0.2))
                    st.markdown(f"**{price} XP**")
                    
                    # زر الشراء
                    if st.button(t('buy'), key=f"buy_{book['id']}"):
                        if user['points'] >= price:
                            user['points'] -= price
                            user['library'].append(book)
                            book['downloads'] += 1
                            st.balloons() # احتفال بالشراء
                            st.toast(t('success_buy'), icon="✅")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(t('error_points'))

def dashboard_view():
    # (نفس الكود السابق مع تحسينات طفيفة)
    user = st.session_state.user
    st.title(t('dashboard'))
    col1, col2, col3 = st.columns(3)
    col1.metric(t('recent_books'), len(user['library']))
    col2.metric(t('my_uploads'), len(user['uploads']))
    col3.metric(t('level'), user['level'])
    st.subheader(t('recent_books'))
    if not user['library']:
        st.warning(t('no_books'))
        if st.button(t('go_library')): set_view('library'); st.rerun()
    else:
        for book in user['library']:
            with st.expander(f"📄 {book['title']}"):
                st.write(f"👤 {book['author']}")
                file_data = get_mock_file_data(book['title'])
                st.download_button(
                    label=f"⬇️ {t('download')}",
                    data=file_data,
                    file_name=f"{book['title']}.txt",
                    mime="text/plain",
                    key=f"dash_dl_{book['id']}"
                )

def settings_view():
    st.title(t('settings'))
    
    # قسم اللغة
    st.subheader("🌐 Language / اللغة")
    c1, c2, c3 = st.columns([1,1,1])
    if c1.button("العربية", key="lang_ar"): set_lang('ar'); st.rerun()
    if c2.button("Français", key="lang_fr"): set_lang('fr'); st.rerun()
    if c3.button("English", key="lang_en"): set_lang('en'); st.rerun()
    
    st.divider()
    
    # قسم الأمان (محاكاة)
    st.subheader(f"🔒 {t('change_pass')}")
    with st.expander(t('change_pass')):
        current = st.text_input(t('old_pass'), type="password")
        new_p = st.text_input(t('new_pass'), type="password")
        confirm_p = st.text_input(t('confirm_pass'), type="password")
        if st.button(t('save_changes')):
            if new_p == confirm_p and len(new_p) > 0:
                st.success("تم تحديث كلمة المرور بنجاح!")
            else:
                st.error("كلمات المرور غير متطابقة")
    
    st.divider()
    
    # ربط الحسابات (محاكاة)
    st.subheader(f"🔗 {t('link_accounts')}")
    c_fb, c_google = st.columns(2)
    with c_fb:
        st.toggle("Facebook", value=False)
    with c_google:
        st.toggle("Google", value=True)
        
    st.divider()
    
    # إدارة البيانات
    st.subheader("🗑️ Zone Danger")
    if st.button(t('clear_chat'), type="primary"):
        st.session_state.chat_history = []
        st.success("تم مسح السجل")
        time.sleep(0.5)
        st.rerun()

# الدوال الأخرى (upload_view, quiz_view) تبقى كما هي مع التأكد من استدعائها بشكل صحيح
def upload_view():
    # ... (نفس كود الرفع السابق)
    st.title(t('upload'))
    st.info(t('upload_text'))
    title = st.text_input("عنوان الملف")
    uploaded_file = st.file_uploader("PDF", type="pdf")
    if uploaded_file and title:
        if st.button("تحليل"):
            with st.spinner(t('analyzing')):
                time.sleep(1.5)
                score = random.randint(50, 99)
                price = int(score * 0.8)
                st.session_state.upload_result = {"score": score, "price": price, "title": title}
    if 'upload_result' in st.session_state:
        res = st.session_state.upload_result
        st.success(f"الجودة: {res['score']}%")
        st.metric(t('price'), f"{res['price']} XP")
        if st.button(t('publish')): # إضافة الكتاب للمكتبة والمستخدم
             # ... (Logic to add book)
             new_book = {"id": int(time.time()), "title": res['title'], "author": st.session_state.user['name'], "faculty": st.session_state.user['faculty'], "price": res['price'], "downloads": 0, "category": "General"}
             st.session_state.books.append(new_book)
             st.session_state.user['uploads'].append(new_book)
             st.session_state.user['points'] += 20
             del st.session_state.upload_result
             st.balloons()
             st.rerun()

def quiz_view():
    st.title(t('quiz'))
    user = st.session_state.user
    if not user['library']: st.warning(t('no_books')); return
    
    if st.button(t('gen_quiz')) or st.session_state.quiz_data is None:
        book = random.choice(user['library'])
        st.session_state.quiz_data = {"question": f"سؤال حول {book['title']}؟", "options": ["أ", "ب", "ج"], "correct": "أ"}
    
    q = st.session_state.quiz_data
    st.subheader(q['question'])
    ans = st.radio("الجواب", q['options'], key=f"q_{q['question']}")
    if st.button("تحقق"):
        if ans == q['correct']: st.success(t('correct')); user['points']+=10
        else: st.error(t('wrong'))

# --- المحرك الرئيسي ---
if st.session_state.user is None:
    auth_view()
else:
    sidebar_menu()
    if st.session_state.view == 'dashboard': dashboard_view()
    elif st.session_state.view == 'library': library_view()
    elif st.session_state.view == 'upload': upload_view()
    elif st.session_state.view == 'quiz': quiz_view()
    elif st.session_state.view == 'ai_chat': ai_chat_view()
    elif st.session_state.view == 'settings': settings_view()
    elif st.session_state.view == 'profile': profile_view()
