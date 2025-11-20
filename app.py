import streamlit as st
import time
import re  # مكتبة للتحقق من صيغة الإيميل

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="بوابة الطالب | جامعة قسنطينة 3",
    page_icon="🎓",
    layout="centered",  # جعلناها في الوسط للتركيز على الدخول
    initial_sidebar_state="collapsed" # إخفاء القائمة الجانبية في البداية
)

# --- 2. التصميم البصري (The Visual Engine) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    
    /* الخلفية العامة والخطوط */
    .stApp {
        background-color: #f0f2f5;
        font-family: 'Tajawal', sans-serif;
    }
    
    /* تنسيق العناوين */
    h1, h2, h3 {
        font-family: 'Tajawal', sans-serif;
        font-weight: 900;
        color: #1a1a1a;
        text-align: center;
    }
    
    /* بطاقة تسجيل الدخول (Glassmorphism) */
    .login-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-top: 2rem;
        border: 1px solid #e1e4e8;
    }
    
    /* تحسين حقول الإدخال */
    .stTextInput input {
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #ddd;
        text-align: right;
        font-family: 'Tajawal', sans-serif;
    }
    .stTextInput input:focus {
        border-color: #1877F2;
        box-shadow: 0 0 0 2px rgba(24, 119, 242, 0.2);
    }
    
    /* أزرار مخصصة */
    .stButton button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    /* زر تسجيل الدخول الرئيسي */
    div[data-testid="stVerticalBlock"] > div:nth-child(5) button {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        border: none;
        height: 50px;
        font-size: 18px;
    }
    
    /* رسائل التنبيه */
    .validation-msg {
        font-size: 12px;
        margin-top: -10px;
        margin-bottom: 10px;
        text-align: right;
    }
    
</style>
""", unsafe_allow_html=True)

# --- 3. أدوات التحقق الخاصة (Logic Tools) ---

def validate_email_format(email):
    """أداة خاصة للتحقق من صيغة البريد الإلكتروني"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def simulate_facebook_auth():
    """أداة محاكاة الاتصال بسيرفرات فيسبوك"""
    msg_placeholder = st.empty()
    with st.spinner('جاري الاتصال بـ Meta Secure Servers...'):
        time.sleep(1.5)
        msg_placeholder.info("🔐 جاري التحقق من المصادقة الثنائية...")
        time.sleep(1.5)
        msg_placeholder.success("✅ تم التحقق من الحساب بنجاح!")
        time.sleep(1)
    msg_placeholder.empty()
    return True

# --- 4. إدارة الحالة (Session State) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = {}

# --- 5. واجهة التطبيق ---

# الشاشة 1: تسجيل الدخول (إذا لم يكن مسجلاً)
if not st.session_state['logged_in']:
    
    # شعار وعنوان
    st.markdown("<h1 style='color:#1877F2; margin-bottom:0;'>مرحباً بك 👋</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>بوابة الطالب الجامعية - جامعة قسنطينة 3</p>", unsafe_allow_html=True)

    # حاوية البطاقة
    col1, col2, col3 = st.columns([1, 8, 1]) # لضبط العرض في الوسط
    with col2:
        # بداية البطاقة
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # خيارات الدخول
        tab1, tab2 = st.tabs(["📧 البريد الإلكتروني", "📘 فيسبوك"])
        
        # --- خيار 1: البريد الإلكتروني ---
        with tab1:
            email = st.text_input("البريد الإلكتروني الجامعي", placeholder="example@univ-constantine3.dz")
            password = st.text_input("كلمة المرور", type="password", placeholder="••••••••")
            
            if st.button("تسجيل الدخول الآمن"):
                # 1. فحص الحقول الفارغة
                if not email or not password:
                    st.error("⚠️ يرجى ملء جميع الحقول")
                
                # 2. استخدام أداة فحص الإيميل
                elif not validate_email_format(email):
                    st.error("❌ صيغة البريد الإلكتروني غير صحيحة (تأكد من وجود @ و .)")
                
                # 3. فحص كلمة المرور (محاكاة)
                elif len(password) < 6:
                    st.error("🔒 كلمة المرور قصيرة جداً (يجب أن تكون 6 أحرف على الأقل)")
                
                # 4. النجاح
                else:
                    with st.spinner('جاري تشفير البيانات والتحقق...'):
                        time.sleep(1.5)
                        st.session_state['logged_in'] = True
                        st.session_state['user_info'] = {
                            "name": email.split('@')[0], # استخراج الاسم من الايميل
                            "email": email,
                            "method": "email"
                        }
                        st.success("✅ تم الدخول بنجاح!")
                        st.rerun()

        # --- خيار 2: فيسبوك ---
        with tab2:
            st.info("💡 سيتم ربط حسابك الجامعي بحساب فيسبوك للتحقق من الهوية.")
            if st.button("متابعة باستخدام Facebook", type="primary"):
                if simulate_facebook_auth():
                    st.session_state['logged_in'] = True
                    st.session_state['user_info'] = {
                        "name": "Facebook User",
                        "email": "fb_user@example.com",
                        "method": "facebook"
                    }
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # تذييل بسيط
        st.markdown("""
        <div style='text-align: center; margin-top: 20px; color: gray; font-size: 12px;'>
        🔒 جميع البيانات مشفرة ومحفوظة وفق معايير الخصوصية
        </div>
        """, unsafe_allow_html=True)

# الشاشة 2: لوحة التحكم (بعد الدخول)
else:
    # إعادة ضبط الصفحة لتكون عريضة بعد الدخول
    
    # الهيدر العلوي
    st.markdown(f"""
    <div style="background: white; padding: 15px; border-radius: 15px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <div>
            <h3 style="margin:0; text-align: right; color: #1e3a8a;">أهلاً، {st.session_state['user_info']['name']} 🎓</h3>
        </div>
        <div style="background: #e0f2fe; color: #0369a1; padding: 5px 15px; border-radius: 20px; font-weight: bold;">
            طالب نشط ✅
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.success("🎉 نجحت الخطوة الأولى! تم تسجيل الدخول وحفظ البيانات.")
    st.info("نحن الآن داخل المنصة. بناءً على طلبك، سنقوم ببناء الأقسام التالية (الكتب، النقاط، الألعاب) خطوة بخطوة.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("تسجيل الخروج (للعودة للتجربة)"):
            st.session_state['logged_in'] = False
            st.session_state['user_info'] = {}
            st.rerun()
