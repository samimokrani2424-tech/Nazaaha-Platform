import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# --- 1. إعدادات الصفحة (يجب أن تكون أول أمر) ---
st.set_page_config(
    page_title="منصة نزاهة | الحوكمة الأكاديمية",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. تنسيق الواجهة (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* تحسين الأزرار */
    .stButton button {
        background-color: #0e76a8;
        color: white;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton button:hover {
        background-color: #005c85;
        transform: scale(1.02);
    }
    
    /* صناديق الرسائل */
    .success-box {
        padding: 15px;
        background-color: #d4edda;
        color: #155724;
        border-radius: 10px;
        margin-bottom: 10px;
        border-right: 5px solid #28a745;
    }
    .warning-box {
        padding: 15px;
        background-color: #fff3cd;
        color: #856404;
        border-radius: 10px;
        margin-bottom: 10px;
        border-right: 5px solid #ffc107;
    }
    
    /* تخصيص القائمة الجانبية */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. إدارة الحالة (Session State) ---
if 'points' not in st.session_state:
    st.session_state['points'] = 0
if 'level' not in st.session_state:
    st.session_state['level'] = 1
if 'badges' not in st.session_state:
    st.session_state['badges'] = []
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [
        {"user": "النظام", "message": "أهلاً بكم في منصة نزاهة. نناقش اليوم: هلوسة الذكاء الاصطناعي.", "time": datetime.now().strftime("%H:%M")}
    ]

# --- 4. الدوال المساعدة ---
def add_points(amount):
    st.session_state['points'] += amount
    st.toast(f'🎉 مذهل! حصلت على {amount} نقطة خبرة', icon="🌟")
    check_badges()

def check_badges():
    badges_map = {
        50: "مبتدئ واعد",
        150: "مدقق معرفي",
        300: "خبير النزاهة"
    }
    for score, badge in badges_map.items():
        if st.session_state['points'] >= score and badge not in st.session_state['badges']:
            st.session_state['badges'].append(badge)
            st.balloons()
            st.success(f"🏆 مبروك! فتحت وسام: {badge}")

# --- 5. القائمة الجانبية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135768.png", width=80)
    st.title("ملف الطالب")
    
    # شريط التقدم
    progress = min(st.session_state['points'] / 300, 1.0)
    st.progress(progress)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("المستوى", st.session_state['level'])
    with col_s2:
        st.metric("النقاط", st.session_state['points'])
    
    st.divider()
    st.subheader("الأوسمة المكتسبة")
    if not st.session_state['badges']:
        st.caption("لم تحصل على أوسمة بعد.")
    else:
        for b in st.session_state['badges']:
            st.markdown(f"🎖️ **{b}**")
            
    st.divider()
    st.info("نسخة الويب الحية v1.0")

# --- 6. الصفحات الرئيسية ---
tabs = st.tabs(["🏠 الرئيسة", "🤖 التدريب العملي", "📚 المكتبة والمصادر", "💬 المجتمع"])

# الصفحة 1: الرئيسة
with tabs[0]:
    st.title("منصة نزاهة للحوكمة الأكاديمية")
    st.markdown("""
    ### عن المنصة
    منصة تفاعلية تهدف لتعزيز **النزاهة الإبستيمولوجية** عند استخدام الذكاء الاصطناعي في البحث العلمي والفنون.
    
    #### المحاور الأساسية:
    * 🚫 **مكافحة الهلوسة:** كيف نمنع النماذج من اختلاق المعلومات.
    * ⚖️ **العدالة الخوارزمية:** تجنب التحيز في النتائج.
    * 📝 **التوثيق:** طرق الاقتباس الصحيحة (APA).
    """)
    
    st.warning("💡 تذكر: الذكاء الاصطناعي هو 'مساعد' وليس 'بديلاً' عن عقلك النقدي.")

# الصفحة 2: التدريب (مدرب البرومت)
with tabs[1]:
    st.header("🤖 مختبر هندسة البرومت")
    
    lvl = st.session_state['level']
    
    if lvl == 1:
        st.subheader("المستوى 1: الهلوسة (Hallucination)")
        st.markdown("**التحدي:** تريد معلومات عن تاريخ الفن الحديث، لكن تخشى أن يختلق النموذج أسماء فنانين غير موجودين. اكتب برومت يجبره على الدقة.")
        
        u_prompt = st.text_area("اكتب الأمر هنا:", key="p1")
        if st.button("تحقق من البرومت", key="b1"):
            strong_words = ["مصدر", "مراجع", "تأكد", "حقيقي", "citations", "references"]
            if any(w in u_prompt for w in strong_words) and len(u_prompt) > 15:
                st.markdown('<div class="success-box">✅ **ممتاز!** طلبك للمصادر هو خط الدفاع الأول ضد الهلوسة.</div>', unsafe_allow_html=True)
                add_points(50)
                st.session_state['level'] = 2
                time.sleep(1)
                st.rerun()
            else:
                st.markdown('<div class="warning-box">⚠️ **حاول مجدداً:** لم تطلب إثباتات أو مصادر. هذا قد يؤدي لمعلومات مغلوطة.</div>', unsafe_allow_html=True)
    
    elif lvl == 2:
        st.subheader("المستوى 2: التحيز (Bias)")
        st.markdown("**التحدي:** اكتب برومت لتوليد صورة لـ 'أطباء في المستشفى'. كيف تضمن أن الصورة لا تظهر فقط رجالاً أو عرقاً واحداً؟")
        
        u_prompt = st.text_area("اكتب الأمر هنا:", key="p2")
        if st.button("تحقق من البرومت", key="b2"):
            bias_words = ["تنوع", "جنسين", "خلفيات", "diverse", "inclusive", "gender"]
            if any(w in u_prompt for w in bias_words):
                st.markdown('<div class="success-box">✅ **رائع!** تحديد التنوع صراحةً يقلل من التحيز الخوارزمي.</div>', unsafe_allow_html=True)
                add_points(100)
                st.session_state['level'] = 3
                time.sleep(1)
                st.rerun()
            else:
                st.markdown('<div class="warning-box">⚠️ **تنبيه:** البرومت عام جداً، وسيعتمد النموذج على الصور النمطية (Stereotypes). حدد التنوع.</div>', unsafe_allow_html=True)
                
    elif lvl == 3:
        st.success("🎉 أنت الآن 'خبير نزاهة'! لقد أتممت التدريب الأساسي.")
        st.markdown("يمكنك الآن مساعدة زملائك في قسم المجتمع.")

# الصفحة 3: المكتبة
with tabs[2]:
    st.header("📚 المصادر والمراجع")
    
    refs = [
        {"name": "ورقة: الذكاء الاصطناعي في فضاء الفنون", "type": "DOCX", "link": "#"},
        {"name": "ميثاق الألكسو لأخلاقيات AI", "type": "PDF", "link": "#"},
        {"name": "دليل التوثيق بنظام APA 7", "type": "Web", "link": "#"}
    ]
    
    for r in refs:
        with st.expander(f"📄 {r['name']}"):
            st.write(f"النوع: {r['type']}")
            st.button(f"تحميل الملف", key=r['name'])

# الصفحة 4: المجتمع
with tabs[3]:
    st.header("💬 النقاش الحي")
    
    for chat in st.session_state['chat_history']:
        with st.chat_message(chat["user"]):
            st.write(chat["message"])
            st.caption(chat["time"])
            
    msg = st.chat_input("اكتب رسالتك هنا...")
    if msg:
        # إضافة رسالة المستخدم
        st.session_state['chat_history'].append({
            "user": "أنا",
            "message": msg,
            "time": datetime.now().strftime("%H:%M")
        })
        
        # محاكاة رد تلقائي (لجعل الموقع يبدو حياً)
        time.sleep(1.5)
        replies = [
            "نقطة مثيرة للاهتمام!",
            "هل يمكنك توضيح كيف يؤثر ذلك على البحث النوعي؟",
            "أتفق معك تماماً.",
            "شكراً لمشاركتك هذه الفكرة."
        ]
        st.session_state['chat_history'].append({
            "user": "زميل",
            "message": random.choice(replies),
            "time": datetime.now().strftime("%H:%M")
        })
        st.rerun()
