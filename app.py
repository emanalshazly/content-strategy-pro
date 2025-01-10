import streamlit as st
from streamlit_tags import st_tags
import pandas as pd
import altair as alt
from datetime import datetime
import json
from vertexai.preview.generative_models import GenerativeModel
import vertexai

# Initialize Vertex AI
PROJECT_ID = "content-strategy-pro"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Page Configuration
st.set_page_config(layout="wide", page_title="Content Strategy Designer Pro")

# Add Custom CSS
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 16px;
    }
    .metric-card {
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

def generate_content_strategy(inputs):
    model = GenerativeModel("gemini-1.0-pro")
    
    prompt = f"""Create a content strategy for:
Business Type: {inputs['business']}
Audience: {inputs['audience']}
Goals: {inputs['goals']}
Platform: {inputs['platform']}

Return the strategy as a simple JSON object with these exact keys:
- audience_analysis (array of 3 points)
- content_pillars (array of 3 points)
- distribution_strategy (array of 3 points)
- content_calendar (array of 3 points)
- metrics (array of 3 points)
- timeline (array of 3 points)

Keep all text simple and avoid any special characters or formatting.
Respond with ONLY the JSON object, nothing else."""

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Find the JSON part if there's extra text
        start = response_text.find('{')
        end = response_text.rfind('}')
        if start != -1 and end != -1:
            response_text = response_text[start:end+1]
            
        # Parse JSON
        result = json.loads(response_text)
        return result
    except Exception as e:
        st.error(f"Error parsing strategy: {str(e)}")
        st.write("Raw response:", response_text)
        return None

# Main App Layout
st.title("Content Strategy Designer Pro 🚀")

# Input Form
business_type = st.text_input("Business Type 🏢", placeholder="e.g., E-commerce, SaaS")
target_audience = st.text_input("Target Audience 👥", placeholder="e.g., Young professionals")
content_goals = st.text_area("Content Goals 🎯", placeholder="What do you want to achieve?")
platform = st.selectbox("Primary Platform 📱", 
                      ["All Platforms", "Website/Blog", "Social Media", "Email Marketing"])

# Generate Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Generate Strategy ✨", type="primary", use_container_width=True):
        if not all([business_type, target_audience, content_goals]):
            st.error("Please fill all required fields")
        else:
            with st.spinner("Generating your strategy..."):
                strategy = generate_content_strategy({
                    "business": business_type,
                    "audience": target_audience,
                    "goals": content_goals,
                    "platform": platform
                })
                if strategy:
                    st.session_state.strategy = strategy

# Display Strategy
if 'strategy' in st.session_state and st.session_state.strategy is not None:
    tabs = st.tabs(["Strategy 📋", "Timeline ⏱️", "Metrics 📊"])
    
    # Strategy Tab
    with tabs[0]:
        for section, items in st.session_state.strategy.items():
            with st.expander(section.replace('_', ' ').title()):
                for item in items:
                    col1, col2 = st.columns([0.05, 0.95])
                    with col1:
                        st.checkbox("", key=f"check_{item}")
                    with col2:
                        st.write(item)
    
    # Timeline Tab
    with tabs[1]:
        timeline_df = pd.DataFrame({
            'Month': [f"Month {i+1}" for i in range(6)],
            'Tasks': st.session_state.strategy['timeline'][:6] if len(st.session_state.strategy['timeline']) >= 6 
                    else st.session_state.strategy['timeline'] + [''] * (6 - len(st.session_state.strategy['timeline']))
        })
        st.dataframe(timeline_df, use_container_width=True)
    
    # Metrics Tab
    with tabs[2]:
        metrics = st.session_state.strategy['metrics']
        cols = st.columns(2)
        for i, metric in enumerate(metrics):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{metric}</h3>
                    <p>Target: Set your goal</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Export Options
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            label="📥 Download Strategy",
            data=json.dumps(st.session_state.strategy, indent=2),
            file_name=f"content_strategy_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
    with col2:
        if st.button("✏️ Edit Strategy", use_container_width=True):
            st.session_state.editing = True
    with col3:
        if st.button("📤 Share Strategy", use_container_width=True):
            st.info("Sharing feature coming soon!")
