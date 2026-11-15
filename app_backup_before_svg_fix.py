
import streamlit as st
import pandas as pd
import base64
from pathlib import Path
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

/* ==========================================
   FLAME DNA - NAVIGATION EFFECTS
   ========================================== */

/* Sidebar navigation items */
section[data-testid="stSidebar"]
div[role="radiogroup"] label {

    border-radius: 12px;
    padding: 11px 13px;
    margin-bottom: 6px;

    border: 1px solid transparent;
    background: transparent;

    transition:
        background-color 0.25s ease,
        border-color 0.25s ease,
        box-shadow 0.25s ease;
}

/* Hover effect */
section[data-testid="stSidebar"]
div[role="radiogroup"] label:hover {

    background-color: #26201B;
    border-color: #A96B35;

    box-shadow:
        0 3px 14px rgba(243, 107, 8, 0.12);
}

/* Active navigation item */
section[data-testid="stSidebar"]
div[role="radiogroup"] label:has(input:checked) {

    background-color: #302015;
    border-color: #F36B08;

    box-shadow:
        inset 3px 0 0 #F36B08,
        0 3px 15px rgba(243, 107, 8, 0.10);
}

/* Navigation text */
section[data-testid="stSidebar"]
div[role="radiogroup"] label p {

    font-weight: 500;
    color: #F5F5F5;

    transition: color 0.25s ease;
}

/* Active navigation text */
section[data-testid="stSidebar"]
div[role="radiogroup"] label:has(input:checked) p {

    color: #F36B08;
    font-weight: 600;
}

/* ==========================================
   KPI CARD EFFECTS
   ========================================== */

div[data-testid="stMetric"] {

    transition:
        border-color 0.25s ease,
        box-shadow 0.25s ease;
}

div[data-testid="stMetric"]:hover {

    border-color: #F36B08;

    box-shadow:
        0 6px 22px rgba(243, 107, 8, 0.15);
}

/* ==========================================
   BUTTON EFFECTS
   ========================================== */

div.stButton > button,
div.stDownloadButton > button {

    border-radius: 10px;
    border: 1px solid #A96B35;

    transition:
        border-color 0.25s ease,
        background-color 0.25s ease,
        box-shadow 0.25s ease;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {

    border-color: #F36B08;
    background-color: #302015;

    box-shadow:
        0 4px 16px rgba(243, 107, 8, 0.18);
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# SVG NAVIGATION ICONS
# =====================================================

ICON_DIR = Path(__file__).resolve().parent / "assets" / "icons"


def load_svg_icon(filename):
    """Load a local SVG icon as a CSS data URI."""
    path = ICON_DIR / filename

    if not path.is_file():
        return ""

    svg_data = path.read_bytes()

    encoded = base64.b64encode(svg_data).decode("ascii")

    return f"data:image/svg+xml;base64,{encoded}"


NAV_ICON_FILES = {
    "Overview": "overview.svg",
    "Real-Time Monitoring": "monitoring.svg",
    "NASA Research Catalog": "nasa-catalog.svg",
    "Data Explorer": "data-explorer.svg",
    "Scientific Analysis & Comparison": "analysis.svg",
    "Space Mission Fire Safety": "fire-safety.svg",
    "AI Assistant": "ai-assistant.svg",
    "Data Quality & Provenance": "data-quality.svg",
}

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


NAV_ICONS = {
    "Overview": "📊",
    "Real-Time Monitoring": "📡",
    "NASA Research Catalog": "🛰",
    "Data Explorer": "🔎",
    "Scientific Analysis & Comparison": "📈",
    "Space Mission Fire Safety": "🛡",
    "AI Assistant": "✦",
    "Data Quality & Provenance": "▣",
}

page = st.sidebar.radio(
    "Navigation",
    PAGES,
)


# =====================================================
# ORANGE SVG ICONS IN SIDEBAR
# =====================================================


# =====================================================
# ORANGE SVG NAVIGATION ICONS
# =====================================================

icon_rules = []

for index, name in enumerate(PAGES, start=1):
    icon_url = load_svg_icon(NAV_ICON_FILES[name])

    if icon_url:
        icon_rules.append(f"""
        section[data-testid="stSidebar"]
        div[role="radiogroup"] > label:nth-of-type({index})
        {{
            position: relative;
            padding-left: 44px !important;
        }}

        section[data-testid="stSidebar"]
        div[role="radiogroup"] > label:nth-of-type({index})::before
        {{
            content: "";
            position: absolute;
            left: 13px;
            top: 50%;
            transform: translateY(-50%);
            width: 20px;
            height: 20px;
            background-image: url("{icon_url}");
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
            pointer-events: none;
        }}
        """)

st.markdown(
    "<style>" + "\n".join(icon_rules) + """
    section[data-testid="stSidebar"]
    div[role="radiogroup"] label
    div[data-testid="stMarkdownContainer"] p::before {
        content: none !important;
        background-image: none !important;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label
    div[data-testid="stMarkdownContainer"] p {
        margin: 0 !important;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label
    div[data-testid="stMarkdownContainer"] {
        position: relative;
        z-index: 1;
    }

    section[data-testid="stSidebar"]
div[role="radiogroup"] label
[data-testid="stRadio"] {
    display: none;
}

section[data-testid="stSidebar"]
div[role="radiogroup"] label
input[type="radio"] {
    position: absolute;
    opacity: 0;
}
    </style>""",
    unsafe_allow_html=True,
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
