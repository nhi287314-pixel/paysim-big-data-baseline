"""9B — Báo cáo nghiệp vụ. Năm vùng AFTER, không thay phép tính."""
import altair as alt
import pandas as pd
import streamlit as st
from dashboard_core import PAGES, fmt_int, fmt_float, fmt_pct, detector_metrics, render_page, render_confusion_matrix

PAGE_CONFIG=dict(page_title="PaySim | Business review",layout="centered",initial_sidebar_state="expanded")

# BEFORE Start — 9B.1
# Dashboard rộng với sidebar và tiêu đề vận hành.
# BEFORE END — 9B.1
# AFTER Start — 9B.1: trang báo cáo có khổ đọc, typography serif, mục lục ngang.
def setup():
    st.markdown('''<style>
   [data-testid="stAppViewContainer"] {background:#b99fb3;}[data-testid="stHeader"] {background:transparent;}
    .block-container {max-width:1200px;padding:1.5rem 3rem 3rem;background: #f7eee4;
    border-radius: 28px;margin-top: 3rem;margin-bottom: 3rem;}
    .block-container [data-testid="stVerticalBlock"] {gap:0.5rem !important;}
    .block-container h1 {margin-bottom:0.25rem !important;}
    .block-container [data-testid="stCaptionContainer"] {margin-top:0 !important;margin-bottom:0 !important;}
    [data-testid="stVerticalBlockBorderWrapper"] {
        background:#eadfe6;
        border:1px solid #dfcfd8;
        border-radius:18px;
        padding:0.8rem 1rem;
    }
    [data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background: #e8dddd;
}
    h1,h2,h3 {font-family:Georgia,serif!important;color:#302c23!important;}
    [data-testid="stMetric"] {padding:10px 0;border-bottom:1px solid #d9cfb9;}
    [data-testid="stMetricValue"] {font-family:Georgia,serif;font-size:2.3rem;color:#624d28;}
    .report-masthead {font:12px monospace;letter-spacing:4px;border-bottom:3px solid #302c23;padding-bottom:12px;color: #302c23;}[data-testid="stCaptionContainer"],
[data-testid="stSelectbox"] label {
    color: #302c23 !important;
}
.report-divider {border:0;height:2px;background:#302c23;margin:0.25rem 0 0.5rem;}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked),
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) * {
    font-weight: 700 !important;
}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    font-size: 16px !important;
}
[data-testid="stSidebar"] label[data-baseweb="radio"] > div:last-child {
    font-size: 18px !important;
}

    </style>''',unsafe_allow_html=True)
    st.sidebar.markdown(
        '<div class="report-masthead">PAYSIM / BUSINESS INTELLIGENCE</div>',
        unsafe_allow_html=True,
    )
    st.title("Giao dịch & rủi ro")
    st.caption("Báo cáo kết quả xử lý và chất lượng phát hiện gian lận")
    st.markdown('<hr class="report-divider">', unsafe_allow_html=True)

    return st.sidebar.radio(
        "Không gian phân tích",
        options=PAGES,
        format_func=lambda page: page,
        key="dashboard_page",
    )

# AFTER END — 9B.1

# BEFORE Start — 9B.2
# Sáu thẻ KPI giống nhau, ưu tiên tốc độ vận hành.
# BEFORE END — 9B.2
# AFTER Start — 9B.2: hai số liệu chủ đạo, số liệu vận hành đưa xuống cuối báo cáo.
def headline(s):
    left,right=st.columns([3,2])
    with left:
        with st.container(border=True):
            st.markdown("### 01 / Quy mô xử lý")
            st.metric("Spark đã xử lý",fmt_int(s.processed),delta=f"{fmt_int(s.lag)} đang chờ")
            st.caption(f"Nguồn đã phát {fmt_int(s.emitted)} giao dịch trong run này.")
    with right:
        with st.container(border=True):
            st.markdown("### 02 / Cảnh báo gian lận")
            st.metric("Fraud alerts",fmt_int(s.alerts_count),delta=fmt_pct(s.model['Alert rate']))
            st.caption("Alert là kết quả dự đoán, không đồng nghĩa fraud thực tế.")
# AFTER END — 9B.2

# BEFORE Start — 9B.3
# So sánh model bằng bảng trên một trang riêng.
# BEFORE END — 9B.3
# AFTER Start — 9B.3: đối chiếu chất lượng bằng thanh ngang trên trang báo cáo chính.
def comparison(s):
    st.markdown("### 03 / Chất lượng phát hiện")
    rows=[]
    for key,name in [('rule','Spark SQL rule'),('model','Spark MLlib')]:
        values=detector_metrics(s.evaluation,key)
        rows.extend({'Chỉ số':metric,'Detector':name,'Giá trị':values[metric]} for metric in ['Precision','Recall','F1'])
    chart=alt.Chart(pd.DataFrame(rows)).mark_bar(size=13).encode(
        y=alt.Y('Chỉ số:N',title=None),x=alt.X('Giá trị:Q',scale=alt.Scale(domain=[0,1]),axis=alt.Axis(format='%'),title=None),
        yOffset='Detector:N',color=alt.Color('Detector:N',scale=alt.Scale(range=['#b99862','#38665b']),legend=alt.Legend(orient='bottom')),
        tooltip=['Chỉ số','Detector',alt.Tooltip('Giá trị:Q',format='.2%')],
    ).properties(height=210)
    st.altair_chart(chart)
# AFTER END — 9B.3

# BEFORE Start — 9B.4
# Phân phối giao dịch là donut ở trang dòng dữ liệu.
# BEFORE END — 9B.4
# AFTER Start — 9B.4: phân phối bằng thanh ngang, confusion matrix đặt cạnh kết quả model.
def business(s):
    left,right=st.columns([3,2])
    with left: comparison(s)
    with right:
        st.markdown("### Kết quả phân loại")
        render_confusion_matrix(s.model)
    st.markdown("### 04 / Cơ cấu giao dịch")
    if s.aggregates:
        chart=alt.Chart(pd.DataFrame(s.aggregates)).mark_bar(color='#38665b',cornerRadiusEnd=4).encode(
            y=alt.Y('type:N',sort='-x',title=None,axis=alt.Axis(labelOverlap=False)),x=alt.X('transactions:Q',title='Số giao dịch'),
            tooltip=['type','transactions','total_amount','model_alerts','rule_alerts'],
        ).properties(height=210)
        st.altair_chart(chart)
# AFTER END — 9B.4

# BEFORE Start — 9B.5
# Biểu đồ vận hành và sơ đồ pipeline đứng trước phần nghiệp vụ.
# BEFORE END — 9B.5
# AFTER Start — 9B.5: báo cáo nghiệp vụ trước; chỉ số vận hành và phụ lục ở cuối.
def render(s,page):
    headline(s)
    st.markdown("### Thông số vận hành")
    a,b,c,d=st.columns(4)
    with a:
        with st.container(border=True):
            st.metric('Nguồn đã phát',fmt_int(s.emitted))
    with b:
        with st.container(border=True):
            st.metric('Ingest hiện tại',f"{fmt_float(s.run.get('instant_emission_rate'))} ev/s")
    with c:
        with st.container(border=True):
            st.metric('Processing throughput',f"{fmt_float(s.latest_metric.get('processing_throughput'))} ev/s")
    with d:
        with st.container(border=True):
            st.metric('End-to-end latency p95',f"{fmt_float(s.latest_metric.get('latency_p95_ms'),0)} ms")
    if page==PAGES[0]: business(s)
    else: render_page(s,page)
    with st.expander("Phụ lục: telemetry theo micro-batch"):
        render_page(s,PAGES[0])
    st.caption(f"Dataset cycle {s.run.get('source_cycle',1)} · dòng {fmt_int(s.run.get('source_row'))}/{fmt_int(s.run.get('dataset_rows'))} · tiến độ {min(float(s.run.get('source_progress_pct',0)),1.0):.2%}")
    st.caption("Nguồn: snapshot MongoDB của run đang hiển thị · cập nhật mỗi 2 giây")
    st.sidebar.caption(f"RUN {s.run_id}  /  {s.status.upper()}")
# AFTER END — 9B.5
