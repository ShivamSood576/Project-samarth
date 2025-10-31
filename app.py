"""Project Samarth - Advanced Streamlit Web Application"""

import streamlit as st
import os
import base64
from dotenv import load_dotenv
from src import QueryPlanner, QueryExecutor, DataGovInConnector, AnswerGenerator

# Page config
st.set_page_config(
    page_title="Project Samarth - Agricultural Data Q&A",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Purple & Blue Theme with Enhanced Design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=Roboto:wght@300;400;500&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main container with vibrant gradient background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        background-attachment: fixed;
    }
    
    /* Animated gradient background */
    .stApp {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 25%, rgba(240, 147, 251, 0.90) 50%, rgba(79, 172, 254, 0.90) 75%, rgba(0, 242, 254, 0.85) 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        background-attachment: fixed;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Modern Hero Section with Glass Effect */
    .hero-section {
        background: linear-gradient(135deg, rgba(138, 43, 226, 0.25) 0%, rgba(75, 0, 130, 0.2) 100%);
        backdrop-filter: blur(30px) saturate(180%);
        -webkit-backdrop-filter: blur(30px) saturate(180%);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 30px;
        padding: 3.5rem 2.5rem;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 12px 48px rgba(138, 43, 226, 0.4), 
                    0 0 80px rgba(147, 51, 234, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
        animation: fadeInDown 0.8s ease-out, float 6s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #e0c3fc 25%, #8ec5fc 50%, #ffffff 75%, #fbc2eb 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        text-shadow: 0 0 60px rgba(255, 255, 255, 0.5);
        letter-spacing: -2px;
        animation: shimmer 3s linear infinite;
        position: relative;
        z-index: 1;
    }
    
    @keyframes shimmer {
        to { background-position: 200% center; }
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 400;
        letter-spacing: 1px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }
    
    /* Chat container with modern glass effect */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.12) !important;
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1.5px solid rgba(255, 255, 255, 0.18);
        border-radius: 20px !important;
        padding: 1.8rem !important;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
        animation: slideInUp 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.4);
    }
    
    /* User message - Purple gradient */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, rgba(147, 51, 234, 0.3) 0%, rgba(126, 34, 206, 0.25) 100%) !important;
        border-left: 4px solid #a855f7;
        box-shadow: 0 8px 32px rgba(147, 51, 234, 0.3);
    }
    
    /* Assistant message - Blue/Cyan gradient */
    .stChatMessage[data-testid="assistant-message"] {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.25) 0%, rgba(6, 182, 212, 0.2) 100%) !important;
        border-left: 4px solid #06b6d4;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.25);
    }
    
    /* Sidebar with vibrant gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(88, 28, 135, 0.9) 0%, rgba(49, 46, 129, 0.9) 50%, rgba(30, 58, 138, 0.9) 100%);
        backdrop-filter: blur(15px) saturate(180%);
        border-right: 2px solid rgba(255, 255, 255, 0.15);
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    
    /* Example buttons - Vibrant neon style */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.25) 0%, rgba(139, 92, 246, 0.2) 100%);
        color: #e9d5ff;
        border: 2px solid rgba(168, 85, 247, 0.5);
        border-radius: 15px;
        padding: 0.9rem 1.3rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.45) 0%, rgba(139, 92, 246, 0.4) 100%);
        border-color: #c084fc;
        color: #ffffff;
        box-shadow: 0 0 30px rgba(168, 85, 247, 0.6), 
                    0 0 60px rgba(168, 85, 247, 0.3),
                    inset 0 0 20px rgba(168, 85, 247, 0.2);
        transform: translateY(-3px) scale(1.02);
    }
    
    /* Input field with enhanced glass effect */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(20px) saturate(180%);
        border: 2px solid rgba(255, 255, 255, 0.25);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .stChatInputContainer:focus-within {
        border-color: rgba(168, 85, 247, 0.6);
        box-shadow: 0 8px 32px rgba(168, 85, 247, 0.4), 
                    0 0 40px rgba(168, 85, 247, 0.2);
    }
    
    /* Enhanced Confidence badges with glow */
    .confidence-badge {
        display: inline-block;
        padding: 0.6rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.95rem;
        backdrop-filter: blur(15px) saturate(180%);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
    }
    
    .confidence-badge:hover {
        transform: scale(1.05);
    }
    
    .confidence-high {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.35) 0%, rgba(22, 163, 74, 0.3) 100%);
        color: #bbf7d0;
        border: 2px solid rgba(34, 197, 94, 0.6);
        text-shadow: 0 0 10px rgba(34, 197, 94, 0.5);
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.3), 
                    0 0 30px rgba(34, 197, 94, 0.2);
    }
    
    .confidence-medium {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.35) 0%, rgba(245, 158, 11, 0.3) 100%);
        color: #fef3c7;
        border: 2px solid rgba(251, 191, 36, 0.6);
        text-shadow: 0 0 10px rgba(251, 191, 36, 0.5);
        box-shadow: 0 6px 20px rgba(251, 191, 36, 0.3), 
                    0 0 30px rgba(251, 191, 36, 0.2);
    }
    
    .confidence-low {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.35) 0%, rgba(220, 38, 38, 0.3) 100%);
        color: #fecaca;
        border: 2px solid rgba(239, 68, 68, 0.6);
        text-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.3), 
                    0 0 30px rgba(239, 68, 68, 0.2);
    }
    
    /* Enhanced info cards with gradient borders */
    .info-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(20px) saturate(180%);
        border: 2px solid rgba(255, 255, 255, 0.18);
        border-radius: 20px;
        padding: 1.8rem;
        margin: 1.2rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .info-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #a855f7, #ec4899, #06b6d4, #a855f7);
        background-size: 200% auto;
        animation: shimmer 3s linear infinite;
    }
    
    .info-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(168, 85, 247, 0.3);
        border-color: rgba(168, 85, 247, 0.4);
    }
    
    .info-card h3 {
        color: #e9d5ff;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        font-weight: 700;
        text-shadow: 0 2px 10px rgba(168, 85, 247, 0.3);
    }
    
    .info-card p {
        color: rgba(255, 255, 255, 0.85);
        font-size: 0.95rem;
        line-height: 1.7;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Divider with gradient glow */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.6), rgba(236, 72, 153, 0.6), transparent);
        margin: 2.5rem 0;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
    }
    
    /* Expander with enhanced styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1.5px solid rgba(168, 85, 247, 0.3);
        color: rgba(255, 255, 255, 0.95);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.3) 0%, rgba(139, 92, 246, 0.25) 100%);
        border-color: rgba(168, 85, 247, 0.5);
        box-shadow: 0 0 25px rgba(168, 85, 247, 0.3);
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Custom scrollbar - Purple theme */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 27, 75, 0.6);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 50%, #06b6d4 100%);
        border-radius: 10px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #c084fc 0%, #f472b6 50%, #22d3ee 100%);
        box-shadow: 0 0 25px rgba(168, 85, 247, 0.7);
    }
    
    /* Text colors - Enhanced readability */
    .stMarkdown, p, li {
        color: rgba(255, 255, 255, 0.92);
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: rgba(255, 255, 255, 0.98);
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Status messages with glass effect */
    .stAlert {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
        backdrop-filter: blur(15px) saturate(180%);
        border-radius: 15px;
        border: 1.5px solid rgba(168, 85, 247, 0.3);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Spinner - Purple theme */
    .stSpinner > div {
        border-top-color: #a855f7 !important;
        border-right-color: #ec4899 !important;
    }
    
    /* Additional decorative elements */
    .stProgress > div > div {
        background: linear-gradient(90deg, #a855f7, #ec4899, #06b6d4);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_system():
    """Initialize the Q&A system components."""
    load_dotenv()
    
    data_gov_key = os.getenv('DATA_GOV_IN_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not data_gov_key or not gemini_key:
        st.error("❌ API keys not found! Please set DATA_GOV_IN_API_KEY and GEMINI_API_KEY in Hugging Face Spaces secrets.")
        st.stop()
    
    try:
        connector = DataGovInConnector(api_key=data_gov_key)
        planner = QueryPlanner(api_key=gemini_key)
        executor = QueryExecutor(connector)
        answer_gen = AnswerGenerator(api_key=gemini_key)
        return planner, executor, answer_gen
    except Exception as e:
        st.error(f"❌ Failed to initialize system: {e}")
        st.stop()


def get_confidence_badge(confidence: float) -> str:
    """Generate modern confidence badge HTML."""
    pct = confidence * 100
    if pct >= 90:
        return f'<span class="confidence-badge confidence-high">✓ HIGH CONFIDENCE {pct:.0f}%</span>'
    elif pct >= 70:
        return f'<span class="confidence-badge confidence-medium">◐ MEDIUM CONFIDENCE {pct:.0f}%</span>'
    else:
        return f'<span class="confidence-badge confidence-low">! LOW CONFIDENCE {pct:.0f}%</span>'


def main():
    # Hero Section with animated glassmorphism
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🌾 PROJECT SAMARTH</div>
        <div class="hero-subtitle">✨ AI-Powered Agricultural Intelligence Platform ✨</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize system
    planner, executor, answer_gen = initialize_system()
    
    # Sidebar with modern cards
    with st.sidebar:
        st.markdown("""
        <div class="info-card">
            <h3>🤖 About Samarth</h3>
            <p>Next-generation AI platform combining real-time agricultural data from data.gov.in with advanced natural language processing to deliver intelligent, cited insights for India's farming community.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### ⚡ Quick Examples")
        examples = [
            ("🌾 Production Comparison", "Which state had more rice production in 2015 - Karnataka or Tamil Nadu?"),
            ("🌧️ Climate Analysis", "Compare rainfall in Karnataka vs Tamil Nadu for last 5 years"),
            ("📊 District Insights", "Which district in Karnataka has the highest maize production?"),
            ("🔗 Correlation Study", "Is there a correlation between rainfall and rice production in Tamil Nadu?"),
            ("📋 Policy Analysis", "What are three arguments to promote Bajra over Rice in Rajasthan?")
        ]
        
        for i, (label, question) in enumerate(examples, 1):
            if st.button(label, key=f"ex_{i}", use_container_width=True):
                st.session_state.example_query = question
        
        st.divider()
        
        st.markdown("""
        <div class="info-card">
            <h3>📡 Live Data Sources</h3>
            <p>
            🌾 District-level Crop Production<br>
            🌧️ IMD Climate & Rainfall Data<br>
            💰 Agricultural Market Prices<br>
            🗺️ Pan-India State & District Coverage<br>
            📊 Historical Trends (1901-2017)
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <h3>✨ Intelligent Features</h3>
            <p>
            🧠 Advanced NLP Query Understanding<br>
            ⚡ Real-time API Data Integration<br>
            🎯 AI-Powered Cross-Domain Analysis<br>
            📈 Statistical Confidence Scoring<br>
            📑 Transparent Source Citations<br>
            🔗 Correlation & Trend Detection
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Chat History", key="clear_btn", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Welcome message with modern styling
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="info-card" style="text-align: center; padding: 2.5rem;">
            <h2 style="background: linear-gradient(135deg, #e9d5ff 0%, #fbbf24 50%, #06b6d4 100%); 
                       -webkit-background-clip: text; 
                       -webkit-text-fill-color: transparent; 
                       font-size: 2rem; 
                       margin-bottom: 1.5rem; 
                       font-weight: 800;">
                👋 Welcome to Agricultural Intelligence Reimagined
            </h2>
            <p style="font-size: 1.15rem; line-height: 2; color: rgba(255, 255, 255, 0.9);">
                Harness the power of AI to explore India's agricultural landscape. Ask complex questions in <strong>plain language</strong> and receive data-backed insights with full transparency and citations.
            </p>
            <p style="color: rgba(255, 255, 255, 0.7); margin-top: 1.5rem; font-size: 1.05rem;">
                💬 Start by typing your question below or choose a quick example from the sidebar →
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)
            if "metadata" in message:
                with st.expander("📊 View Details"):
                    st.json(message["metadata"])
    
    # Handle example query
    if "example_query" in st.session_state:
        query = st.session_state.example_query
        del st.session_state.example_query
    else:
        query = st.chat_input("Ask me anything about Indian agriculture...")
    
    # Process query
    if query:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        
        # Process with assistant
        with st.chat_message("assistant"):
            try:
                # Simple, clean progress indicator
                with st.spinner("Analyzing..."):
                    plan = planner.parse_question(query)
                    result = executor.execute(plan)
                    data_summary = answer_gen.extract_data_summary(plan, result.data, result.metadata)
                    enhanced_answer = answer_gen.generate_answer(
                        original_question=query,
                        query_plan=plan,
                        raw_answer=result.answer,
                        data_summary=data_summary,
                        metadata=result.metadata
                    )
                
                # Display answer
                st.markdown(enhanced_answer)
                
                # Display confidence with modern badge
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    f'<div style="text-align: center; margin: 1.5rem 0;">{get_confidence_badge(result.confidence)}</div>',
                    unsafe_allow_html=True
                )
                
                # Create response message
                response_content = f"{enhanced_answer}\n\n---\n**Confidence:** {get_confidence_badge(result.confidence)}"
                
                # Add to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_content,
                    "metadata": {
                        "intent": plan.intent,
                        "states": plan.states,
                        "crops": plan.crops,
                        "years": f"{plan.year_start}-{plan.year_end}",
                        "confidence": f"{result.confidence*100:.0f}%"
                    }
                })
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"❌ Sorry, I encountered an error: {str(e)}\n\nPlease try rephrasing your question."
                })


if __name__ == "__main__":
    main()
