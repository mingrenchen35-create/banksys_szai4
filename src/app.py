"""Bank Marketing Subscription Analysis & Prediction System."""

import streamlit as st

st.set_page_config(
    page_title="银行营销认购分析系统",
    page_icon=":bank:",
    layout="wide",
)

st.title("银行营销认购分析系统")
st.markdown("""
欢迎使用银行营销数据分析与预测系统。

- **数据分析**: 在左侧导航选择「1_analysis」,探索客户数据分布与特征关系。
- **在线预测**: 在左侧导航选择「2_prediction」,输入客户特征预测认购结果。
""")
