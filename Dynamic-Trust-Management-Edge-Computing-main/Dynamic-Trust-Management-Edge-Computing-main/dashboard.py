import streamlit as st
import redis
import json
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# =====================================================
# AUTO REFRESH
# =====================================================

st_autorefresh(interval=3000, key="refresh")

# =====================================================
# REDIS CONNECTION
# =====================================================

r = redis.Redis(
    host="localhost",
    port=6380,
    decode_responses=True
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Alvarium Trust Dashboard",
    layout="wide"
)

st.title("🚀 AI-Driven Multidimensional Trust Dashboard")
nodes = [f"edge-{i}" for i in range(10)]
selected_node = st.selectbox(
    "Select Edge Node",
    nodes
)

# =====================================================
# EDGE NODES
# =====================================================



all_data = []

# =====================================================
# TRUST COMPUTATION
# =====================================================

def calculate_trust(
    latency,
    cpu,
    memory,
    availability,
    success_rate,
    uptime
):

    # ---------------------------
    # NORMALIZATION
    # ---------------------------

    latency = min(max(latency / 1000, 0), 1)

    cpu = min(max(cpu, 0), 1)
    memory = min(max(memory, 0), 1)

    availability = min(max(availability, 0), 1)
    success_rate = min(max(success_rate, 0), 1)
    uptime = min(max(uptime, 0), 1)

    # ---------------------------
    # OPERATIONAL TRUST
    # ---------------------------

    T_operational = (
        0.4 * success_rate +
        0.3 * availability +
        0.3 * uptime
    )

    # ---------------------------
    # RESOURCE TRUST
    # ---------------------------

    T_resource = (
        0.5 * (1 - cpu) +
        0.5 * (1 - memory)
    )

    # ---------------------------
    # NETWORK TRUST
    # ---------------------------

    T_network = 1 - latency

    # ---------------------------
    # DATA TRUST
    # ---------------------------

    T_data = success_rate

    # ---------------------------
    # HISTORICAL TRUST
    # ---------------------------

    T_historical = (
        T_operational +
        T_resource +
        T_network +
        T_data
    ) / 4

    # ---------------------------
    # FINAL RULE TRUST
    # ---------------------------

    T_rule = (
        0.30 * T_operational +
        0.25 * T_resource +
        0.20 * T_network +
        0.15 * T_data +
        0.10 * T_historical
    )

    T_rule = max(0, min(T_rule, 1))

    return round(T_rule, 3)

# =====================================================
# TRUST CATEGORY
# =====================================================

def trust_label(score):

    if 0.90 <= score <= 1.00:
        return "🟢 Highly Trusted"

    elif 0.75 <= score < 0.90:
        return "🟡 Reliable"

    elif 0.50 <= score < 0.75:
        return "🟠 Moderate"

    else:
        return "🔴 Untrusted"

# =====================================================
# FETCH DATA
# =====================================================

for node in nodes:

    raw = r.lrange(f"annotation:{node}", 0, 9)

    for item in raw:

        try:

            x = json.loads(item)

            a = x["annotations"]

            latency = float(a["latency"])
            cpu = float(a["cpu"])
            memory = float(a["memory"])
            availability = float(a["availability"])
            success_rate = float(a["success_rate"])
            uptime = float(a["uptime"])

            trust_score = calculate_trust(
                latency,
                cpu,
                memory,
                availability,
                success_rate,
                uptime
            )

            status = trust_label(trust_score)


            

            raw_timestamp = x.get("timestamp", 0)

            timestamp = datetime.fromtimestamp(
               raw_timestamp
            ).strftime("%H:%M:%S")

            all_data.append({

              "Node": node,
              "Timestamp": timestamp,

              "Latency": latency,
              "CPU": round(cpu, 3),
              "Memory": round(memory, 3),
              "Availability": round(availability, 3),
              "Success Rate": round(success_rate, 3),
              "Uptime": round(uptime, 3),

              "Trust Score": trust_score,
              "Status": status

            })
        except:
            pass

# =====================================================
# DATAFRAME
# =====================================================

df = pd.DataFrame(all_data)

# =====================================================
# DASHBOARD
# =====================================================

if len(df) == 0:

    st.warning("No telemetry data received yet...")

else:

    st.subheader(
        f"📊 Metrics for {selected_node}"
    )

    subset = (
        df[df["Node"] == selected_node]
        .head(10)
        .iloc[::-1]
    )

    if len(subset) > 0:

        latest_df = pd.DataFrame(
            [subset.iloc[-1]]
        )

        st.dataframe(
            latest_df,
            use_container_width=True
        )

    else:

        st.warning(
            f"No data available for {selected_node}"
        )

    # =================================================
    # TRUST GRAPH
    # =================================================

    st.subheader("🛡 Trust Score Over Time")

    fig0, ax0 = plt.subplots(figsize=(12, 5))

    subset = (
        df[df["Node"] == selected_node]
        .head(10)
        .iloc[::-1]
    )

    if len(subset) > 0:

        ax0.plot(
            subset["Timestamp"],
            subset["Trust Score"],
            marker="o",
            linewidth=3,
            label=selected_node
        )

    ax0.set_ylabel("Trust Score")
    ax0.set_xlabel("Timestamp")

    ax0.tick_params(
        axis="x",
        rotation=45
    )

    ax0.set_ylim([0, 1])

    ax0.legend()

    plt.tight_layout()

    st.pyplot(fig0)
    # =================================================
    # LATENCY
    # =================================================

    st.subheader("⚡ Latency")

    fig1, ax1 = plt.subplots(figsize=(10, 4))

    subset = (
      df[df["Node"] == selected_node]
      .head(10)
      .iloc[::-1]
    )

    if len(subset) > 0:

      ax1.plot(
        subset["Timestamp"],
        subset["Latency"],
        marker="o",
        linewidth=3,
        label=selected_node
      )

    ax1.set_ylabel("Latency (ms)")
    ax1.set_xlabel("TimeStamp")

    ax1.legend()
    
    ax1.tick_params(axis="x", rotation=45)
    st.pyplot(fig1)

    # =================================================
    # CPU
    # =================================================

    st.subheader("🖥 CPU Usage")

    fig2, ax2 = plt.subplots(figsize=(10, 4))

    subset = (
      df[df["Node"] == selected_node]
      .head(10)
      .iloc[::-1]
    )

    if len(subset) > 0:

      ax2.plot(
        subset["Timestamp"],
        subset["CPU"],
        marker="o",
        linewidth=3,
        label=selected_node
     )

    ax2.set_ylabel("CPU")
    ax2.set_xlabel("TimeStamp")

    ax2.legend()
    ax2.tick_params(axis="x", rotation=45)
    st.pyplot(fig2)

    # =================================================
    # MEMORY
    # =================================================

    st.subheader("💾 Memory Usage")

    fig3, ax3 = plt.subplots(figsize=(10, 4))

    subset = (
      df[df["Node"] == selected_node]
      .head(10)
     .iloc[::-1]
    )

    if len(subset) > 0:

      ax3.plot(
        subset["Timestamp"],
        subset["Memory"],
        marker="o",
        linewidth=3,
        label=selected_node
      )

    ax3.set_ylabel("Memory")
    ax3.set_xlabel("TimeStamp")

    ax3.legend()
    ax3.tick_params(axis="x", rotation=45)
    st.pyplot(fig3)

    # =================================================
    # AVAILABILITY
    # =================================================

    st.subheader("✅ Availability")

    fig4, ax4 = plt.subplots(figsize=(10, 4))

    subset = (
      df[df["Node"] == selected_node]
      .head(10)
      .iloc[::-1]
    )

    if len(subset) > 0:

      ax4.plot(
        subset["Timestamp"],
        subset["Availability"],
        marker="o",
        linewidth=3,
        label=selected_node
      )

    ax4.set_ylabel("Availability")
    ax4.set_xlabel("TimeStamp")
    ax4.tick_params(axis="x", rotation=45)
    ax4.legend()

    st.pyplot(fig4)