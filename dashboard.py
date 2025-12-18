import streamlit as st
import pandas as pd
import time
import os

#config
st.set_page_config(layout="wide", page_title="k8s-dashboard | Symphony IoT Orchestrator",page_icon="☸️")
DATA_FILE = 'data/telemetry.csv'

#hfunc
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=['timestamp', 'device_type', 'cpu', 'memory', 'battery', 'temp', 'vibration'])
    
    try:
        df = pd.read_csv(DATA_FILE)
        #time-stamp to date-time
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['timestamp'] = df['timestamp'].dt.floor('s')
        return df
    except Exception as e:
        #st.error(f"Error reading telemetry: {e}")
        return pd.DataFrame()

#dash board.
st.title(" Symphony IoT: Multi-Device Telemetry")

#side bar
st.sidebar.header("Orchestration Controller")
device_filter = st.sidebar.selectbox("Select Device Stream", 
    ["All", "Linux (Host)", "Android", "iOS", "Win11", "Rpi"])

refresh_rate_hz = st.sidebar.slider("Refresh Rate (Hz)", 1, 60, 30)
sleep_delay=1.0/refresh_rate_hz
# Placeholder for the main loop
dashboard_placeholder = st.empty()

while True:
    df = load_data()
    
    if not df.empty:
        with dashboard_placeholder.container():
            last_ts = df['timestamp'].iloc[-1]
            # date-time
            if isinstance(last_ts, str):
                last_ts = pd.to_datetime(last_ts)
            
            latency = (pd.Timestamp.now() - last_ts).total_seconds()
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 🐳 Container Status")
            st.sidebar.code("ID: iot-orchestration-49b84a\nImage: symphony/edge:v2", language="bash")
            
            # status
            status_color = "🟢" if latency < 2 else "🟠"
            st.sidebar.write(f"{status_color} **Link Latency:** {latency*1000:.0f}ms")
            # filter1
            if device_filter != "All":
                # filter-view
                filtered_df = df[df['device_type'] == device_filter]
                
                if not filtered_df.empty:
                    latest = filtered_df.iloc[-1]
                    
                    # Metricing
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("CPU Load", f"{int(latest['cpu'])}%", delta=f"{latest['cpu'] - 50:.1f}")
                    col2.metric("Memory", f"{int(latest['memory'])}%")
                    col3.metric("Battery", f"{int(latest['battery'])}%")
                    col4.metric("Temperature", f"{int(latest['temp'])}°C")

                    # chart - cpuVmem
                    st.subheader(f"Real-Time Metrics: {device_filter}")
                    chart_data = filtered_df.set_index('timestamp')[['cpu', 'memory', 'vibration']]
                    st.line_chart(chart_data)
                else:
                    st.warning(f"No data received yet for {device_filter}...")

            else:
                # aggregate - allView
                latest_df = df.groupby('device_type').last().reset_index()
                
                # Averages for the top cards
                avg_cpu = latest_df['cpu'].mean()
                avg_temp = latest_df['temp'].mean()
                active_devs = len(latest_df)

                col1, col2, col3 = st.columns(3)
                col1.metric("Active Endpoints", f"{active_devs}/5", "Online")
                col2.metric("Avg Cluster CPU", f"{int(avg_cpu)}%")
                col3.metric("Avg Cluster Temp", f"{int(avg_temp)}°C")

                # multi-line chart.
                st.subheader("Cluster CPU Load (Comparison)")
                # dataframe=>device=column
                pivot_df = df.pivot_table(index='timestamp', columns='device_type', values='cpu')
                st.line_chart(pivot_df.tail(50)) # last 50 datapoints

    time.sleep(sleep_delay)