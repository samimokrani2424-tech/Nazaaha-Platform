import streamlit as st
import time
import random
from datetime import datetime

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="منصة نزاهة | جامعة قسنطينة 3",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. قاموس اللغات والترجمة ---
translations = {
    "ar": {
        "title": "منصة نزاهة الجامعية",
        "login": "تسجيل الدخول",
        "signup": "حساب جديد",
        "email": "البريد الإلكتروني",
        "password": "كلمة المرور",
        "welcome": "مرحباً بك في",
        "points": "نقاط المعرفة",
        "library": "المكتبة المركزية",
        "upload": "نشر بحث/كتاب",
        "quiz": "اختبر معلوماتك",
        "settings": "الإعدادات",
        "buy": "شراء وتحميل",
        "price": "السعر",
        "downloads": "التحميلات",
        "upload_btn": "رفع الملف للتقييم",
        "ai_check": "جاري التحليل بواسطة AI...",
        "logout": "خروج",
        "level": "المستوى الدراسي",
        "specialty": "التخصص",
        "faculty": "الكلية",
        "fb_login": "متابعة باستخدام Facebook"
    },
    "fr": {
        "title": "Plateforme Universitaire Nazaaha",
        "login": "Connexion",
        "signup": "Inscription",
        "email": "Email",
        "password": "Mot de passe",
        "welcome": "Bienvenue à",
        "points": "Points de Savoir",
        "library": "Bibliothèque",
        "upload": "Publier",
        "quiz": "Quiz",
        "settings": "Paramètres",
        "buy": "Acheter",
        "price": "Prix",
        "downloads": "Téléchargements",
        "upload_btn": "Soumettre pour évaluation",
        "ai_check": "Analyse AI en cours...",
        "logout": "Déconnexion",
        "level": "Niveau d'étude",
        "specialty": "Spécialité",
        "faculty": "Faculté",
        "fb_login": "Continuer avec Facebook"
    },
    "en": {
        "title": "Nazaaha University Platform",
        "login": "Login",
        "signup": "Sign Up",
        "email": "Email",
        "password": "Password",
        "welcome": "Welcome to",
        "points": "Knowledge Points",
        "library": "Library",
        "upload": "Upload",
        "quiz": "Quiz",
        "settings": "Settings",
        "buy": "Buy & Download",
        "price": "Price",
        "downloads": "Downloads",
        "upload_btn": "Upload for Evaluation",
        "ai_check": "AI Analyzing...",
        "logout": "Logout",
        "level": "Study Level",
        "specialty": "Major",
        "faculty": "Faculty",
        "fb_login": "Continue with Facebook"
    }
}

# --- 3. قاعدة بيانات جامعة قسنطينة 3 (محاكاة) ---
const_3_faculties = {
    "كلية الهندسة المعمارية والتعمير": ["هندسة معمارية", "تسيير المدن", "عمارة بيئية"],
    "كلية الفنون والثقافة": ["فنون تشكيلية", "فنون العرض", "سينما وتلفزيون", "دراسات نقدية"],
    "كلية الطب": ["طب عام", "صيدلة", "طب أسنان"],
    "كلية هندسة الطرائق": ["هندسة كيميائية", "هندسة صيدلانية", "هندسة البيئة"],
    "كلية العلوم السياسية": ["نظم سياسية", "علاقات دولية", "إدارة عامة"],
    "كلية علوم الإعلام والاتصال": ["صحافة", "اتصال جماهيري", "علاقات عامة"],
    "معهد تسيير التقنيات الحضرية": ["تسيير المدن", "تقنيات حضرية"]
}

study_levels = ["الليسانس (Licence)", "الماستر (Master)", "الدكتوراه (Doctorate)", "مدرسة عليا (Grande École)"]

# --- 4. إدارة البيانات (Session State) ---
if 'users' not in st.session_state:
    # مستخدم افتراضي للتجربة
    st.session_state['users'] = {
        "student@univ-constantine3.dz": {
            "password": "123",
            "name": "طالب مجتهد",
            "faculty": "كلية الهندسة المعمارية والتعمير",
            "specialty": "هندسة معمارية",
            "level": "الماستر (Master)",
            "points": 100,
            "avatar": "👨‍🎓",
            "my_books": [], # الكتب التي اشتراها
            "interests": ["التصميم", "تاريخ العمارة"]
        }
    }
if 'current_user' not in st.session_state: st.session_state['current_user'] = None
if 'lang' not in st.session_state: st.session_state['lang'] = "ar"
if 'books' not in st.session_state:
    # كتب أولية في النظام
    st.session_state['books'] = [
        {"id": 1, "title": "مبادئ العمارة الإسلامية", "price": 45, "downloads": 5, "uploader": "system", "type": "كتاب"},
        {"id": 2, "title": "Introduction à l'Urbanisme", "price": 50, "downloads": 12, "uploader": "system", "type": "كتاب"},
        {"id": 3, "title": "الذكاء الاصطناعي في الطب", "price": 60, "downloads": 20, "uploader": "system", "type": "مقال"},
    ]

# دالة الترجمة المساعدة
def t(key):
    lang = st.session_state['lang']
    return translations[lang].get(key, key)

# --- 5. التصميم CSS ---
def apply_css():
    direction = "rtl" if st.session_state['lang'] == "ar" else "ltr"
    align = "right" if st.session_state['lang'] == "ar" else "left"
    
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        
        html, body, [class*="css"] {{
            font-family: 'Cairo', sans-serif;
            direction: {direction};
            text-align: {align};
        }}
        
        /* تحسين كروت الكتب */
        .book-card {{
            background: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
            margin-bottom: 10px;
            transition: transform 0.2s;
        }}
        .book-card:hover {{
            transform: translateY(-3px);
            border-color: #3b82f6;
        }}
        
        /* زر الفيسبوك */
        .fb-btn {{
            background-color: #1877F2;
            color: white;
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            border: none;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 10px;
        }}
        
        /* شارة النقاط */
        .points-badge {{
            background-color: #f59e0b;
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            font-weight: bold;
        }}
    </style>
    """, unsafe_allow_html=True)

apply_css()

# --- 6. الصفحات ---

def login_page():
    st.markdown(f"<h1 style='text-align: center; color:#1e3a8a;'>{t('title')}</h1>", unsafe_allow_html=True)
    
    # اختيار اللغة في صفحة الدخول
    col_l, col_r = st.columns(2)
    with col_l:
        lang_choice = st.selectbox("Language / اللغة", ["العربية", "Français", "English"])
        if lang_choice == "العربية": st.session_state['lang'] = "ar"
        elif lang_choice == "Français": st.session_state['lang'] = "fr"
        else: st.session_state['lang'] = "en"
        
    tab1, tab2 = st.tabs([t("login"), t("signup")])
    
    with tab1:
        st.markdown(f"""<button class="fb-btn">📘 {t('fb_login')}</button>""", unsafe_allow_html=True)
        st.markdown("---")
        email = st.text_input(t("email"), key="l_email")
        password = st.text_input(t("password"), type="password", key="l_pass")
        
        if st.button(t("login"), use_container_width=True):
            user = st.session_state['users'].get(email)
            if user and user['password'] == password:
                st.session_state['current_user'] = email
                st.success("✅")
                st.rerun()
            else:
                st.error("خطأ في البيانات / Erreur de données")

    with tab2:
        new_email = st.text_input(t("email"), key="s_email")
        new_pass = st.text_input(t("password"), type="password", key="s_pass")
        new_name = st.text_input("الاسم الكامل / Full Name")
        
        # بيانات الجامعة
        st.markdown("### بيانات الطالب (جامعة قسنطينة 3)")
        faculty = st.selectbox(t("faculty"), list(const_3_faculties.keys()))
        specialty = st.selectbox(t("specialty"), const_3_faculties[faculty])
        level = st.selectbox(t("level"), study_levels)
        
        # الاهتمامات
        interests = st.multiselect("مجالات الاهتمام / Interests", 
                                 ["الذكاء الاصطناعي", "الأدب", "التاريخ", "العلوم", "الفنون", "السياسة", "الهندسة"])

        if st.button(t("signup"), use_container_width=True):
            if new_email in st.session_state['users']:
                st.error("البريد مسجل مسبقاً")
            else:
                st.session_state['users'][new_email] = {
                    "password": new_pass,
                    "name": new_name,
                    "faculty": faculty,
                    "specialty": specialty,
                    "level": level,
                    "points": 100, # مكافأة التسجيل
                    "avatar": "👤",
                    "my_books": [],
                    "interests": interests
                }
                st.success("تم التسجيل! سجل دخولك الآن.")

def main_app():
    user_email = st.session_state['current_user']
    user_data = st.session_state['users'][user_email]
    
    # القائمة الجانبية
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135768.png", width=80)
        st.markdown(f"### {user_data['avatar']} {user_data['name']}")
        st.markdown(f"**{t('points')}:** <span class='points-badge'>{user_data['points']} XP</span>", unsafe_allow_html=True)
        st.caption(f"{user_data['faculty']} | {user_data['specialty']}")
        st.divider()
        
        menu = st.radio("", [t("library"), t("upload"), t("quiz"), t("settings")])
        
        st.divider()
        if st.button(t("logout")):
            st.session_state['current_user'] = None
            st.rerun()

    # المحتوى الرئيسي
    st.title(f"{t('welcome')} {t('title')}")
    
    # --- 1. المكتبة (الاقتصاد) ---
    if menu == t("library"):
        st.subheader(f"📚 {t('library')}")
        
        # فلترة الكتب
        search = st.text_input("🔍 بحث عن كتاب...", "")
        
        col1, col2 = st.columns(2)
        for book in st.session_state['books']:
            if search in book['title']:
                current_price = book['price'] + book['downloads'] # السعر يزود مع التحميلات
                
                with st.container():
                    st.markdown(f"""
                    <div class="book-card">
                        <h4>📖 {book['title']}</h4>
                        <p style="color:gray; font-size:0.9em;">{book['type']} | {t('downloads')}: {book['downloads']}</p>
                        <p><b>{t('price')}: {current_price} XP</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # منطق الشراء
                    if book['id'] in user_data['my_books']:
                        st.info("✅ تملك هذا الكتاب")
                    else:
                        if st.button(f"{t('buy')} (-{current_price})", key=f"btn_{book['id']}"):
                            if user_data['points'] >= current_price:
                                # خصم من المشتري
                                user_data['points'] -= current_price
                                user_data['my_books'].append(book['id'])
                                
                                # تحديث الكتاب
                                book['downloads'] += 1
                                
                                # مكافأة الناشر (صاحب الكتاب)
                                uploader_email = book['uploader']
                                if uploader_email in st.session_state['users']:
                                    st.session_state['users'][uploader_email]['points'] += current_price
                                    st.toast(f"💰 تم تحويل {current_price} نقطة للناشر!", icon="💸")
                                
                                st.success("تم الشراء بنجاح!")
                                st.rerun()
                            else:
                                st.error("لا تملك نقاطاً كافية!")

    # --- 2. رفع الملفات (الذكاء الاصطناعي) ---
    elif menu == t("upload"):
        st.subheader(f"📤 {t('upload')}")
        st.info("💡 ملاحظة: يجب أن يكون المحتوى أكاديمياً. الذكاء الاصطناعي سيقوم بتقييمه.")
        
        title = st.text_input("عنوان الكتاب/البحث")
        desc = st.text_area("ملخص قصير")
        file = st.file_uploader("اختر ملف PDF", type="pdf")
        
        if file and st.button(t("upload_btn")):
            with st.spinner(t("ai_check")):
                time.sleep(3) # محاكاة قراءة الذكاء الاصطناعي للكتاب
                
                # محاكاة التقييم
                ai_score = random.randint(40, 100) # جودة الكتاب
                is_academic = True if ai_score > 50 else False
                
                if is_academic:
                    initial_price = random.randint(40, 60)
                    st.balloons()
                    st.success(f"✅ تمت الموافقة! تقييم الجودة: {ai_score}%")
                    st.markdown(f"**تم تحديد السعر الأولي بـ: {initial_price} نقطة**")
                    st.markdown("سيتم إضافة نقاط لحسابك كلما قام شخص بتحميل كتابك.")
                    
                    # إضافة الكتاب للنظام
                    new_book = {
                        "id": len(st.session_state['books']) + 1,
                        "title": title,
                        "price": initial_price,
                        "downloads": 0,
                        "uploader": user_email,
                        "type": "محتوى أكاديمي"
                    }
                    st.session_state['books'].append(new_book)
                else:
                    st.error("❌ نأسف، المحتوى لا يبدو أكاديمياً كفاية حسب معايير المنصة.")

    # --- 3. لعبة "لخص لي" (Gamification) ---
    elif menu == t("quiz"):
        st.subheader("🧠 لعبة 'لخص لي' (Quiz Game)")
        
        if not user_data['my_books']:
            st.warning("يجب أن تشتري كتباً أولاً لتلعب هذا التحدي!")
        else:
            # جلب الكتب التي يملكها المستخدم
            my_books_info = [b for b in st.session_state['books'] if b['id'] in user_data['my_books']]
            book_to_quiz = st.selectbox("اختر كتاباً قرأته لتختبر فهمك:", [b['title'] for b in my_books_info])
            
            if st.button("بدء التحدي (محاكاة الذكاء الاصطناعي)"):
                with st.status("جاري توليد أسئلة من الكتاب..."):
                    time.sleep(2)
                    st.write("قراءة الفصول...")
                    time.sleep(1)
                    st.write("صياغة الأسئلة...")
                
                st.markdown(f"### سؤال حول: {book_to_quiz}")
                st.write("ما هي الفكرة الرئيسية في الفصل الثاني حسب السياق الأكاديمي؟")
                
                # خيارات وهمية
                ans = st.radio("اختر الإجابة:", ["النظرية التفكيكية", "التحليل الإحصائي", "تاريخ العمارة", "لا شيء مما سبق"])
                
                if st.button("تأكيد الإجابة"):
                    # نتيجة عشوائية للمحاكاة
                    win = random.choice([True, False])
                    if win:
                        reward = 20
                        user_data['points'] += reward
                        st.balloons()
                        st.success(f"إجابة صحيحة! كسبت {reward} نقطة.")
                    else:
                        penalty = 10
                        user_data['points'] -= penalty
                        st.error(f"إجابة خاطئة. خسرت {penalty} نقطة. اقرأ الكتاب جيداً!")

    # --- 4. الإعدادات ---
    elif menu == t("settings"):
        st.subheader(f"⚙️ {t('settings')}")
        
        with st.expander("تغيير اللغة / Change Language"):
            l = st.radio("اللغة", ["العربية", "Français", "English"])
            if st.button("حفظ اللغة"):
                if l == "العربية": st.session_state['lang'] = "ar"
                elif l == "Français": st.session_state['lang'] = "fr"
                else: st.session_state['lang'] = "en"
                st.rerun()

        with st.expander("تغيير صورة البروفيل"):
            avatars = ["👨‍🎓", "👩‍🎓", "👨‍🏫", "👩‍🏫", "👨‍🔬", "👩‍🔬"]
            new_av = st.selectbox("اختر أيقونة", avatars)
            if st.button("حفظ الصورة"):
                user_data['avatar'] = new_av
                st.success("تم التحديث!")
                st.rerun()
                
        with st.expander("الأمان وكلمة المرور"):
            curr = st.text_input("كلمة المرور الحالية", type="password")
            new = st.text_input("كلمة المرور الجديدة", type="password")
            if st.button("تغيير كلمة المرور"):
                if curr == user_data['password']:
                    user_data['password'] = new
                    st.success("تم تغيير كلمة المرور بنجاح")
                else:
                    st.error("كلمة المرور الحالية غير صحيحة")

# --- تشغيل التطبيق ---
if st.session_state['current_user'] is None:
    login_page()
else:
    main_app()
