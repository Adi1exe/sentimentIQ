import streamlit as st
from utils.ui_components import render_page_header

def render():
    render_page_header(
        "👋 About the Developer",
        "Hi, I'm Aditya Dolas. Learn more about me and this project here."
    )
    
    st.markdown("""
<div style="background-color: #1e1e2e; padding: 2rem; border-radius: 12px; border: 1px solid #333;">
    <h3>Hi there! 👋</h3>
    <p style="font-size: 1.1rem; line-height: 1.6; color: #cbd5e1;">
        I'm <b>Adi</b>. Welcome to the <b>SentimentIQ</b> tool. 
        I built this application to demonstrate how modern AI can be leveraged for advanced 
        sentiment analysis on business text, emails, and customer feedback.
    </p>
    <hr style="border-color: #333; margin: 20px 0;">
    
    <h4>🚀 About the Project</h4>
    <p style="color: #94a3b8;">
        This tool processes inputs using the latest Google Gemini models, scoring them based on sentiment, urgency, and key themes, and even drafting automatic responses. Enjoy exploring the features!
    </p>
    
    <br/>
    <h4>🛠️ Tech Stack</h4>
    <ul style="color: #94a3b8;">
        <li><b>Frontend:</b> Python, Streamlit, HTML/CSS for custom UI</li>
        <li><b>AI Integration:</b> Google Gemini API</li>
        <li><b>Data Visualization:</b> Streamlit core components</li>
    </ul>
    
    <br/>
    <h4>🌐 Connect with me</h4>
    <p>
        <a href="https://github.com/Adi1exe" target="_blank" style="color: #a855f7; text-decoration: none; margin-right: 15px;">🔗 GitHub</a>
        <a href="https://www.linkedin.com/in/dolas-aditya/" target="_blank" style="color: #a855f7; text-decoration: none; margin-right: 15px;">💼 LinkedIn</a>
        <a href="https://adityadolas-theta.vercel.app/" target="_blank" style="color: #a855f7; text-decoration: none;">🌐 Portfolio</a>
    </p>
</div>
""", unsafe_allow_html=True)
