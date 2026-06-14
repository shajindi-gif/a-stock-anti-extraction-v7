"""Streamlit 数据看板 — v8 决策 / 执行 / 东财条件单可视化。"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st

from data.demo_scenarios import get_scenario, list_scenarios
from data.portfolio_state import get_portfolio
from engine_v8 import run_all_scenarios_v8, run_v8_pipeline

st.set_page_config(
    page_title="A股反收割 v8 数据看板",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 1.5rem; }
    div[data-testid="stMetricValue"] { font-size: 1.6rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_all() -> pd.DataFrame:
    return pd.DataFrame(run_all_scenarios_v8())


def render_probability_chart(prob: dict[str, float]) -> None:
    df = pd.DataFrame({
        "方向": ["上涨", "震荡", "下跌"],
        "概率": [prob["up"], prob["side"], prob["down"]],
    })
    st.bar_chart(df.set_index("方向"), color="#58a6ff", height=220)


def main() -> None:
    st.title("🚀 A股反收割系统 v8 · 数据看板")
    st.caption("AI 决策 + 执行闭环 + 东方财富条件单 · Demo 数据")

    with st.sidebar:
        st.header("⚙️ 控制面板")
        scenario = st.selectbox(
            "Demo 场景",
            list_scenarios(),
            format_func=lambda k: {
                "bullish_kcb50": "科创50ETF · 多头",
                "sideways_hs300": "沪深300ETF · 震荡",
                "bear_trap_detected": "创业板ETF · 诱多",
                "liquidity_crisis": "科创50ETF · 流动性危机",
            }.get(k, k),
        )
        portfolio = get_portfolio()
        pv = st.number_input("组合总值（元）", value=float(portfolio["total_value"]), step=10000.0)
        st.divider()
        st.markdown("**新手？** [QUICKSTART.md](https://github.com/shajindi-gif/a-stock-anti-extraction-v7/blob/main/QUICKSTART.md)")
        st.markdown("**在线 Web：** [网页版](https://shajindi-gif.github.io/a-stock-anti-extraction-v7/)")
        st.warning("⚠️ 演示工具，不构成投资建议")

    result = run_v8_pipeline(get_scenario(scenario), portfolio_value=pv)
    v7 = result.v7

    # ── 指标行 ──
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("标的", f"{v7.symbol}")
    c2.metric("当前价", f"{v7.price:.3f}")
    c3.metric("AI 决策", v7.decision)
    c4.metric("目标仓位", f"{v7.position:.0%}")
    c5.metric("条件单", f"{len(result.conditional_orders)} 条")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 决策概览", "🔄 执行闭环", "📱 东财条件单", "📈 全场景对比"])

    with tab1:
        col_l, col_r = st.columns([1, 1])
        with col_l:
            st.subheader("概率预测")
            render_probability_chart(v7.probability)
            st.markdown(f"**信号**：`{v7.signal}` · **市场状态**：{v7.regime_label}")
        with col_r:
            st.subheader("结构判断")
            for note in v7.structure_notes:
                st.info(note)
            st.subheader("风控")
            st.write(f"动态止损：**-{v7.stop_pct}%** · 状态：**{v7.stop_action}**")

    with tab2:
        st.subheader("订单路由")
        st.json(result.order_route)
        st.subheader("仓位重平衡")
        rb = result.rebalance
        rc1, rc2, rc3 = st.columns(3)
        rc1.metric("当前仓位", f"{rb['current_pct']:.0%}")
        rc2.metric("目标仓位", f"{rb['target_pct']:.0%}")
        rc3.metric("调仓份数", f"{rb['shares']} 份")
        st.subheader("自动止损计划")
        st.json(result.stop_plan)

    with tab3:
        st.subheader("东方财富条件单建议")
        if not result.conditional_orders:
            st.success("当前无需设置条件单")
        for i, order in enumerate(result.conditional_orders, 1):
            with st.expander(f"【{i}】{order['type']} · 优先级 {order['priority']}", expanded=i == 1):
                st.markdown(f"**操作路径**：{order['app_path']}")
                oc1, oc2, oc3 = st.columns(3)
                oc1.write(f"触发价：**{order['trigger_price']}**")
                oc2.write(f"委托价：**{order['order_price']}**")
                oc3.write(f"数量：**{order['quantity']}**")
                st.write(f"理由：{order['reason']}")
        st.code(result.eastmoney_guide, language=None)

    with tab4:
        st.subheader("全场景对比看板")
        df = load_all()
        st.dataframe(df, use_container_width=True, hide_index=True)

        chart_df = df.set_index("symbol")[["prob_up", "prob_side", "prob_down"]]
        st.bar_chart(chart_df, height=300)

        st.subheader("决策分布")
        st.bar_chart(df["decision"].value_counts(), height=200)

    st.divider()
    with st.expander("📋 完整 v8 报告"):
        st.code(result.to_report(), language=None)


if __name__ == "__main__":
    main()
