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
    placeholder="https://example.com",
    help="Enter a complete URL including http:// or https://"
)

analyze_button = st.button("Analyze Website", type="primary")

if analyze_button and url_input:
    # Validate URL
    if not validators.url(url_input):
        st.error("❌ Please enter a valid URL (e.g., https://example.com)")
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
    
    # Create columns for score and issues
    col1, col2 = st.columns([1, 2])
    
    with col1:
        score = validation_results["score"]
        if score >= 80:
            st.success(f"**SEO Score: {score}/100** 🟢")
        elif score >= 60:
            st.warning(f"**SEO Score: {score}/100** 🟡")
        else:
            st.error(f"**SEO Score: {score}/100** 🔴")
    
    with col2:
        st.write("**Issues Found:**")
        if validation_results["issues"]:
            for issue in validation_results["issues"]:
                st.write(f"• {issue}")
        else:
            st.write("✅ No major issues found!")
    
    # Recommendations
    if validation_results["recommendations"]:
        st.subheader("💡 Recommendations")
        for recommendation in validation_results["recommendations"]:
            st.info(recommendation)
    
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
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Title")
            if meta_tags.get("title"):
                st.code(meta_tags["title"])
                st.caption(f"Length: {len(meta_tags['title'])} characters")
            else:
                st.error("❌ No title tag found")
        
        with col2:
            st.subheader("Description")
            if meta_tags.get("description"):
                st.code(meta_tags["description"])
                st.caption(f"Length: {len(meta_tags['description'])} characters")
            else:
                st.error("❌ No description meta tag found")
        
        if meta_tags.get("keywords"):
            st.subheader("Keywords")
            st.code(meta_tags["keywords"])
    
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
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>SEO Meta Tag Analyzer - Improve your website's search engine optimization</p>
</div>
""", unsafe_allow_html=True)
