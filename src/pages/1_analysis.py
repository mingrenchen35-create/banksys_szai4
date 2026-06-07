"""Data analysis page: interactive EDA for bank marketing data."""

import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import (
    CATEGORICAL_COLS,
    NUMERIC_COLS,
    TARGET_COL,
    get_feature_stats,
    get_feature_types,
    get_summary,
    load_train,
)

st.set_page_config(page_title="数据分析", page_icon=":bar_chart:", layout="wide")

st.title("银行营销数据分析")
st.markdown("交互式探索训练数据中各特征与认购结果的关系。")


@st.cache_data
def load_data():
    return load_train()


df = load_data()
summary = get_summary(df)
feature_types = get_feature_types()

# ── Sidebar ──────────────────────────────────────────────────────────
st.sidebar.header("数据概览")
st.sidebar.metric("样本数", f"{summary['n_rows']:,}")
st.sidebar.metric("特征数", summary["n_cols"])
st.sidebar.metric("缺失值列数", sum(1 for v in summary["missing_pct"].values() if v > 0))

# ── Tabs ─────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["数据集预览", "数值特征分布", "分类特征分布", "散点图分析", "缺失值分析"]
)

with tab1:
    st.subheader("数据集预览")
    st.dataframe(df.head(100), use_container_width=True)

    st.subheader("目标变量分布 (subscribe)")
    col1, col2 = st.columns(2)
    with col1:
        target_counts = df[TARGET_COL].value_counts().reset_index()
        target_counts.columns = ["subscribe", "count"]
        fig = px.bar(target_counts, x="subscribe", y="count", text="count", color="subscribe")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.dataframe(
            pd.DataFrame(
                {
                    "类别": target_counts["subscribe"].tolist(),
                    "数量": target_counts["count"].tolist(),
                    "占比": (target_counts["count"] / len(df) * 100).round(2).tolist(),
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

with tab2:
    st.subheader("数值特征分布")
    numeric_feat = st.selectbox("选择数值特征", NUMERIC_COLS, key="num_dist")
    col1, col2 = st.columns(2)
    stats = get_feature_stats(df, numeric_feat)
    with col1:
        fig = px.histogram(
            df, x=numeric_feat, color=TARGET_COL, nbins=50, marginal="box", opacity=0.7
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.box(df, y=numeric_feat, x=TARGET_COL, color=TARGET_COL)
        st.plotly_chart(fig, use_container_width=True)
    st.caption(
        f"均值={stats['mean']:.2f} | 中位数={stats['median']:.2f} "
        f"| 标准差={stats['std']:.2f} | min={stats['min']:.2f} | max={stats['max']:.2f}"
    )

with tab3:
    st.subheader("分类特征分布")
    cat_feat = st.selectbox("选择分类特征", CATEGORICAL_COLS, key="cat_dist")
    stats = get_feature_stats(df, cat_feat)
    crosstab_df = pd.DataFrame(stats["crosstab"]).T
    crosstab_df.index.name = cat_feat
    crosstab_df = crosstab_df.reset_index()
    fig = px.bar(
        crosstab_df,
        x=cat_feat,
        y=crosstab_df.columns[1:].tolist(),
        barmode="group",
        title=f"{cat_feat} 按 subscribe 分组",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("散点图分析")
    col1, col2 = st.columns(2)
    with col1:
        x_feat = st.selectbox("X 轴特征", NUMERIC_COLS, key="scatter_x")
    with col2:
        y_feat = st.selectbox(
            "Y 轴特征",
            NUMERIC_COLS,
            index=min(3, len(NUMERIC_COLS) - 1),
            key="scatter_y",
        )
    sample_size = st.slider(
        "采样数量(大数据量时建议采样)", 500, len(df), min(5000, len(df)), step=500
    )
    df_sample = df.sample(n=sample_size, random_state=42) if sample_size < len(df) else df
    fig = px.scatter(
        df_sample,
        x=x_feat,
        y=y_feat,
        color=TARGET_COL,
        opacity=0.6,
        marginal_x="histogram",
        marginal_y="histogram",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("相关性矩阵")
    corr = df[NUMERIC_COLS].corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
    )
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.subheader("缺失值分析")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame(
        {
            "特征": missing.index,
            "缺失数": missing.values,
            "缺失率(%)": missing_pct.values,
        }
    )
    missing_df = missing_df[missing_df["缺失数"] > 0].sort_values("缺失数", ascending=False)

    if missing_df.empty:
        st.success("数据集无缺失值。")
    else:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(missing_df, x="特征", y="缺失率(%)", text="缺失率(%)")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.dataframe(missing_df, use_container_width=True, hide_index=True)

    st.subheader("缺失值热力图")
    if missing_df.empty:
        st.info("无缺失值,无法生成热力图。")
    else:
        missing_mask = df.isnull()
        sample_cols = missing_df["特征"].tolist()
        fig = px.imshow(
            missing_mask[sample_cols].iloc[:200].T,
            aspect="auto",
            labels=dict(x="样本索引", y="特征", color="缺失"),
            title="前200行缺失值分布",
        )
        st.plotly_chart(fig, use_container_width=True)
