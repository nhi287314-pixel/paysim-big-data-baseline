"""9B — Báo cáo nghiệp vụ. Năm vùng AFTER, không thay phép tính."""
import altair as alt
import pandas as pd
import streamlit as st
from pathlib import Path
from dashboard_core import PAGES, fmt_int, fmt_float, fmt_pct, detector_metrics, render_page, render_confusion_matrix

ASSET_DIR = Path(__file__).resolve().parent / "assets"

PAGE_CONFIG=dict(page_title="PaySim | Business review",page_icon="💰",layout="centered",initial_sidebar_state="expanded")

# BEFORE Start — 9B.1
# Dashboard rộng với sidebar và tiêu đề vận hành.
# BEFORE END — 9B.1
# AFTER Start — 9B.1: trang báo cáo có khổ đọc, typography serif, mục lục ngang.
def setup():
    st.markdown('''<style>
   [data-testid="stAppViewContainer"] {background:#1F3F74;}[data-testid="stHeader"] {background:transparent;}
    .block-container {max-width:1200px;padding:1.5rem 3rem 3rem;background: #e9f3ff;
    border-radius: 28px;margin-top: 3rem;margin-bottom: 3rem;}
    .block-container [data-testid="stVerticalBlock"] {gap:0.5rem !important;}
    .block-container h1 {margin-bottom:0.25rem !important;}
    .block-container [data-testid="stCaptionContainer"] {margin-top:0 !important;margin-bottom:0 !important;}

[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlockBorderWrapper"] > div,
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
    background-color: #e8d9ed !important;
    border-radius: 20px !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    padding: 0.2rem 0.5rem !important;
}

[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
    gap: 0.2 rem !important;
}
    [data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background: #EDF1F6;
}
    h1,h2,h3 {font-family:Times New Roman,serif!important;color:#302c23!important;}
    [data-testid="stMetric"] {padding:10px 0;border-bottom:1px solid #d9cfb9;}
    [data-testid="stMetricValue"] {font-family:Georgia,serif;font-size:2.3rem;color:#624d28;}
    .report-masthead {font:12px monospace;letter-spacing:4px;border-bottom:3px solid #302c23;padding-bottom:12px;color: #302c23;}[data-testid="stCaptionContainer"],
[data-testid="stSelectbox"] label {
    color: #302c23 !important;
}
.stSidebar .report-masthead {font-size:10px;letter-spacing:2px;line-height:1.6;overflow-wrap:anywhere;}
.report-divider {border:0;height:2px;background:#302c23;margin:0.25rem 0 0.5rem;}
.page-title {text-align:center;}
.page-subtitle {text-align:center;color:#85837d;font-size:1.1rem;margin-top:0;}
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
.st-key-processing-card,
.st-key-processing-card [data-testid="stVerticalBlock"],
.st-key-processing-card [data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFF9F0 !important;
    border-radius: 20px !important;
}
.st-key-fraud-card,
.st-key-fraud-card [data-testid="stVerticalBlock"],
.st-key-fraud-card [data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #D0E3FF !important;
    border-radius: 20px !important;
}
.st-key-high-risk-card,
.st-key-high-risk-card [data-testid="stVerticalBlock"],
.st-key-high-risk-card [data-testid="stVerticalBlockBorderWrapper"],
.st-key-high-risk-card [data-testid="stVerticalBlockBorderWrapper"] > div,
.st-key-high-risk-card [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
    background-color: #D0E3FF !important;
    border-radius: 20px !important;
}
.st-key-flagged-amount-card,
.st-key-flagged-amount-card [data-testid="stVerticalBlock"],
.st-key-flagged-amount-card [data-testid="stVerticalBlockBorderWrapper"],
.st-key-flagged-amount-card [data-testid="stVerticalBlockBorderWrapper"] > div,
.st-key-flagged-amount-card [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
    background-color: #FFF9F0 !important;
    border-radius: 20px !important;
}
.st-key-new-data-filters,
.st-key-new-data-filters [data-testid="stVerticalBlock"] {
    background-color: #D0E3FF !important;
    border: 1px solid #B8CCE8;
    border-radius: 18px !important;
    padding: 0.5rem;
}
.st-key-record-lookup-panel,
.st-key-record-lookup-panel [data-testid="stVerticalBlock"],
.st-key-record-lookup-panel [data-testid="stExpander"],
.st-key-record-lookup-panel [data-testid="stExpander"] details,
.st-key-record-lookup-panel [data-testid="stExpander"] details > div,
.st-key-record-lookup-panel [data-testid="stExpander"] details > div > div {
    background-color: #FFFFFF !important;
}
.st-key-record-lookup-panel,
.st-key-record-lookup-panel [data-testid="stVerticalBlock"] {
    border-radius: 22px !important;
    overflow: hidden !important;
}
.st-key-record-lookup-panel [data-testid="stExpander"] {
    border: 1px solid #C7D3E0 !important;
    border-radius: 22px !important;
    overflow: hidden !important;
}
[class*="st-key-record-metric-"] [data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border: 1px solid #000000 !important;
    border-radius: 12px !important;
    padding: 0.45rem 0.65rem !important;
}
[class*="st-key-record-metric-"] [data-testid="stVerticalBlockBorderWrapper"] > div,
[class*="st-key-record-metric-"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
    background-color: #FFFFFF !important;
    border-radius: 12px !important;
}
.st-key-recent-transaction-mix,
.st-key-recent-transaction-mix [data-testid="stVerticalBlock"] {
    background-color: #FFFFFF !important;
}
.st-key-recent-transaction-mix {
    border: 1px solid #C7D3E0 !important;
    border-radius: 18px !important;
    padding: 0.4rem;
    overflow: hidden;
}
.st-key-ingestion-processing-group {
    background-color: #FFF9F0 !important;
    border-radius: 20px !important;
    border: 1px solid #d8cdbd;
    padding: 0.5rem;
}
.st-key-ingestion-processing-group [data-testid="stVerticalBlockBorderWrapper"],
.st-key-ingestion-processing-group [data-testid="stVerticalBlockBorderWrapper"] > div,
.st-key-ingestion-processing-group [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
    background-color: transparent !important;
}
.st-key-storage-quality-group,
.st-key-analytics-fraud-group,
.st-key-serving-reliability-group {
    border-radius: 20px !important;
    border: 1px solid #b8cce8;
    padding: 0.5rem;
}
.st-key-ingestion-processing-group h3,
.st-key-storage-quality-group h3,
.st-key-analytics-fraud-group h3,
.st-key-serving-reliability-group h3 {
    margin: 0.15rem 0 0.5rem !important;
    padding: 0.35rem 0.6rem 0.65rem;
    border-bottom: 1px solid rgba(48, 44, 35, 0.18);
}
.st-key-storage-quality-group,
.st-key-storage-quality-group [data-testid="stVerticalBlockBorderWrapper"],
.st-key-storage-quality-group [data-testid="stVerticalBlockBorderWrapper"] > div,
.st-key-storage-quality-group [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"],
.st-key-serving-reliability-group,
.st-key-serving-reliability-group [data-testid="stVerticalBlockBorderWrapper"],
.st-key-serving-reliability-group [data-testid="stVerticalBlockBorderWrapper"] > div,
.st-key-serving-reliability-group [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
    background-color: #D0E3FF !important;
}
.st-key-analytics-fraud-group,
.st-key-analytics-fraud-group [data-testid="stVerticalBlockBorderWrapper"],
.st-key-analytics-fraud-group [data-testid="stVerticalBlockBorderWrapper"] > div,
.st-key-analytics-fraud-group [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
    background-color: #FFF9F0 !important;
}
[class*="st-key-track-metric-"],
[class*="st-key-track-metric-"] [data-testid="stVerticalBlockBorderWrapper"] {
    border: 1.5px solid #081F5C !important;
}
.st-key-quality-chart-panel {
    background-color: #FFFFFF !important;
    border: 1px solid #D8D2C3;
    border-radius: 18px;
    padding: 0.4rem;
    overflow: hidden;
}
.st-key-quality-chart-panel [data-testid="stVerticalBlock"] {
    background-color: transparent !important;
}
.st-key-confusion-chart-panel,
.st-key-rule-confusion-chart-panel,
.st-key-model-confusion-chart-panel {
    background-color: #FFFFFF !important;
    border: 1px solid #C7D3E0;
    border-radius: 18px;
    padding: 0.4rem;
    overflow: hidden;
}
.st-key-confusion-chart-panel [data-testid="stVerticalBlock"],
.st-key-rule-confusion-chart-panel [data-testid="stVerticalBlock"],
.st-key-model-confusion-chart-panel [data-testid="stVerticalBlock"] {
    background-color: transparent !important;
}
[data-testid="stVegaLiteChart"] {
    border-radius: 16px !important;
    overflow: hidden !important;
}
[data-testid="stVegaLiteChart"] iframe,
[data-testid="stVegaLiteChart"] canvas,
[data-testid="stVegaLiteChart"] svg {
    border-radius: 16px !important;
}
    </style>''',unsafe_allow_html=True)
    st.sidebar.markdown(
        '<div class="report-masthead">PAYSIM / BUSINESS INTELLIGENCE</div>',
        unsafe_allow_html=True,
    )
    _, logo_samsung, logo_aof, _ = st.columns([2, 1, 1, 2], vertical_alignment="center")
    with logo_samsung:
        st.image(str(ASSET_DIR / "logo_samsung.png"), width=135)
    with logo_aof:
        st.image(str(ASSET_DIR / "logo_aof.png"), width=90)
    st.markdown(
        f'<h1 class="page-title">{"Báo cáo kết quả xử lý và chất lượng phát hiện gian lận"}</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<p class="page-subtitle">{"Giao dịch và rủi ro"}</p>', unsafe_allow_html=True)
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
    st.caption(f"RUN {s.run_id}  /  {s.status.upper()}")
    left,right=st.columns([2,3])
    with left:
        with st.container(border=True,key="processing-card"):
            st.markdown("### Quy mô xử lý")
            st.metric("Spark đã xử lý",fmt_int(s.processed),delta=f"{fmt_int(s.lag)} đang chờ")
            st.caption(f"Nguồn đã phát {fmt_int(s.emitted)} giao dịch trong run này.")
    with right:
        with st.container(border=True,key="fraud-card"):
            st.markdown("### Cảnh báo gian lận")
            st.metric("Fraud alerts",fmt_int(s.alerts_count),delta=fmt_pct(s.model['Alert rate']))
            st.caption("Alert là kết quả dự đoán, không đồng nghĩa fraud thực tế.")
# AFTER END — 9B.2

# BEFORE Start — 9B.3
# So sánh model bằng bảng trên một trang riêng.
# BEFORE END — 9B.3
# AFTER Start — 9B.3: đối chiếu chất lượng bằng thanh ngang trên trang báo cáo chính.
def comparison(s):
    st.markdown("### Chất lượng phát hiện")
    rows=[]
    for key,name in [('rule','Spark SQL rule'),('model','Spark MLlib')]:
        values=detector_metrics(s.evaluation,key)
        rows.extend({'Chỉ số':metric,'Detector':name,'Giá trị':values[metric]} for metric in ['Precision','Recall','F1'])
    chart=alt.Chart(pd.DataFrame(rows)).mark_bar(
        size=13,stroke='#C6BFAF',strokeWidth=1
    ).encode(
        y=alt.Y('Chỉ số:N',sort=['Precision','Recall','F1'],title=None),x=alt.X('Giá trị:Q',scale=alt.Scale(domain=[0,1]),axis=alt.Axis(format='%'),title=None),
        yOffset='Detector:N',color=alt.Color(
            'Detector:N',
            scale=alt.Scale(
                domain=['Spark MLlib','Spark SQL rule'],
                range=['#FFF9F0','#7096D1'],
            ),
            legend=alt.Legend(orient='bottom',labelColor='#302c23',titleColor='#302c23'),
        ),
        tooltip=['Chỉ số','Detector',alt.Tooltip('Giá trị:Q',format='.2%')],
    ).properties(height=210)
    labels=alt.Chart(pd.DataFrame(rows)).mark_text(align='left',dx=4,color='#302c23').encode(
        y=alt.Y('Chỉ số:N',sort=['Precision','Recall','F1'],title=None),
        x=alt.X('Giá trị:Q',scale=alt.Scale(domain=[0,1])),
        yOffset='Detector:N',
        text=alt.Text('Giá trị:Q',format='.1%'),
    )
    quality_chart=(chart+labels).properties(background='transparent').configure_view(
        stroke=None,
    ).configure_axis(
        labelColor='#302c23',titleColor='#302c23',gridColor='#D8D2C3',
        domainColor='#9A9486',tickColor='#9A9486',
    )
    with st.container(key='quality-chart-panel'):
        st.altair_chart(quality_chart,use_container_width=True)
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
    st.markdown("### Cơ cấu giao dịch")
    if s.aggregates:
        transaction_df=pd.DataFrame(s.aggregates).copy()
        total_transactions=transaction_df['transactions'].sum()
        transaction_df['share']=transaction_df['transactions']/total_transactions if total_transactions else 0
        transaction_df['share_label']=transaction_df.apply(
            lambda row: f"{int(row['transactions']):,} ({row['share']:.1%})", axis=1
        )
        max_transactions=transaction_df['transactions'].max()
        transaction_axis=alt.X(
            'transactions:Q',
            scale=alt.Scale(domain=[0,max_transactions*1.2]),
            title='Số giao dịch',
        )
        chart=alt.Chart(transaction_df).mark_bar(
            cornerRadiusEnd=4,stroke='#A9B7C7',strokeWidth=0.6
        ).encode(
            y=alt.Y('type:N',sort='-x',title=None,axis=alt.Axis(labelOverlap=False)),
            x=transaction_axis,
            color=alt.Color(
                'type:N',
                scale=alt.Scale(
                    domain=['PAYMENT','CASH_IN','CASH_OUT','TRANSFER','DEBIT'],
                    range=['#D0E3FF','#BAD6EB','#7096D1','#F2F0DE','#D0E3FF'],
                ),
                legend=None,
            ),
            tooltip=[
                'type',
                alt.Tooltip('transactions:Q',title='Số giao dịch',format=','),
                alt.Tooltip('share:Q',title='Tỷ trọng',format='.1%'),
                alt.Tooltip('total_amount:Q',title='Tổng giá trị',format=',.2f'),
                alt.Tooltip('model_alerts:Q',title='Cảnh báo model',format=','),
                alt.Tooltip('rule_alerts:Q',title='Cảnh báo rule',format=','),
            ],
        ).properties(height=210)
        labels=alt.Chart(transaction_df).mark_text(
            align='left',dx=5,color='#302c23',fontSize=12
        ).encode(
            y=alt.Y('type:N',sort='-x',title=None),
            x=transaction_axis,
            text='share_label:N',
        )
        transaction_chart=(chart+labels).properties(background='#FFFFFF').configure_view(
            stroke=None,
        )
        st.altair_chart(transaction_chart,use_container_width=True)
# AFTER END — 9B.4

# BEFORE Start — 9B.5
# Biểu đồ vận hành và sơ đồ pipeline đứng trước phần nghiệp vụ.
# BEFORE END — 9B.5
# AFTER Start — 9B.5: báo cáo nghiệp vụ trước; chỉ số vận hành và phụ lục ở cuối.
def render(s,page):
    headline(s)
    with st.expander("Thông số vận hành"):
        a,b,c,d=st.columns(4)
        with a:
            with st.container(border=True):
                st.metric('Kafka lag',fmt_int(s.lag),help='Số giao dịch đã được phát nhưng Spark chưa xử lý.')
        with b:
            with st.container(border=True):
                st.metric('Ingest throughput',f"{fmt_float(s.latest_metric.get('ingest_throughput'))} ev/s")
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
# AFTER END — 9B.5
