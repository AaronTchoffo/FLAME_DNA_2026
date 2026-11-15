
import streamlit as st
import pandas as pd

from modules.event_history import (
    create_event_history,
    record_event,
    get_event_statistics,
    export_event_history,
)
from modules.simulator import generate_sensor_data
from modules.alerts import analyze_fire_risk
from modules.anomaly_detection import (
    train_anomaly_model,
    detect_anomaly,
)


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="FLAME DNA | FLAMENOVA TECH",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_resource
def load_ai_model():
    return train_anomaly_model()

# =====================================================
# DESIGN
# =====================================================

st.markdown("""
<style>
.stApp {
    background-color: #101010;
    color: #F5F5F5;
}

[data-testid="stSidebar"] {
    background-color: #181818;
}

h1, h2, h3 {
    color: #F36B08 !important;
}

div[data-testid="stMetric"] {
    background: #1C1C1C;
    border: 1px solid #A96B35;
    border-radius: 12px;
    padding: 16px;
}

div[data-testid="stMetricValue"] {
    color: #F36B08 !important;
}

div[data-testid="stMetricLabel"] {
    color: #D9A441 !important;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# NAVIGATION
# =====================================================

PAGES = [
    "Overview",
    "Real-Time Monitoring",
    "NASA Research Catalog",
    "Data Explorer",
    "Scientific Analysis & Comparison",
    "Space Mission Fire Safety",
    "AI Assistant",
    "Data Quality & Provenance",
]

st.sidebar.title("🔥 FLAME DNA")
st.sidebar.caption("FLAMENOVA TECH")

page = st.sidebar.radio(
    "Navigation",
    PAGES,
)


# =====================================================
# HEADER
# =====================================================

st.title("🔥 FLAME DNA")
st.caption(
    "Understanding Fire. Predicting Risks. Protecting Lives."
)


# =====================================================
# OVERVIEW
# =====================================================

if page == "Overview":

    st.subheader(
        "Intelligent Fire Safety Dashboard"
    )

    st.write(
        "FLAME DNA combines NASA microgravity "
        "combustion research with a simulated "
        "fire monitoring and early-warning system."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "NASA Studies Integrated",
        "0"
    )

    c2.metric(
        "Simulated Sensors",
        "4"
    )

    c3.metric(
        "Active Alerts",
        "0"
    )

    st.info(
        "NASA research datasets and advanced "
        "AI features will be integrated progressively."
    )


# =====================================================
# REAL-TIME MONITORING
# =====================================================

elif page == "Real-Time Monitoring":

    st.subheader(
        "Intelligent Fire Monitoring System"
    )

    st.caption(
        "Demonstration prototype using simulated "
        "sensor data. Not connected to physical sensors."
    )

    scenario = st.selectbox(
        "Select Monitoring Scenario",
        ["normal", "anomaly", "fire"],
        format_func=lambda x: {
            "normal": "Normal Conditions",
            "anomaly": "Sensor Anomaly",
            "fire": "Simulated Fire",
        }[x],
    )

    if (
        "sensor_history" not in st.session_state
        or st.session_state.get("last_scenario") != scenario
    ):
        st.session_state.sensor_history = []
        st.session_state.last_scenario = scenario
    if "event_history" not in st.session_state:
        st.session_state.event_history = create_event_history()
    
    @st.fragment(run_every="2s")
    def live_monitoring():

        # Generate simulated sensor readings
        data = generate_sensor_data(scenario)

        # Analyze risk using predefined rules
        risk = analyze_fire_risk(data)

        # Analyze readings using AI
        model, scaler = load_ai_model()

        ai_result = detect_anomaly(
            data,
            model,
            scaler,
        )

        st.session_state.event_history = record_event(
            st.session_state.event_history,
            data,
            risk,
            ai_result,
        )
        # Update sensor history
        st.session_state.sensor_history.append(data)

        st.session_state.sensor_history = (
            st.session_state.sensor_history[-100:]
        )

        # AI anomaly detection panel
        st.markdown("### AI Anomaly Detection")

        ai_col1, ai_col2 = st.columns(2)

        with ai_col1:
            if ai_result["is_anomaly"]:
                st.error(
                    "AI Status: ANOMALY DETECTED"
                )
            else:
                st.success(
                    "AI Status: NORMAL PATTERN"
                )

        with ai_col2:
            st.metric(
                "AI Anomaly Score",
                f"{ai_result['anomaly_score']:.4f}",
            )

        st.caption(
            "AI model: Isolation Forest | "
            "Trained on synthetic baseline data. "
            "An anomaly is not a confirmed fire."
        )

        # Existing monitoring section

        st.markdown("### Monitoring Status")

        if risk["status"] == "NORMAL":
            st.success(
                "🟢 Normal Conditions — No anomaly detected."
            )

        elif risk["status"] == "ANOMALIE":
            st.warning(
                "🟠 Warning — Unusual sensor readings detected."
            )

        else:
            st.error(
                "🔴 Simulated Fire Alert — Immediate review required."
            )

        detail_translations = {
            "Température simulée très élevée":
                "Very high simulated temperature",
            "Température simulée inhabituelle":
                "Unusual simulated temperature",
            "Indice de fumée simulée élevé":
                "High simulated smoke index",
            "Présence de fumée simulée":
                "Simulated smoke detected",
            "Concentration en oxygène inhabituelle":
                "Unusual oxygen concentration",
            "Ventilation simulée faible":
                "Low simulated airflow",
        }

        for detail in risk["details"]:
            st.write(
                "• " + detail_translations.get(
                    detail,
                    "Unclassified sensor warning"
                )
            )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Temperature",
            f"{data['temperature']:.1f} °C"
        )

        c2.metric(
            "Smoke Index",
            f"{data['smoke']:.3f}"
        )

        c3.metric(
            "Oxygen Level",
            f"{data['oxygen']:.1f} %"
        )

        c4.metric(
            "Airflow",
            f"{data['airflow']:.2f} m/s"
        )

        history = pd.DataFrame(
            st.session_state.sensor_history
        )

        st.markdown(
            "### Live Sensor Trends"
        )

        if len(history) >= 2:

            history["sample"] = range(
                len(history)
            )

            st.plotly_chart(
                {
                    "data": [
                        {
                            "x": history["sample"].tolist(),
                            "y": history["temperature"].tolist(),
                            "type": "scatter",
                            "mode": "lines+markers",
                            "name": "Temperature (°C)",
                            "line": {
                                "color": "#F36B08"
                            },
                        }
                    ],
                    "layout": {
                        "paper_bgcolor": "#101010",
                        "plot_bgcolor": "#101010",
                        "font": {
                            "color": "#F5F5F5"
                        },
                        "xaxis": {
                            "title": "Sample"
                        },
                        "yaxis": {
                            "title": "Temperature (°C)"
                        },
                    },
                },
                width="stretch",
                key="temperature_chart",
            )

            st.line_chart(
                history.set_index("sample")[
                    ["smoke", "oxygen", "airflow"]
                ].rename(
                    columns={
                        "smoke": "Smoke Index",
                        "oxygen": "Oxygen (%)",
                        "airflow": "Airflow (m/s)",
                    }
                ),
                height=250,
            )



        # ==========================================
        # EVENT HISTORY
        # ==========================================

        st.markdown("### Event History")

        history_events = st.session_state.event_history

        stats = get_event_statistics(history_events)

        e1, e2, e3, e4 = st.columns(4)

        e1.metric(
            "Total Events",
            stats["total_events"],
        )

        e2.metric(
            "AI Anomalies",
            stats["ai_anomalies"],
        )

        e3.metric(
            "Sensor Alerts",
            stats["sensor_alerts"],
        )

        e4.metric(
            "Critical Alerts",
            stats["critical_alerts"],
        )

        if not history_events.empty:

            st.dataframe(
                history_events.iloc[::-1],
                width="stretch",
                hide_index=True,
            )

            st.download_button(
                label="Download Event History (CSV)",
                data=export_event_history(history_events),
                file_name="flame_dna_event_history.csv",
                mime="text/csv",
                key="download_event_history",
            )

        else:
            st.info(
                "No anomalies or alerts recorded yet."
            )

        st.caption(
            "All events are generated from simulated "
            "sensor readings for demonstration purposes."
        )

        st.caption(
            "Last simulated reading: "
            + data["timestamp"]
        )


    live_monitoring()


# =====================================================
# OTHER MODULES
# =====================================================

else:

    st.subheader(page)

    st.info(
        "This module is currently under development."
    )
