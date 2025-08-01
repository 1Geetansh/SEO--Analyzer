import streamlit as st
import validators
from seo_analyzer import SEOAnalyzer
from preview_generators import PreviewGenerator
import time

# Page configuration
st.set_page_config(
    page_title="SEO Meta Tag Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS for responsive design and better styling
st.markdown("""
<style>
    /* Mobile-first responsive design */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 1200px;
    }
    
    /* Better button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        margin: 0.5rem 0;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* SEO Score styling */
    .seo-score-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1rem 0;
    }
    
    .seo-score {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        min-width: 200px;
    }
    
    .seo-score h2 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .seo-score p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 0.9rem;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e1e5e9;
        padding: 0.75rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Preview cards responsive design */
    .preview-card {
        margin: 1rem 0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .preview-card:hover {
        transform: translateY(-2px);
    }
    
    /* Responsive columns */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        .seo-score {
            padding: 1rem 1.5rem;
            min-width: 150px;
        }
        
        .seo-score h2 {
            font-size: 1.5rem;
        }
        
        /* Stack columns on mobile */
        .element-container {
            width: 100% !important;
        }
    }
    
    /* Header styling */
    h1 {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    /* Issues and recommendations styling */
    .issue-item {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    
    .recommendation-item {
        background: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    
    /* Expandable sections */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    /* Character count styling */
    .character-count {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #f8f9fa;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 1px solid #e1e5e9;
        color: #6c757d;
    }
    
    /* Tab styling improvements */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        background-color: #f8f9fa;
        border-radius: 8px;
        color: #495057;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    
    /* Meta tags section styling */
    .meta-tag-section {
        background: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .meta-tag-item {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Responsive improvements for small screens */
    @media (max-width: 480px) {
        .main .block-container {
            padding-left: 0.25rem;
            padding-right: 0.25rem;
        }
        
        .seo-score {
            padding: 1rem;
            min-width: 120px;
        }
        
        .seo-score h2 {
            font-size: 1.25rem;
        }
        
        .preview-card {
            margin: 0.5rem 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0 12px;
            font-size: 0.9rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize analyzers
@st.cache_resource
def get_analyzers():
    return SEOAnalyzer(), PreviewGenerator()

seo_analyzer, preview_generator = get_analyzers()

# Main title and description
st.title("🔍 SEO Meta Tag Analyzer")
st.markdown("""
Analyze any website's SEO meta tags and see how they appear in Google search results and social media platforms.
Get actionable feedback to improve your SEO implementation.
""")

# URL input section
st.header("Website Analysis")
url_input = st.text_input(
    "Enter website URL to analyze:",
    placeholder="example.com",
    help="Enter any website URL (protocol will be added automatically)"
)

analyze_button = st.button("Analyze Website", type="primary")

if analyze_button and url_input:
    # Auto-add protocol if missing
    if not url_input.startswith(('http://', 'https://')):
        url_input = 'https://' + url_input
    
    # Validate URL
    if not validators.url(url_input):
        st.error("❌ Please enter a valid URL (e.g., example.com or https://example.com)")
    else:
        # Show loading spinner
        with st.spinner("Fetching and analyzing website..."):
            try:
                # Analyze the website
                analysis_result = seo_analyzer.analyze_website(url_input)
                
                if analysis_result["success"]:
                    st.success(f"✅ Successfully analyzed: {analysis_result['final_url']}")
                    
                    # Store results in session state
                    st.session_state.analysis_result = analysis_result
                    st.session_state.analyzed_url = url_input
                    
                else:
                    st.error(f"❌ Error analyzing website: {analysis_result['error']}")
                    
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

# Display results if available
if hasattr(st.session_state, 'analysis_result') and st.session_state.analysis_result["success"]:
    result = st.session_state.analysis_result
    meta_tags = result["meta_tags"]
    
    # Google Search Preview
    st.header("🔍 Google Search Preview")
    preview_generator.render_google_preview(meta_tags, result["final_url"])
    
    # SEO Validation
    st.header("📊 SEO Validation")
    validation_results = seo_analyzer.validate_seo(meta_tags)
    
    # Centered SEO Score
    score = validation_results["score"]
    if score >= 80:
        score_color = "#28a745"
        score_emoji = "🟢"
        score_text = "Excellent"
    elif score >= 60:
        score_color = "#ffc107"
        score_emoji = "🟡"
        score_text = "Good"
    else:
        score_color = "#dc3545"
        score_emoji = "🔴"
        score_text = "Needs Improvement"
    
    st.markdown(f"""
    <div class="seo-score-container">
        <div class="seo-score">
            <h2>{score}/100</h2>
            <p>{score_emoji} {score_text}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Issues section
    if validation_results["issues"]:
        st.subheader("⚠️ Issues Found")
        for issue in validation_results["issues"]:
            st.markdown(f"""
            <div class="issue-item">
                • {issue}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No major issues found!")
    
    # Recommendations
    if validation_results["recommendations"]:
        st.subheader("💡 Recommendations")
        for recommendation in validation_results["recommendations"]:
            st.markdown(f"""
            <div class="recommendation-item">
                💡 {recommendation}
            </div>
            """, unsafe_allow_html=True)
    
    # Social Media Previews
    st.header("📱 Social Media Previews")
    
    # Create tabs for different platforms
    tab1, tab2, tab3 = st.tabs(["Facebook", "Twitter", "LinkedIn"])
    
    with tab1:
        preview_generator.render_facebook_preview(meta_tags, result["final_url"])
    
    with tab2:
        preview_generator.render_twitter_preview(meta_tags, result["final_url"])
    
    with tab3:
        preview_generator.render_linkedin_preview(meta_tags, result["final_url"])
    
    # Detailed Meta Tags Analysis
    st.header("🏷️ Detailed Meta Tags")
    
    # Basic Meta Tags
    with st.expander("📄 Basic Meta Tags", expanded=True):
        # Title section
        st.subheader("📝 Title Tag")
        if meta_tags.get("title"):
            st.markdown(f"""
            <div class="meta-tag-item">
                <div style="font-family: monospace; background: #e9ecef; padding: 0.5rem; border-radius: 4px; margin: 0.5rem 0;">
                    {meta_tags["title"]}
                </div>
                <small>Length: {len(meta_tags['title'])} characters</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ No title tag found")
        
        # Description section
        st.subheader("📄 Meta Description")
        if meta_tags.get("description"):
            st.markdown(f"""
            <div class="meta-tag-item">
                <div style="font-family: monospace; background: #e9ecef; padding: 0.5rem; border-radius: 4px; margin: 0.5rem 0;">
                    {meta_tags["description"]}
                </div>
                <small>Length: {len(meta_tags['description'])} characters</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ No description meta tag found")
        
        # Keywords section
        if meta_tags.get("keywords"):
            st.subheader("🔍 Keywords")
            st.markdown(f"""
            <div class="meta-tag-item">
                <div style="font-family: monospace; background: #e9ecef; padding: 0.5rem; border-radius: 4px; margin: 0.5rem 0;">
                    {meta_tags["keywords"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Open Graph Tags
    og_tags = {k: v for k, v in meta_tags.items() if k.startswith("og:")}
    if og_tags:
        with st.expander("📊 Open Graph Tags"):
            for tag, value in og_tags.items():
                st.write(f"**{tag}:** {value}")
    
    # Twitter Card Tags
    twitter_tags = {k: v for k, v in meta_tags.items() if k.startswith("twitter:")}
    if twitter_tags:
        with st.expander("🐦 Twitter Card Tags"):
            for tag, value in twitter_tags.items():
                st.write(f"**{tag}:** {value}")
    
    # Technical Meta Tags
    technical_tags = {}
    for tag in ["robots", "canonical", "author", "viewport", "charset"]:
        if meta_tags.get(tag):
            technical_tags[tag] = meta_tags[tag]
    
    if technical_tags:
        with st.expander("⚙️ Technical Meta Tags"):
            for tag, value in technical_tags.items():
                st.write(f"**{tag}:** {value}")

# Footer
st.markdown("""
<div class="footer">
    <p>SEO Meta Tag Analyzer - Improve your website's search engine optimization</p>
</div>
""", unsafe_allow_html=True)
