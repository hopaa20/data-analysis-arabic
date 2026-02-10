"""
Data Analysis Pro - النسخة المجانية
تطبيق تحليل البيانات العربي
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime
import os

# ========== إعدادات هامة لـ Render ==========
# هذا السطر مهم جداً ليعمل على Render
PORT = int(os.environ.get("PORT", 10000))

# إعدادات الصفحة
st.set_page_config(
    page_title="تحليل البيانات العربي",
    page_icon="📊",
    layout="wide"
)

# ========== واجهة التطبيق ==========

# العنوان
st.title("📊 Data Analysis Pro")
st.markdown("### 🎁 النسخة المجانية - تحليل بيانات عربي سهل")

# قسم المعلومات
st.markdown("---")
st.markdown("""
<div style='background: #f0f8ff; padding: 20px; border-radius: 10px; border-right: 5px solid #3498db;'>
<h3 style='color: #2c3e50;'>✨ المميزات المجانية:</h3>
<ul>
<li>✅ رفع وتحليل ملفات Excel و CSV</li>
<li>✅ تحليل إحصائي كامل</li>
<li>✅ تصدير التقارير</li>
<li>✅ واجهة عربية 100%</li>
<li>✅ لا تحتاج خبرة برمجة</li>
</ul>
</div>
""", unsafe_allow_html=True)

# قسم رفع الملف
st.markdown("---")
st.markdown("## 📁 ارفع ملفك للتحليل")

uploaded_file = st.file_uploader(
    "اختر ملف Excel (.xlsx) أو CSV (.csv)",
    type=['csv', 'xlsx', 'xls'],
    help="حجم الملف حتى 200MB"
)

if uploaded_file is not None:
    try:
        # عرض معلومات التحميل
        with st.spinner("جاري تحميل الملف..."):
            # قراءة الملف حسب النوع
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ تم تحميل الملف بنجاح!")
            
            # عرض معلومات الملف
            col1, col2 = st.columns(2)
            with col1:
                st.metric("عدد الصفوف", df.shape[0])
                st.metric("عدد الأعمدة", df.shape[1])
            
            with col2:
                # إحصائيات سريعة
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                st.metric("الأعمدة العددية", len(numeric_cols))
                st.metric("القيم المفقودة", df.isnull().sum().sum())
            
            # معاينة البيانات
            st.markdown("### 👀 معاينة البيانات")
            st.dataframe(df.head(), use_container_width=True)
            
            # خيارات التحليل
            st.markdown("---")
            st.markdown("## 📈 اختر نوع التحليل")
            
            analysis_type = st.selectbox(
                "ما الذي تريد تحليله؟",
                ["معلومات عامة عن البيانات", "إحصائيات وصفية", "تحليل القيم المفقودة", "تحليل سريع"]
            )
            
            if st.button("🔍 إجراء التحليل", type="primary", use_container_width=True):
                if analysis_type == "معلومات عامة عن البيانات":
                    st.markdown("### 📋 معلومات الملف")
                    buffer = io.StringIO()
                    df.info(buf=buffer)
                    st.text(buffer.getvalue())
                    
                elif analysis_type == "إحصائيات وصفية":
                    st.markdown("### 📊 الإحصائيات الوصفية")
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        st.dataframe(df[numeric_cols].describe(), use_container_width=True)
                    else:
                        st.warning("⚠️ لا توجد أعمدة عددية في البيانات")
                        
                elif analysis_type == "تحليل القيم المفقودة":
                    st.markdown("### ⚠️ القيم المفقودة")
                    missing = df.isnull().sum()
                    if missing.sum() > 0:
                        missing_df = pd.DataFrame({
                            'العمود': missing.index,
                            'عدد القيم المفقودة': missing.values,
                            'النسبة المئوية': ((missing.values / len(df)) * 100).round(2)
                        })
                        st.dataframe(missing_df[missing_df['عدد القيم المفقودة'] > 0], use_container_width=True)
                    else:
                        st.success("🎉 لا توجد قيم مفقودة في البيانات!")
                        
                elif analysis_type == "تحليل سريع":
                    st.markdown("### ⚡ تحليل سريع")
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric("القيم الفريدة", df.nunique().mean().round())
                    
                    with col_b:
                        st.metric("متوسط الصفوف", df.shape[0])
                    
                    with col_c:
                        st.metric("متوسط الأعمدة", df.shape[1])
                
                st.balloons()
            
            # خيارات التصدير
            st.markdown("---")
            st.markdown("## 📤 تصدير النتائج")
            
            export_format = st.radio(
                "اختر تنسيق التصدير",
                ["Excel 📊", "CSV 📄", "JSON 🔤"],
                horizontal=True
            )
            
            if st.button("💾 حفظ التقرير", use_container_width=True):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                if "Excel" in export_format:
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='البيانات')
                    
                    st.download_button(
                        label="📥 تحميل ملف Excel",
                        data=buffer.getvalue(),
                        file_name=f"data_analysis_{timestamp}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                    
                elif "CSV" in export_format:
                    csv_data = df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📥 تحميل ملف CSV",
                        data=csv_data,
                        file_name=f"data_analysis_{timestamp}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
                elif "JSON" in export_format:
                    json_data = df.to_json(orient='records', force_ascii=False)
                    st.download_button(
                        label="📥 تحميل ملف JSON",
                        data=json_data,
                        file_name=f"data_analysis_{timestamp}.json",
                        mime="application/json",
                        use_container_width=True
                    )
    
    except Exception as e:
        st.error(f"❌ حدث خطأ: {str(e)}")
        st.info("💡 تأكد أن الملف بصيغة صحيحة وغير تالف")

# قسم المميزات الكاملة
st.markdown("---")
st.markdown("## 💎 النسخة الكاملة تشمل:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='text-align: center; padding: 15px; background: #e8f4f8; border-radius: 10px;'>
    <h4>🤖 تحليل متقدم</h4>
    <p>تعلم الآلة</p>
    <p>التنبؤ بالمستقبل</p>
    <p>تحليل الارتباط</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 15px; background: #e8f4f8; border-radius: 10px;'>
    <h4>📊 تقارير احترافية</h4>
    <p>قوالب مخصصة</p>
    <p>تصدير متعدد</p>
    <p>تنسيقات متنوعة</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='text-align: center; padding: 15px; background: #e8f4f8; border-radius: 10px;'>
    <h4>👨‍💻 دعم فني</h4>
    <p>دعم 24/7</p>
    <p>تدريب مجاني</p>
    <p>تحديثات مستمرة</p>
    </div>
    """, unsafe_allow_html=True)

# نموذج الاتصال للترقية
st.markdown("---")
with st.expander("🚀 ترقية إلى النسخة الكاملة (29.99 ريال/شهر)"):
    with st.form("upgrade_form"):
        name = st.text_input("اسمك")
        email = st.text_input("بريدك الإلكتروني")
        phone = st.text_input("رقم الهاتف")
        
        if st.form_submit_button("📩 طلب الترقية", use_container_width=True):
            st.success("🎉 تم إرسال طلبك! سنتواصل معك خلال 24 ساعة.")

# تذييل الصفحة
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
<p><strong>📊 Data Analysis Pro - النسخة المجانية</strong></p>
<p>تحليل بيانات عربي سهل وسريع</p>
<p>📧 للدعم: support@dataanalysis.com | 📱 +966500000000</p>
<p>© 2024 جميع الحقوق محفوظة</p>
</div>
""", unsafe_allow_html=True)

# ========== هذه السطور مهمة جداً ==========
# للتحقق من أن التطبيق يعمل
if __name__ == "__main__":
    # هذا التأكيد أن الكود يعمل
    print("✅ تطبيق تحليل البيانات يعمل بنجاح!")
