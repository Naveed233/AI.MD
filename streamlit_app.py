"""
AI Merchandising System - Streamlit Web App
Deploy to: streamlit.app or share via Streamlit Cloud
"""

import streamlit as st
import requests
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="AI Merchandising System",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .metric-box {
        background-color: white;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state and get ML API URL from environment or default
import os
ML_API_URL = os.getenv("ML_API_URL", "http://localhost:8080")

if 'ml_api_url' not in st.session_state:
    st.session_state.ml_api_url = ML_API_URL

# Header
st.markdown('<div class="main-header">🛍️ AI Merchandising System</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    ml_url = st.text_input(
        "ML Service URL",
        value=st.session_state.ml_api_url,
        help="URL of the ML prediction service"
    )
    st.session_state.ml_api_url = ml_url
    
    st.markdown("---")
    st.header("📊 About")
    st.info("""
    This system predicts optimal inventory levels
    using AI trained on 541K+ transactions.
    
    **Model:** Random Forest Regressor
    **Accuracy:** 97% (R² = 0.97)
    """)
    
    # Show environment info
    with st.expander("🔧 Environment Info"):
        st.code(f"""
        ML API URL: {st.session_state.ml_api_url}
        Environment: {os.getenv('STREAMLIT_ENV', 'local')}
        """)
    
    if st.button("🔍 Test Connection"):
        try:
            response = requests.get(f"{ml_url}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ Connected to ML Service!")
            else:
                st.error(f"❌ Connection failed: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Cannot connect: {str(e)}")

# Main content
tab1, tab2, tab3 = st.tabs(["📈 Predict Demand", "📊 Analytics", "🤖 Model Info"])

with tab1:
    st.header("Demand Prediction")
    st.markdown("Enter customer data to predict optimal inventory levels")
    
    col1, col2 = st.columns(2)
    
    with col1:
        customer_id = st.text_input("Customer ID", value="C001", placeholder="Enter customer ID")
        age = st.number_input("Age", min_value=0, max_value=120, value=35, step=1)
        purchase_history = st.number_input("Purchase History (count)", min_value=0, value=20, step=1)
        avg_order_value = st.number_input("Average Order Value ($)", min_value=0.0, value=150.50, step=1.0)
    
    with col2:
        last_purchase_days = st.number_input("Days Since Last Purchase", min_value=0, value=7, step=1)
        region = st.selectbox(
            "Region",
            options=["North America", "South America", "Europe", "Asia", "Africa", "Oceania"],
            index=0
        )
        seasonality_factor = st.slider(
            "Seasonality Factor",
            min_value=0.1,
            max_value=5.0,
            value=1.2,
            step=0.1,
            help="1.0 = normal, >1.0 = high season (holidays), <1.0 = low season"
        )
    
    if st.button("🔮 Predict Demand", type="primary", use_container_width=True):
        # Prepare request
        payload = {
            "customer_id": customer_id,
            "age": float(age),
            "purchase_history": int(purchase_history),
            "avg_order_value": float(avg_order_value),
            "last_purchase_days": int(last_purchase_days),
            "region": region,
            "seasonality_factor": float(seasonality_factor)
        }
        
        # Show loading
        with st.spinner("🤖 AI is analyzing..."):
            try:
                response = requests.post(
                    f"{st.session_state.ml_api_url}/predict",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("✅ Prediction Complete!")
                    
                    # Display results
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "Predicted Demand",
                            f"{result['predicted_demand']:.0f}",
                            help="Expected demand in units"
                        )
                    
                    with col2:
                        category_color = {
                            "High": "🟢",
                            "Medium": "🟡",
                            "Low": "🔴"
                        }
                        st.metric(
                            "Category",
                            f"{category_color.get(result['category'], '⚪')} {result['category']}"
                        )
                    
                    with col3:
                        st.metric(
                            "Optimal Stock",
                            f"{result['optimal_stock']}",
                            help="Recommended stock level (demand + 20% buffer)"
                        )
                    
                    with col4:
                        st.metric(
                            "Confidence",
                            f"{result['confidence']*100:.1f}%",
                            help="Model confidence level"
                        )
                    
                    # Detailed view
                    with st.expander("📋 View Detailed Results"):
                        st.json(result)
                    
                    # Store in session state for analytics
                    if 'predictions' not in st.session_state:
                        st.session_state.predictions = []
                    st.session_state.predictions.append({
                        **payload,
                        **result,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                else:
                    st.error(f"❌ Error: HTTP {response.status_code}")
                    st.text(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to ML service.")
                st.warning(f"**ML Service URL:** {st.session_state.ml_api_url}")
                st.info("""
                💡 **To fix this:**
                - For local: Start ML service with `docker compose up ml_service`
                - For Streamlit Cloud: Set `ML_API_URL` in Streamlit Secrets
                - Or update the URL in the sidebar above
                """)
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The ML service may be slow or unreachable.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

with tab2:
    st.header("Analytics Dashboard")
    
    if 'predictions' not in st.session_state or len(st.session_state.predictions) == 0:
        st.info("👆 Make some predictions first to see analytics here!")
    else:
        predictions = st.session_state.predictions
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Predictions", len(predictions))
        
        with col2:
            avg_demand = sum(p['predicted_demand'] for p in predictions) / len(predictions)
            st.metric("Avg Predicted Demand", f"{avg_demand:.0f}")
        
        with col3:
            avg_confidence = sum(p['confidence'] for p in predictions) / len(predictions)
            st.metric("Avg Confidence", f"{avg_confidence*100:.1f}%")
        
        with col4:
            high_demand = sum(1 for p in predictions if p['category'] == 'High')
            st.metric("High Demand Predictions", high_demand)
        
        # Category distribution
        st.subheader("Demand Category Distribution")
        categories = {}
        for p in predictions:
            cat = p['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(categories)
        
        with col2:
            st.write("**Distribution:**")
            for cat, count in categories.items():
                percentage = (count / len(predictions)) * 100
                st.write(f"{cat}: {count} ({percentage:.1f}%)")
        
        # Recent predictions
        st.subheader("Recent Predictions")
        recent = predictions[-10:][::-1]  # Last 10, reversed
        for pred in recent:
            with st.expander(f"Customer {pred['customer_id']} - {pred['category']} ({(pred['confidence']*100):.0f}% confidence)"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Predicted Demand:** {pred['predicted_demand']:.0f} units")
                    st.write(f"**Optimal Stock:** {pred['optimal_stock']} units")
                with col2:
                    st.write(f"**Age:** {pred['age']}")
                    st.write(f"**Purchase History:** {pred['purchase_history']}")
                    st.write(f"**Region:** {pred['region']}")
        
        # Clear predictions
        if st.button("🗑️ Clear All Predictions"):
            st.session_state.predictions = []
            st.rerun()

with tab3:
    st.header("Model Information")
    
    st.subheader("🤖 AI Model Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Algorithm:** Random Forest Regressor  
        **Trees:** 100 decision trees  
        **Training Data:** 541,909 transactions  
        **Features:** 6 input features
        """)
    
    with col2:
        st.success("""
        **Performance Metrics:**
        - R² Score: 0.97 (97% accuracy)
        - MAE: 17.91 units
        - MSE: 569.28
        """)
    
    st.subheader("📊 Input Features")
    st.write("""
    The model uses these 6 features to predict demand:
    1. **Age** - Customer age
    2. **Purchase History** - Number of past purchases
    3. **Average Order Value** - Average spending per order
    4. **Last Purchase Days** - Days since last purchase
    5. **Region** - Geographic location
    6. **Seasonality Factor** - Seasonal adjustment
    """)
    
    st.subheader("📈 How It Works")
    st.write("""
    1. Model was trained on 541K real e-commerce transactions
    2. 100 decision trees analyze the input features
    3. Each tree votes on the predicted demand
    4. Final prediction is the average of all votes
    5. System adds 20% buffer for optimal stock recommendation
    """)
    
    # Model health check
    st.subheader("🔍 Model Status")
    if st.button("Check Model Health"):
        try:
            response = requests.get(f"{st.session_state.ml_api_url}/health", timeout=5)
            if response.status_code == 200:
                health = response.json()
                st.success("✅ Model is healthy and loaded!")
                st.json(health)
            else:
                st.error("❌ Model health check failed")
        except Exception as e:
            st.error(f"❌ Cannot connect to ML service: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>AI Merchandising System | Powered by Random Forest ML</div>",
    unsafe_allow_html=True
)

