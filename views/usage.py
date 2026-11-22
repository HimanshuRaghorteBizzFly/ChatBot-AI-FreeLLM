"""
Usage & Limits View.
Real-time API token analytics, request metrics, estimated cost tracking, and CSV export.
"""
import streamlit as st
from components.navbar import render_navbar
from backend.repositories.storage import get_usage_summary
from backend.services.usage import export_csv

def render():
    render_navbar("📈 Usage & Analytics", "Real-time Token Consumption, Request Volume & Cost Auditing")

    summary = get_usage_summary()

    # Metric Cards
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Requests</div>
                <div class="metric-value" style="color: #2563EB;">{summary.get('total_requests', 0):,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Tokens Processed</div>
                <div class="metric-value" style="color: #7C3AED;">{summary.get('total_tokens', 0):,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Estimated Cost</div>
                <div class="metric-value" style="color: #059669;">${summary.get('total_cost', 0.0):.4f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Provider Breakdown
    st.markdown("### 📊 Requests by Provider")
    by_provider = summary.get("by_provider", {})
    if by_provider:
        p_cols = st.columns(len(by_provider))
        for idx, (prov, count) in enumerate(by_provider.items()):
            with p_cols[idx]:
                st.metric(prov, f"{count} calls")
    else:
        st.caption("No provider requests recorded yet.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # Activity Log Table
    st.markdown("### 📝 Recent API Operations Log")
    recent = summary.get("recent", [])
    if recent:
        st.dataframe(recent, use_container_width=True)
        csv_data = export_csv()
        st.download_button(
            "📥 Export Usage Audit (.csv)",
            data=csv_data,
            file_name="ai_studio_usage_log.csv",
            mime="text/csv",
            key="dl_usage_csv"
        )
    else:
        st.info("No activity records found. Use the Chat, Vision, or Image studios to start recording usage.")
