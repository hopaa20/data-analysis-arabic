"""
تطبيق تحليل البيانات العربي - النسخة المجانية
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="تحليل البيانات العربي",
    page_icon="📊",
    layout="wide"
)

# العنوان
st.title("📊 تطبيق تحليل البيانات العربي")
st.markdown("### 🎁 النسخة المجانية - جرب قبل الشراء")

# قسم رفع الملف
st.markdown("---")
st.markdown("## 📁 رفع ملف للتحليل")

uploaded_file = st.file_uploader(
    "اسحب وأسقط ملف Excel أو CSV هنا",
    type=['csv', 'xlsx'],
    help="يدعم ملفات CSV و Excel"
)

if uploaded_file is not None:
    try:
        # قراءة الملف
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ تم رفع الملف: {uploaded_file.name}")
        
        # عرض معلومات الملف
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("الصفوف", df.shape[0])
        with col2:
            st.metric("الأعمدة", df.shape[1])
        with col3:
            numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
            st.metric("الأعمدة العددية", numeric_cols)
        
        # معاينة البيانات
        st.markdown("### 👀 معاينة البيانات")
        st.dataframe(df.head(), use_container_width=True)
        
        # التحليل الأساسي
        st.markdown("### 📈 تحليل أساسي")
        
        if st.button("🔍 إجراء التحليل الإحصائي"):
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) > 0:
                st.markdown("#### 📊 الإحصائيات الوصفية")
                st.dataframe(df[numeric_cols].describe(), use_container_width=True)
            else:
                st.warning("لا توجد أعمدة عددية في البيانات")
        
        # تصدير البيانات
        st.markdown("---")
        st.markdown("### 📤 تصدير النتائج")
        
        if st.button("💾 حفظ كملف Excel", use_container_width=True):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            buffer = io.BytesIO()
            
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='البيانات')
            
            st.download_button(
                label="📥 تحميل الملف",
                data=buffer.getvalue(),
                file_name=f"تحليل_{timestamp}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    except Exception as e:
        st.error(f"❌ حدث خطأ: {str(e)}")

# قسم المعلومات
st.markdown("---")
st.markdown("## ℹ️ معلومات عن التطبيق")

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.markdown("""
    ### ✅ المميزات المجانية:
    - رفع وتحليل 5 ملفات
    - تحليل إحصائي أساسي
    - تصدير النتائج
    - واجهة عربية
    """)

with col_info2:
    st.markdown("""
    ### 💎 النسخة المدفوعة:
    - رفع غير محدود
    - تحليل متقدم
    - تعلم الآلة
    - دعم فني 24/7
    - فقط 29.99 ريال/شهر
    """)

# التذييل
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
<p>📞 للدعم أو الترقية: ehab.naahda.it@gmail.com | +20101180699</p>
<p>© 2024 تطبيق تحليل البيانات العربي</p>
</div>
""", unsafe_allow_html=True)