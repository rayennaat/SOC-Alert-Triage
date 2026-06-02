"""
SOC Alert Prioritization Dashboard
Built with Streamlit for real-time alert monitoring and classification
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="SOC Alert Prioritization",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
JAVA_BACKEND_URL = "http://localhost:8080"
PYTHON_ML_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
<style>
    .stAlert {
        padding: 1rem;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .critical-alert {
        background-color: #ff4444;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .high-alert {
        background-color: #ff8800;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/security-shield-green.png", width=80)
    st.title("🛡️ SOC Dashboard")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["📊 Overview", "🔍 Single Alert", "📁 Batch Upload", "⚙️ System Health"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 🎯 Model Info")
    st.metric("Accuracy", "99.98%")
    st.metric("Attack Types", "11")
    st.metric("Priority Levels", "4")

# Helper Functions
def check_service_health(url, service_name):
    """Check if a service is healthy"""
    try:
        if "8080" in url:
            # Java backend health endpoint
            response = requests.get(f"{url}/network-alerts/health", timeout=5)
        else:
            # Python ML service health endpoint
            response = requests.get(f"{url}/health", timeout=5)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Health check error for {service_name}: {str(e)}")
        return False

def get_priority_color(priority):
    """Get color for priority level"""
    colors = {
        'CRITICAL': '#ff4444',
        'HIGH': '#ff8800',
        'MEDIUM': '#ffbb33',
        'LOW': '#00C851'
    }
    return colors.get(priority, '#666666')

def get_priority_icon(priority):
    """Get icon for priority level"""
    icons = {
        'CRITICAL': '🚨',
        'HIGH': '⚠️',
        'MEDIUM': '📋',
        'LOW': '📊'
    }
    return icons.get(priority, '❓')

# =============================================================================
# PAGE 1: OVERVIEW DASHBOARD
# =============================================================================
if page == "📊 Overview":
    st.title("📊 Alert Prioritization Overview")
    
    # Health Status Bar
    col1, col2, col3 = st.columns(3)
    
    with col1:
        java_health = check_service_health(JAVA_BACKEND_URL, "Java Backend")
        status = "🟢 Online" if java_health else "🔴 Offline"
        st.metric("Java Backend", status)
    
    with col2:
        ml_health = check_service_health(PYTHON_ML_URL, "ML Service")
        status = "🟢 Online" if ml_health else "🔴 Offline"
        st.metric("ML Service", status)
    
    with col3:
        overall = "🟢 Operational" if (java_health and ml_health) else "🔴 Degraded"
        st.metric("System Status", overall)
    
    st.markdown("---")
    
    # Sample Data Section
    st.subheader("📈 Recent Alerts Analysis")
    
    if st.button("🔄 Load Sample Data", type="primary"):
        with st.spinner("Processing sample alerts..."):
            try:
                # Try to load real test data
                df = pd.read_csv("real_test_alerts.csv")
                
                # Send to ML service for classification
                files = {'file': open('real_test_alerts.csv', 'rb')}
                response = requests.post(f"{PYTHON_ML_URL}/prioritize/csv", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display summary metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    summary = result['prioritization_summary']
                    
                    with col1:
                        st.metric(
                            "🚨 CRITICAL",
                            summary.get('CRITICAL', 0),
                            delta=None,
                            delta_color="inverse"
                        )
                    
                    with col2:
                        st.metric(
                            "⚠️ HIGH",
                            summary.get('HIGH', 0)
                        )
                    
                    with col3:
                        st.metric(
                            "📋 MEDIUM",
                            summary.get('MEDIUM', 0)
                        )
                    
                    with col4:
                        st.metric(
                            "📊 LOW",
                            summary.get('LOW', 0)
                        )
                    
                    # Priority Distribution Chart
                    st.subheader("📊 Priority Distribution")
                    
                    fig_pie = px.pie(
                        values=list(summary.values()),
                        names=list(summary.keys()),
                        title="Alert Priority Breakdown",
                        color=list(summary.keys()),
                        color_discrete_map={
                            'CRITICAL': '#ff4444',
                            'HIGH': '#ff8800',
                            'MEDIUM': '#ffbb33',
                            'LOW': '#00C851'
                        }
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                    
                    # Attack Type Distribution
                    st.subheader("🎯 Attack Type Distribution")
                    
                    alerts_df = pd.DataFrame(result['all_alerts'])
                    attack_counts = alerts_df['attack_type'].value_counts()
                    
                    fig_bar = px.bar(
                        x=attack_counts.index,
                        y=attack_counts.values,
                        labels={'x': 'Attack Type', 'y': 'Count'},
                        title="Detected Attack Types",
                        color=attack_counts.values,
                        color_continuous_scale='Reds'
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                    
                    # Top Critical Alerts
                    st.subheader("🚨 Top 10 Critical Alerts")
                    
                    top_alerts = pd.DataFrame(result['all_alerts'][:10])
                    
                    for _, alert in top_alerts.iterrows():
                        priority = alert['priority_level']
                        icon = get_priority_icon(priority)
                        color = get_priority_color(priority)
                        
                        with st.container():
                            st.markdown(f"""
                            <div style="background-color: {color}; padding: 15px; border-radius: 8px; margin: 10px 0; color: white;">
                                <h4>{icon} Rank #{alert['rank']} - {alert['attack_type']}</h4>
                                <p><b>Alert ID:</b> {alert['alert_id']}</p>
                                <p><b>Source:</b> {alert['source_ip']} → <b>Destination:</b> {alert['dest_ip']}</p>
                                <p><b>Confidence:</b> {alert['attack_confidence']:.2%} | <b>Priority Score:</b> {alert['priority_score']:.2f}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.success(f"✅ Processed {result['total_alerts']} alerts successfully!")
                    
                else:
                    st.error(f"❌ Error: {response.status_code}")
                    
            except FileNotFoundError:
                st.warning("⚠️ Sample data file not found. Please upload a CSV file in the 'Batch Upload' tab.")
            except Exception as e:
                st.error(f"❌ Error processing data: {str(e)}")
    
    else:
        st.info("👆 Click 'Load Sample Data' to analyze recent alerts")

# =============================================================================
# PAGE 2: SINGLE ALERT CLASSIFICATION
# =============================================================================
elif page == "🔍 Single Alert":
    st.title("🔍 Single Alert Classification")
    st.markdown("Classify individual network traffic alerts using ML models")
    
    with st.form("alert_form"):
        st.subheader("Alert Metadata")
        
        col1, col2 = st.columns(2)
        
        with col1:
            alert_id = st.text_input("Alert ID", value="TEST-ALERT-001")
            source_ip = st.text_input("Source IP", value="192.168.1.100")
            timestamp = st.text_input("Timestamp", value=datetime.now().isoformat())
        
        with col2:
            dest_ip = st.text_input("Destination IP", value="10.0.0.50")
            asset_criticality = st.selectbox("Asset Criticality", ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
        
        st.subheader("Network Traffic Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            flow_duration = st.number_input("Flow Duration", value=8098507.0)
            total_fwd_packets = st.number_input("Total Fwd Packets", value=7.0)
            total_bwd_packets = st.number_input("Total Bwd Packets", value=5.0)
            flow_bytes_s = st.number_input("Flow Bytes/s", value=1439.40)
            flow_packets_s = st.number_input("Flow Packets/s", value=1.48)
            total_fwd_length = st.number_input("Total Fwd Length", value=50.0)
        
        with col2:
            total_bwd_length = st.number_input("Total Bwd Length", value=11607.0)
            fwd_packet_mean = st.number_input("Fwd Packet Mean", value=7.14)
            bwd_packet_mean = st.number_input("Bwd Packet Mean", value=2321.4)
            packet_std = st.number_input("Packet Length Std", value=2250.51)
            flow_iat_mean = st.number_input("Flow IAT Mean", value=736227.91)
            fwd_iat_mean = st.number_input("Fwd IAT Mean", value=1336039.83)
        
        with col3:
            bwd_iat_mean = st.number_input("Bwd IAT Mean", value=20756.75)
            psh_flag = st.number_input("PSH Flag Count", value=0, step=1)
            syn_flag = st.number_input("SYN Flag Count", value=0, step=1)
            fin_flag = st.number_input("FIN Flag Count", value=0, step=1)
            dest_port = st.number_input("Destination Port", value=80, step=1)
            down_up_ratio = st.number_input("Down/Up Ratio", value=0.0)
        
        submitted = st.form_submit_button("🔍 Classify Alert", type="primary")
        
        if submitted:
            with st.spinner("Classifying alert..."):
                # Build request
                request_data = {
                    "alertId": alert_id,
                    "sourceIp": source_ip,
                    "destIp": dest_ip,
                    "timestamp": timestamp,
                    "assetCriticality": asset_criticality,
                    "flowDuration": flow_duration,
                    "totalFwdPackets": total_fwd_packets,
                    "totalBackwardPackets": total_bwd_packets,
                    "flowBytesPerS": flow_bytes_s,
                    "flowPacketsPerS": flow_packets_s,
                    "totalLengthOfFwdPackets": total_fwd_length,
                    "totalLengthOfBwdPackets": total_bwd_length,
                    "fwdPacketLengthMean": fwd_packet_mean,
                    "bwdPacketLengthMean": bwd_packet_mean,
                    "packetLengthStd": packet_std,
                    "flowIATMean": flow_iat_mean,
                    "fwdIATMean": fwd_iat_mean,
                    "bwdIATMean": bwd_iat_mean,
                    "pshFlagCount": int(psh_flag),
                    "synFlagCount": int(syn_flag),
                    "finFlagCount": int(fin_flag),
                    "destinationPort": int(dest_port),
                    "downUpRatio": down_up_ratio
                }
                
                try:
                    response = requests.post(
                        f"{JAVA_BACKEND_URL}/network-alerts/classify",
                        json=request_data,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success("✅ Classification Complete!")
                        
                        # Display results
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🎯 Classification")
                            classification = result['classification']
                            st.metric(
                                "Attack Type",
                                classification['primaryAttackType'],
                                delta=f"{classification['confidence']:.2%} confidence"
                            )
                            
                            if classification.get('alternativeClassifications'):
                                st.write("**Alternative Classifications:**")
                                for alt in classification['alternativeClassifications'][:3]:
                                    st.write(f"- {alt['attackType']}: {alt['probability']:.2%}")
                        
                        with col2:
                            st.subheader("🚨 Prioritization")
                            priority = result['prioritization']
                            
                            icon = get_priority_icon(priority['priorityLevel'])
                            color = get_priority_color(priority['priorityLevel'])
                            
                            st.markdown(f"""
                            <div style="background-color: {color}; padding: 20px; border-radius: 10px; color: white; text-align: center;">
                                <h2>{icon} {priority['priorityLevel']}</h2>
                                <h3>Score: {priority['priorityScore']:.2f}</h3>
                                <p>Confidence: {priority['confidence']:.2%}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Recommendations
                        st.subheader("💡 Recommended Actions")
                        for rec in result['recommendations']:
                            st.info(rec)
                        
                        # Full response (expandable)
                        with st.expander("📄 View Full Response"):
                            st.json(result)
                        
                    else:
                        st.error(f"❌ Error: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ Error calling backend: {str(e)}")

# =============================================================================
# PAGE 3: BATCH UPLOAD
# =============================================================================
elif page == "📁 Batch Upload":
    st.title("📁 Batch Alert Classification")
    st.markdown("Upload CSV file containing multiple alerts for batch processing")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="CSV should contain alert_id, source_ip, dest_ip, timestamp, and all 18 network features"
    )
    
    if uploaded_file is not None:
        # Preview file
        st.subheader("📋 File Preview")
        df_preview = pd.read_csv(uploaded_file)
        st.dataframe(df_preview.head(10), use_container_width=True)
        
        st.info(f"📊 File contains {len(df_preview)} alerts")
        
        # Process button
        if st.button("🚀 Process All Alerts", type="primary"):
            uploaded_file.seek(0)  # Reset file pointer
            
            with st.spinner("Processing alerts... This may take a moment."):
                try:
                    files = {'file': (uploaded_file.name, uploaded_file, 'text/csv')}
                    
                    response = requests.post(
                        f"{JAVA_BACKEND_URL}/network-alerts/batch",
                        files=files,
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success(f"✅ Successfully processed {result['total_alerts']} alerts!")
                        
                        # Summary metrics
                        col1, col2, col3, col4 = st.columns(4)
                        
                        summary = result['prioritization_summary']
                        
                        with col1:
                            st.metric("🚨 CRITICAL", summary.get('CRITICAL', 0))
                        with col2:
                            st.metric("⚠️ HIGH", summary.get('HIGH', 0))
                        with col3:
                            st.metric("📋 MEDIUM", summary.get('MEDIUM', 0))
                        with col4:
                            st.metric("📊 LOW", summary.get('LOW', 0))
                        
                        # Results table
                        st.subheader("📊 Classification Results")
                        
                        results_df = pd.DataFrame(result['all_alerts'])
                        
                        # Add color coding
                        def color_priority(val):
                            colors = {
                                'CRITICAL': 'background-color: #ff4444; color: white',
                                'HIGH': 'background-color: #ff8800; color: white',
                                'MEDIUM': 'background-color: #ffbb33; color: black',
                                'LOW': 'background-color: #00C851; color: white'
                            }
                            return colors.get(val, '')
                        
                        styled_df = results_df[['rank', 'alert_id', 'attack_type', 'attack_confidence', 
                                               'priority_level', 'priority_score']].style.applymap(
                            color_priority, subset=['priority_level']
                        )
                        
                        st.dataframe(styled_df, use_container_width=True, height=400)
                        
                        # Download results
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv,
                            file_name=f"classified_alerts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                        
                    else:
                        st.error(f"❌ Error: {response.status_code}")
                        st.text(response.text)
                        
                except Exception as e:
                    st.error(f"❌ Error processing file: {str(e)}")

# =============================================================================
# PAGE 4: SYSTEM HEALTH
# =============================================================================
elif page == "⚙️ System Health":
    st.title("⚙️ System Health & Diagnostics")
    
    # Service Status
    st.subheader("🔌 Service Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Java Backend")
        java_health = check_service_health(JAVA_BACKEND_URL, "Java Backend")
        
        if java_health:
            st.success("🟢 Online and responding")
            st.code(f"URL: {JAVA_BACKEND_URL}")
        else:
            st.error("🔴 Offline or unreachable")
            st.code(f"URL: {JAVA_BACKEND_URL}")
    
    with col2:
        st.markdown("### ML Service")
        ml_health = check_service_health(PYTHON_ML_URL, "ML Service")
        
        if ml_health:
            st.success("🟢 Online and responding")
            st.code(f"URL: {PYTHON_ML_URL}")
            
            # Get ML service details
            try:
                response = requests.get(f"{PYTHON_ML_URL}/health")
                if response.status_code == 200:
                    health_data = response.json()
                    
                    st.json(health_data)
            except:
                pass
        else:
            st.error("🔴 Offline or unreachable")
            st.code(f"URL: {PYTHON_ML_URL}")
    
    st.markdown("---")
    
    # Model Information
    st.subheader("🤖 ML Model Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Model Accuracy", "99.98%")
    with col2:
        st.metric("Attack Types", "11")
    with col3:
        st.metric("Training Samples", "557,646")
    
    # Supported attacks
    st.subheader("🎯 Supported Attack Types")
    
    attacks = {
        "CRITICAL": ["DDoS", "Heartbleed", "Infiltration"],
        "HIGH": ["DoS Hulk", "DoS GoldenEye", "Bot"],
        "MEDIUM": ["DoS Slowhttptest", "DoS slowloris", "FTP-Patator", "SSH-Patator"],
        "LOW": ["PortScan"]
    }
    
    for priority, attack_list in attacks.items():
        icon = get_priority_icon(priority)
        st.markdown(f"**{icon} {priority}**: {', '.join(attack_list)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🛡️ SOC Alert Prioritization System | Powered by ML (99.98% Accuracy)</p>
    <p>Built with ❤️ using Streamlit, FastAPI, and Spring Boot</p>
</div>
""", unsafe_allow_html=True)