"""Online prediction page: input customer features and get subscription prediction."""

import streamlit as st

from src.model import (
    PREDICTION_CATEGORICAL,
    PREDICTION_NUMERIC,
    load_model,
    predict,
    save_model,
    train_model,
)
from src.utils import has_trained_model

st.set_page_config(page_title="在线预测", page_icon=":crystal_ball:", layout="wide")

st.title("在线预测系统")
st.markdown("输入客户特征,预测其是否会认购定期存款。")


def render_training_section():
    st.warning("模型尚未训练,请先训练模型。")
    if st.button("开始训练模型", type="primary"):
        with st.spinner("正在训练模型,请稍候..."):
            pipeline, metrics = train_model()
            save_model(pipeline)
            st.session_state["model_trained"] = True
            st.session_state["metrics"] = metrics
        st.success("模型训练完成!")
        st.rerun()


def render_metrics(metrics: dict):
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("AUC", f"{metrics['auc']:.4f}")
    col2.metric("准确率", f"{metrics['accuracy']:.4f}")
    col3.metric("精确率", f"{metrics['precision']:.4f}")
    col4.metric("召回率", f"{metrics['recall']:.4f}")
    col5.metric("F1", f"{metrics['f1']:.4f}")


NUMERIC_SLIDER_CONFIG = {
    "age": {"min": 16, "max": 101, "default": 38, "step": 1, "label": "年龄"},
    "campaign": {"min": 0, "max": 57, "default": 1, "step": 1, "label": "营销次数"},
    "pdays": {"min": 0, "max": 1048, "default": 999, "step": 1, "label": "距上次联系天数"},
    "previous": {"min": 0, "max": 6, "default": 0, "step": 1, "label": "之前联系次数"},
    "emp_var_rate": {"min": -3.4, "max": 1.4, "default": 0.0, "step": 0.1, "label": "就业变化率"},
    "cons_price_index": {
        "min": 87.64,
        "max": 99.46,
        "default": 93.5,
        "step": 0.01,
        "label": "消费者物价指数",
    },
    "cons_conf_index": {
        "min": -53.28,
        "max": -25.55,
        "default": -40.0,
        "step": 0.01,
        "label": "消费者信心指数",
    },
    "lending_rate3m": {
        "min": 0.6,
        "max": 5.27,
        "default": 3.9,
        "step": 0.01,
        "label": "3个月贷款利率",
    },
    "nr_employed": {"min": 4715, "max": 5490, "default": 5134, "step": 1, "label": "就业人数"},
}


def render_prediction_form():
    st.subheader("客户特征输入")

    input_data = {}
    col1, col2, col3 = st.columns(3)

    for i, feat in enumerate(PREDICTION_NUMERIC):
        col = [col1, col2, col3][i % 3]
        cfg = NUMERIC_SLIDER_CONFIG.get(feat, {})
        input_data[feat] = col.slider(
            cfg.get("label", feat),
            min_value=cfg.get("min", 0.0),
            max_value=cfg.get("max", 100.0),
            value=cfg.get("default", 0.0),
            step=cfg.get("step", 1.0),
            key=f"num_{feat}",
        )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    for i, feat in enumerate(PREDICTION_CATEGORICAL):
        col = [col1, col2, col3][i % 3]
        input_data[feat] = col.selectbox(
            f"{feat}",
            [
                "admin.",
                "blue-collar",
                "entrepreneur",
                "housemaid",
                "management",
                "retired",
                "self-employed",
                "services",
                "student",
                "technician",
                "unemployed",
                "unknown",
            ]
            if feat == "job"
            else ["divorced", "married", "single", "unknown"]
            if feat == "marital"
            else [
                "basic.4y",
                "basic.6y",
                "basic.9y",
                "high.school",
                "illiterate",
                "professional.course",
                "university.degree",
                "unknown",
            ]
            if feat == "education"
            else ["no", "yes", "unknown"]
            if feat in ("default", "housing", "loan")
            else ["cellular", "telephone"]
            if feat == "contact"
            else [
                "jan",
                "feb",
                "mar",
                "apr",
                "may",
                "jun",
                "jul",
                "aug",
                "sep",
                "oct",
                "nov",
                "dec",
            ]
            if feat == "month"
            else ["mon", "tue", "wed", "thu", "fri"]
            if feat == "day_of_week"
            else ["failure", "nonexistent", "success"]
            if feat == "poutcome"
            else ["unknown"],
            key=f"cat_{feat}",
        )

    return input_data


# ── Main page logic ──────────────────────────────────────────────────
if "model_trained" not in st.session_state:
    st.session_state["model_trained"] = has_trained_model()

if not st.session_state["model_trained"]:
    render_training_section()
else:
    try:
        pipeline = load_model()
    except FileNotFoundError:
        st.session_state["model_trained"] = False
        render_training_section()
        st.stop()

    if "metrics" in st.session_state:
        render_metrics(st.session_state["metrics"])

    input_data = render_prediction_form()

    if st.button("预测", type="primary", key="predict_btn"):
        missing = [k for k, v in input_data.items() if v is None]
        if missing:
            st.error(f"以下字段不能为空: {', '.join(missing)}")
        else:
            with st.spinner("预测中..."):
                result = predict(pipeline, input_data)
            if result["prediction"] == 1:
                st.success(f"预测结果: {result['label']} (概率: {result['probability']:.2%})")
            else:
                st.info(f"预测结果: {result['label']} (概率: {result['probability']:.2%})")
