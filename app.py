import streamlit as st
import time
import random
import google.generativeai as genai
import os
from fpdf import FPDF
import base64

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="منصة نزاهة | جامعة قسنطينة 3",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- إعداد Gemini AI ---
api_key = os.environ.get("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- دوال مساعدة (PDF) ---
def create_pdf(title, author, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # ملاحظة: FPDF القياسية لا تدعم العربية بشكل كامل بدون ملفات خطوط خارجية
    # لذلك سنضع الترويسة باللاتينية لضمان عمل الملف
    pdf.cell(200, 10, txt="Nazaha Platform - Constantine 3 University", ln=1, align='C')
    pdf.cell(200, 10, txt=f"Title: {title}", ln=1, align='L')
    pdf.cell(200, 10, txt=f"Author: {author}", ln=1, align='L')
    pdf.line(10, 30, 200, 30)
    pdf.ln(20)
    # محتوى بسيط
    pdf.multi_cell(0, 10, txt="This document was downloaded from Nazaha Platform.\n\n" + content)
    
    return pdf.output(dest='S').encode('latin-1', 'ignore') 

# --- قاموس الترجمة (عربي / إنجليزي فقط) ---
TRANSLATIONS = {
    "ar": {
        "dir": "rtl",
        "title": "منصة نزاهة الأكاديمية",
        "tagline": "بوابتك نحو التميز الأكاديمي - جامعة قسنطينة 3",
        "login": "تسجيل الدخول",
        "signup": "إنشاء حساب جديد",
        "role_select": "من أنت؟",
        "student": "طالب",
        "professor": "أستاذ",
        "email": "البريد الإلكتروني",
        "password": "كلمة المرور",
        "full_name": "الاسم الكامل",
        "faculty": "الكلية",
        "specialty": "التخصص",
        "department": "القسم",
        "level": "السنة الدراسية",
        "dashboard": "لوحة القيادة",
        "library": "المكتبة الرقمية",
        "research_cell": "خلية البحوث",
        "review_research": "تحكيم البحوث",
        "upload": "مركز النشر",
        "quiz": "تحدي المعرفة",
        "ai_chat": "المساعد الأكاديمي (AI)",
        "settings": "الإعدادات",
        "logout": "خروج",
        "welcome": "مرحباً،",
        "download_pdf": "تحميل PDF",
        "submit_research": "تقديم بحث",
        "research_title": "عنوان البحث",
        "research_abstract": "ملخص البحث",
        "status": "الحالة",
        "pending": "قيد المراجعة",
        "approved": "منشور",
        "approve": "قبول ونشر",
        "reject": "رفض",
        "no_research": "لا توجد بحوث للمراجعة حالياً.",
        "chat_intro": "أهلاً بك. أنا مساعدك الأكاديمي المتخصص. يمكنني مساعدتك في صياغة الإشكاليات، اقتراح المراجع، وتدقيق الاقتباسات لتجنب السرقة العلمية.",
        "chat_placeholder": "اسألني عن كيفية كتابة خطة بحث، أو كيفية التوثيق بطريقة APA...",
        "grade": "الرتبة العلمية",
        "buy": "شراء",
        "owned": "مملوك",
        "points": "نقطة",
        "comments": "تعليقات",
        "add_comment": "أضف تعليق..."
    },
    "en": {
        "dir": "ltr",
        "title": "Nazaha Academic Platform",
        "tagline": "Your gateway to excellence - Constantine 3 University",
        "login": "Login",
        "signup": "Create Account",
        "role_select": "Who are you?",
        "student": "Student",
        "professor": "Professor",
        "email": "Email",
        "password": "Password",
        "full_name": "Full Name",
        "faculty": "Faculty",
        "specialty": "Specialty",
        "department": "Department",
        "level": "Year of Study",
        "dashboard": "Dashboard",
        "library": "Library",
        "research_cell": "Research Cell",
        "review_research": "Review Research",
        "upload": "Upload Center",
        "quiz": "Knowledge Challenge",
        "ai_chat": "Academic Assistant (AI)",
        "settings": "Settings",
        "logout": "Logout",
        "welcome": "Welcome, ",
        "download_pdf": "Download PDF",
        "submit_research": "Submit Research",
        "research_title": "Research Title",
        "research_abstract": "Abstract",
        "status": "Status",
        "pending": "Pending Review",
        "approved": "Published",
        "approve": "Approve & Publish",
        "reject": "Reject",
        "no_research": "No research to review.",
        "chat_intro": "Welcome. I am your specialized academic assistant. I can help you formulate problems, suggest references, and check citations to avoid plagiarism.",
        "chat_placeholder": "Ask me how to write a research plan, or how to cite in APA...",
        "grade": "Academic Grade",
        "buy": "Buy",
        "owned": "Owned",
        "points": "XP",
        "comments": "Comments",
        "add_comment": "Add comment..."
    }
}

# --- البيانات ---
FACULTY_SPECIALTIES = {
    "Faculté de Médecine": ["Médecine", "Pharmacie", "Médecine Dentaire"],
    "Faculté d'Architecture et d'Urbanisme": ["Architecture", "Urbanisme", "Gestion des Villes"],
    "Faculté des NTIC": ["Informatique (GL)", "Informatique (SI)", "Réseaux et Télécom (RSD)"],
    "Faculté des Sciences Politiques": ["Sciences Politiques", "Relations Internationales"]
}

PROF_GRADES = ["Maitre Assistant B", "Maitre Assistant A", "Maitre de Conférence B", "Maitre de Conférence A", "Professeur"]

# --- إدارة الحالة ---
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'view' not in st.session_state: st.session_state.view = 'auth'
if 'user' not in st.session_state: st.session_state.user = None
if 'books' not in st.session_state: 
    st.session_state.books = [
        {"id": 1, "title": "Introduction à l'Architecture", "author": "Dr. Amine", "faculty": "Architecture", "price": 45, "downloads": 120, "comments": []},
        {"id": 2, "title": "Algorithmique Avancée", "author": "Prof. Sara", "faculty": "NTIC", "price": 60, "downloads": 45, "comments": []}
    ]
# قائمة البحوث الطلابية (المقدمة والموافقة عليها)
if 'student_research' not in st.session_state: st.session_state.student_research = [] 
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- دوال مساعدة ---
def t(key): return TRANSLATIONS[st.session_state.lang].get(key, key)
def set_view(v): st.session_state.view = v

# --- الذكاء الاصطناعي المحسن ---
def get_ai_response(prompt, user_context):
    # سياق النظام (System Prompt)
    system_prompt = f"""
    أنت مساعد أكاديمي ذكي في "منصة نزاهة" لجامعة قسنطينة 3.
    مهمتك: مساعدة الطلاب والأساتذة في البحث العلمي، صياغة الفرضيات، وتجنب السرقة العلمية.
    السياق الحالي للمستخدم: {user_context}
    
    تعليمات هامة:
    1. إذا طلب المستخدم كتابة بحث كامل، ارفض بتهذيب واعرض المساعدة في "الهيكلة" أو "التدقيق" فقط (للحفاظ على النزاهة).
    2. إذا سأل عن كيفية التوثيق، اشرح له أسلوب APA أو IEEE.
    3. كن دقيقاً ومختصراً واستخدم لغة أكاديمية رصينة.
    """
    
    if api_key:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            full_prompt = f"{system_prompt}\n\nسؤال المستخدم: {prompt}"
            response = model.generate_content(full_prompt)
            return response.text
        except:
            pass # Fallback to mock if API fails
            
    # المحاكي الذكي (Fallback)
    time.sleep(1.5)
    if "بحث" in prompt:
        return "لإعداد بحث متميز، يجب أن تبدأ بـ **إشكالية واضحة**. هل يمكنك صياغة السؤال الرئيسي لبحثك؟ سأساعدك في تحويله إلى فرضيات قابلة للدراسة."
    elif "سرقة" in prompt or "اقتباس" in prompt:
        return "النزاهة العلمية تتطلب التوثيق الدقيق. أي نص تأخذه من مصدر آخر يجب أن تضعه بين علامتي تنصيص وتذكر المصدر فوراً. هل تريد مثالاً على توثيق كتاب؟"
    elif "خطة" in prompt:
        return "الخطة النموذجية تتكون من: \n1. المقدمة (الإشكالية)\n2. الإطار النظري\n3. الجانب التطبيقي\n4. النتائج والتوصيات.\nما هو موضوعك لنفصل الخطة؟"
    else:
        return "أنا هنا لمساعدتك في رحلتك البحثية. يمكنك سؤالي عن المراجع، المنهجية، أو كيفية استخدام المنصة."

# --- CSS Styles ---
direction = TRANSLATIONS[st.session_state.lang]['dir']
st.markdown(f"""
<style>
    .main {{ direction: {direction}; text-align: {'right' if direction == 'rtl' else 'left'}; }}
    .stButton button {{ width: 100%; border-radius: 8px; }}
    .stTextInput input {{ border-radius: 8px; }}
    .block-container {{ direction: {direction}; }}
    div[data-testid="stMetricValue"] {{ direction: ltr; }}
    .stChatMessage {{ direction: {direction}; }}
    
    /* بطاقات مميزة */
    .card {{
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border: 1px solid #f0f0f0;
    }}
    .status-pending {{ color: #eab308; font-weight: bold; }}
    .status-approved {{ color: #22c55e; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# ================= واجهات التطبيق =================

def auth_view():
    st.markdown(f"<h1 style='text-align: center; color: #0ea5e9;'>{t('title')}</h1>", unsafe_allow_html=True)
    
    # تبديل اللغة
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("English", key="len"): st.session_state.lang = 'en'; st.rerun()
    with c2:
        if st.button("العربية", key="lar"): st.session_state.lang = 'ar'; st.rerun()

    tab_login, tab_signup = st.tabs([t('login'), t('signup')])
    
    # --- تسجيل الدخول ---
    with tab_login:
        with st.form("login_form"):
            email = st.text_input(t('email'))
            password = st.text_input(t('password'), type="password")
            submit = st.form_submit_button(t('login'))
            
            if submit:
                # محاكاة مستخدمين (واحد طالب وواحد أستاذ)
                if email == "prof@univ.dz":
                    st.session_state.user = {"name": "Dr. Ahmed", "role": "professor", "points": 500, "faculty": "NTIC", "library": []}
                    st.session_state.view = 'dashboard'
                    st.rerun()
                elif email == "student@univ.dz" or (email and password):
                    st.session_state.user = {"name": "Student Ali", "role": "student", "points": 100, "faculty": "NTIC", "level": "Master 2", "library": [], "uploads": []}
                    st.session_state.view = 'ai_chat' # توجيه الطالب للدردشة
                    st.rerun()
                else:
                    st.error("بيانات خاطئة (جرب prof@univ.dz أو student@univ.dz)")

    # --- التسجيل الجديد (الواجهة الجديدة) ---
    with tab_signup:
        st.subheader(t('role_select'))
        
        # اختيار الدور
        role = st.radio("", [t('student'), t('professor')], horizontal=True)
        
        with st.form("signup_form"):
            name = st.text_input(t('full_name'))
            email_reg = st.text_input(t('email'))
            pass_reg = st.text_input(t('password'), type="password")
            
            faculty = st.selectbox(t('faculty'), list(FACULTY_SPECIALTIES.keys()))
            
            if role == t('student'):
                specialty = st.selectbox(t('specialty'), FACULTY_SPECIALTIES.get(faculty, []))
                level = st.selectbox(t('level'), ["Licence 1", "Licence 2", "Licence 3", "Master 1", "Master 2", "Doctorat"])
            else:
                # حقول خاصة بالأستاذ
                department = st.text_input(t('department'))
                grade = st.selectbox(t('grade'), PROF_GRADES)

            submit_reg = st.form_submit_button(t('signup'))
            
            if submit_reg:
                if name and email_reg:
                    user_role = "student" if role == t('student') else "professor"
                    st.session_state.user = {
                        "name": name,
                        "email": email_reg,
                        "role": user_role,
                        "points": 200 if user_role == "student" else 1000,
                        "faculty": faculty,
                        "library": [],
                        "uploads": [] # للطلاب: بحوثهم، للأساتذة: منشوراتهم
                    }
                    if user_role == "student":
                        st.session_state.user["level"] = level
                        st.session_state.user["specialty"] = specialty
                    else:
                        st.session_state.user["grade"] = grade
                    
                    st.success("تم التسجيل بنجاح!")
                    time.sleep(1)
                    st.session_state.view = 'ai_chat' if user_role == "student" else 'dashboard'
                    st.rerun()

def sidebar_menu():
    user = st.session_state.user
    with st.sidebar:
        st.title("Nazaha Platform")
        st.caption(f"User: {user['name']} ({t(user['role'])})")
        
        if user['role'] == "student":
             st.metric(t('points'), user['points'])
        
        st.markdown("---")
        
        if st.button(f"🤖 {t('ai_chat')}"): set_view('ai_chat')
        if st.button(f"📊 {t('dashboard')}"): set_view('dashboard')
        if st.button(f"📚 {t('library')}"): set_view('library')
        
        # القائمة الخاصة بالبحوث تختلف حسب الدور
        if user['role'] == "student":
            if st.button(f"📝 {t('submit_research')}"): set_view('research_cell')
        else:
            if st.button(f"⚖️ {t('review_research')}"): set_view('review_research')
            
        if st.button(f"🧠 {t('quiz')}"): set_view('quiz')
        if st.button(f"⚙️ {t('settings')}"): set_view('settings')
        
        st.markdown("---")
        if st.button(f"🚪 {t('logout')}", type="primary"):
            st.session_state.user = None
            st.session_state.view = 'auth'
            st.rerun()

def ai_chat_view():
    st.title(f"🤖 {t('ai_chat')}")
    user = st.session_state.user
    
    if not st.session_state.chat_history:
        st.info(t('chat_intro'))
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input(t('chat_placeholder')):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            placeholder = st.empty()
            # بناء سياق للمستخدم
            context = f"المستخدم: {user['name']}، الدور: {user['role']}، الكلية: {user.get('faculty', 'غير محدد')}"
            response = get_ai_response(prompt, context)
            
            # تأثير الكتابة
            full_res = ""
            for chunk in response.split():
                full_res += chunk + " "
                time.sleep(0.05)
                placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
            
        st.session_state.chat_history.append({"role": "assistant", "content": full_res})

def research_cell_view():
    # واجهة الطالب لتقديم البحوث
    st.title(f"📝 {t('research_cell')}")
    st.info("هنا يمكنك تقديم بحوثك لمراجعتها من قبل الأساتذة. البحوث المتميزة سيتم نشرها في المكتبة.")
    
    with st.form("submit_research_form"):
        title = st.text_input(t('research_title'))
        abstract = st.text_area(t('research_abstract'))
        file = st.file_uploader("ملف البحث (PDF)", type="pdf")
        submit = st.form_submit_button(t('submit_research'))
        
        if submit and title and file:
            new_research = {
                "id": int(time.time()),
                "title": title,
                "abstract": abstract,
                "author": st.session_state.user['name'],
                "faculty": st.session_state.user['faculty'],
                "status": "pending", # معلق
                "date": time.strftime("%Y-%m-%d")
            }
            st.session_state.student_research.append(new_research)
            st.success("تم إرسال بحثك للمراجعة بنجاح!")

    # عرض حالة بحوثي
    st.subheader("بحوثي المقدمة")
    my_research = [r for r in st.session_state.student_research if r['author'] == st.session_state.user['name']]
    for r in my_research:
        status_color = "status-pending" if r['status'] == "pending" else "status-approved"
        status_text = t(r['status'])
        st.markdown(f"""
        <div class="card">
            <h4>{r['title']}</h4>
            <p>{r['abstract']}</p>
            <p class="{status_color}">{status_text}</p>
        </div>
        """, unsafe_allow_html=True)

def review_research_view():
    # واجهة الأستاذ لمراجعة البحوث
    st.title(f"⚖️ {t('review_research')}")
    
    # جلب البحوث المعلقة الخاصة بكلية الأستاذ
    prof_faculty = st.session_state.user['faculty']
    pending = [r for r in st.session_state.student_research if r['status'] == "pending" and r['faculty'] == prof_faculty]
    
    if not pending:
        st.info(t('no_research'))
    
    for r in pending:
        with st.container():
            st.markdown(f"""
            <div class="card">
                <h3>{r['title']}</h3>
                <p><strong>الطالب:</strong> {r['author']}</p>
                <p>{r['abstract']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"✅ {t('approve')}", key=f"app_{r['id']}"):
                    r['status'] = "approved"
                    # إضافة البحث للمكتبة العامة
                    st.session_state.books.append({
                        "id": r['id'],
                        "title": r['title'],
                        "author": r['author'],
                        "faculty": r['faculty'],
                        "price": 0, # بحوث الطلبة مجانية
                        "downloads": 0,
                        "comments": [],
                        "type": "research"
                    })
                    st.success(f"تم نشر البحث '{r['title']}'")
                    st.rerun()
            with c2:
                if st.button(f"❌ {t('reject')}", key=f"rej_{r['id']}"):
                    r['status'] = "rejected"
                    st.warning("تم رفض البحث")
                    st.rerun()

def library_view():
    st.title(f"📚 {t('library')}")
    
    # عرض البحوث المنشورة + الكتب
    books = st.session_state.books
    
    search = st.text_input("بحث...")
    filtered = [b for b in books if search.lower() in b['title'].lower()]
    
    for b in filtered:
        with st.container():
            st.markdown(f"<div class='card'><h3>{b['title']}</h3><p>👤 {b['author']} | 🏛️ {b['faculty']}</p></div>", unsafe_allow_html=True)
            
            # أزرار التفاعل
            c1, c2 = st.columns([1, 3])
            
            # التحقق من الملكية
            is_owned = False
            if 'library' in st.session_state.user:
                is_owned = any(item['id'] == b['id'] for item in st.session_state.user['library'])
            
            # الكتب البحثية مجانية، الكتب الأخرى بالنقاط
            is_free = b.get('type') == 'research'
            
            if is_owned or is_free:
                # توليد PDF حقيقي
                pdf_bytes = create_pdf(b['title'], b['author'], "This is the academic content of the book/research paper...")
                b64_pdf = base64.b64encode(pdf_bytes).decode('latin-1')
                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{b["title"]}.pdf" style="background-color:#22c55e;color:white;padding:8px 15px;text-decoration:none;border-radius:5px;display:block;text-align:center;">⬇️ {t("download_pdf")}</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                if st.button(f"{t('buy')} ({b['price']} {t('points')})", key=f"buy_{b['id']}"):
                    if st.session_state.user['points'] >= b['price']:
                        st.session_state.user['points'] -= b['price']
                        st.session_state.user['library'].append(b)
                        st.success(t('success_buy'))
                        st.rerun()
                    else:
                        st.error("نقاط غير كافية")

def dashboard_view():
    st.title(f"📊 {t('dashboard')}")
    user = st.session_state.user
    
    col1, col2 = st.columns(2)
    if user['role'] == 'student':
        col1.metric(t('points'), user['points'])
        col2.metric("مستوى", user.get('level', ''))
        
        st.subheader("مكتسباتي")
        if user['library']:
            for b in user['library']:
                st.write(f"✅ {b['title']}")
        else:
            st.info("لا توجد كتب بعد.")
            
    else:
        # لوحة الأستاذ
        col1.metric("البحوث المنشورة", len([r for r in st.session_state.student_research if r['status'] == 'approved']))
        col2.metric("الرتبة", user.get('grade', ''))
        st.info("انتقل إلى 'تحكيم البحوث' لمراجعة أعمال الطلبة.")

# --- الموجه الرئيسي ---
if st.session_state.user is None:
    auth_view()
else:
    sidebar_menu()
    if st.session_state.view == 'dashboard': dashboard_view()
    elif st.session_state.view == 'library': library_view()
    elif st.session_state.view == 'ai_chat': ai_chat_view()
    elif st.session_state.view == 'research_cell': research_cell_view()
    elif st.session_state.view == 'review_research': review_research_view()
    elif st.session_state.view == 'quiz': st.title(t('quiz')); st.info("قريباً...")
    elif st.session_state.view == 'settings': st.title(t('settings')); st.write("إعدادات الحساب...")
