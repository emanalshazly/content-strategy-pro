# content-strategy-pro
# Content Strategy Designer Pro 🚀

## Overview
Content Strategy Designer Pro is an AI-powered application that helps businesses create comprehensive content strategies using Google's Gemini Pro model. The application generates personalized content strategies including audience analysis, content pillars, distribution plans, and metrics.

## Features
- 🎯 Customized content strategy generation
- 📊 Interactive strategy dashboard
- ⏱️ Timeline visualization
- 📈 Metrics tracking
- 💾 Strategy export functionality
- ✏️ Edit and customize options

## Technical Requirements
- Python 3.7+
- Google Cloud account
- Vertex AI API enabled
- Required Python packages:
  - streamlit
  - streamlit_tags
  - pandas
  - altair
  - vertexai
  - google-cloud-aiplatform

## Setup Instructions
1. Clone the repository
2. Install requirements:
   ```bash
   pip install streamlit streamlit_tags pandas altair google-cloud-aiplatform
   ```
3. Set up Google Cloud credentials
4. Update the PROJECT_ID in app.py
5. Run the application:
   ```bash
   streamlit run app.py
   ```

## How to Use
1. Enter your business details:
   - Business Type
   - Target Audience
   - Content Goals
   - Primary Platform

2. Click "Generate Strategy"
3. View your strategy across three tabs:
   - Strategy overview
   - Timeline
   - Metrics

4. Export or edit your strategy as needed

## Credits
Created by iman alshazli
Using Google's Vertex AI and Gemini Pro
