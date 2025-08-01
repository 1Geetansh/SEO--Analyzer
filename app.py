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
    
    /* Summary cards styling */
    .summary-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem 0;
        transition: transform 0.2s ease;
    }
    
    .summary-card:hover {
        transform: translateY(-2px);
    }
    
    /* Category card hover effects */
    .category-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Issue and recommendation cards */
    .issue-card, .recommendation-card {
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .issue-card:hover, .recommendation-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Responsive improvements for small screens */
    @media (max-width: 768px) {
        .category-card {
            height: auto !important;
            min-height: 140px;
        }
        
        .summary-card {
            margin: 0.25rem 0;
        }
        
        .category-card .icon {
            font-size: 1.3rem !important;
        }
        
        .category-card .score {
            font-size: 1.2rem !important;
        }
    }
    
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
        
        .category-card {
            height: auto !important;
            min-height: 100px;
            padding: 0.75rem !important;
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
<div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
    <h4 style="color: #495057; margin-bottom: 1rem;">📚 What does this tool do?</h4>
    <p style="color: #6c757d; margin-bottom: 0.5rem;">• <strong>Analyzes your website's SEO</strong> - Checks if search engines can understand your page properly</p>
    <p style="color: #6c757d; margin-bottom: 0.5rem;">• <strong>Shows Google preview</strong> - See exactly how your page appears in search results</p>
    <p style="color: #6c757d; margin-bottom: 0.5rem;">• <strong>Social media previews</strong> - Check how your page looks when shared on Facebook, Twitter, LinkedIn</p>
    <p style="color: #6c757d; margin-bottom: 0;">• <strong>Easy recommendations</strong> - Get simple tips to improve your page's visibility</p>
</div>
""", unsafe_allow_html=True)

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
    
    # SEO Health Check - More beginner friendly
    st.header("🏥 SEO Health Check")
    st.markdown("""
    <p style="color: #6c757d; margin-bottom: 1rem; text-align: center;">
        <em>Think of this like a health checkup for your website. We'll check how well search engines can find and understand your page.</em>
    </p>
    """, unsafe_allow_html=True)
    
    validation_results = seo_analyzer.validate_seo(meta_tags)
    
    # Overall Score with better explanation
    score = validation_results["score"]
    if score >= 80:
        score_color = "#28a745"
        score_emoji = "🟢"
        score_text = "Excellent"
        score_desc = "Your page is well-optimized for search engines!"
        health_status = "Healthy"
    elif score >= 60:
        score_color = "#ffc107"
        score_emoji = "🟡"
        score_text = "Good"
        score_desc = "Your page is doing well, with room for improvement"
        health_status = "Mostly Healthy"
    else:
        score_color = "#dc3545"
        score_emoji = "🔴"
        score_text = "Needs Work"
        score_desc = "Your page needs some SEO improvements to perform better"
        health_status = "Needs Attention"
    
    st.markdown(f"""
    <div class="seo-score-container">
        <div class="seo-score">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{score_emoji}</div>
            <h2>{score}/100</h2>
            <p style="font-size: 1.1rem; font-weight: 600; margin: 0.5rem 0;">{health_status}</p>
            <p style="font-size: 0.9rem; opacity: 0.9; margin: 0;">{score_desc}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Category Scores with beginner-friendly descriptions
    st.subheader("🎯 What We Checked")
    st.markdown("""
    <p style="color: #6c757d; margin-bottom: 1.5rem; text-align: center;">
        <em>We looked at 4 key areas that help your website show up better in search results and social media</em>
    </p>
    """, unsafe_allow_html=True)
    
    category_scores = validation_results["category_scores"]
    
    # Create 2x2 grid for category scores
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    columns = [col1, col2, col3, col4]
    categories = ["basic_meta", "social_media", "technical_seo", "content_structure"]
    icons = ["📝", "📱", "⚙️", "📄"]
    friendly_names = [
        "Page Basics", "Social Sharing", "Technical Setup", "Content Structure"
    ]
    friendly_descriptions = [
        "Title and description that show in search results",
        "How your page looks when shared on social media",
        "Behind-the-scenes settings for search engines",
        "How well your content is organized"
    ]
    
    for i, (col, category_key, icon, friendly_name, friendly_desc) in enumerate(zip(columns, categories, icons, friendly_names, friendly_descriptions)):
        category = category_scores[category_key]
        cat_score = category["score"]
        
        if cat_score >= 80:
            cat_color = "#28a745"
            cat_status = "Excellent"
            status_emoji = "✅"
        elif cat_score >= 60:
            cat_color = "#ffc107"  
            cat_status = "Good"
            status_emoji = "⚠️"
        else:
            cat_color = "#dc3545"
            cat_status = "Needs Work"
            status_emoji = "❌"
        
        with col:
            st.markdown(f"""
            <div class="category-card" style="background: linear-gradient(135deg, {cat_color}15, {cat_color}05); 
                        border: 2px solid {cat_color}30; 
                        border-radius: 12px; 
                        padding: 1rem; 
                        text-align: center; 
                        margin: 0.5rem 0;
                        height: 160px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        transition: transform 0.2s ease, box-shadow 0.2s ease;
                        cursor: pointer;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-size: 1.4rem; font-weight: bold; color: {cat_color}; margin-bottom: 0.2rem;">{cat_score}%</div>
                <div style="font-size: 0.95rem; font-weight: 600; margin-bottom: 0.3rem; color: #333;">{friendly_name}</div>
                <div style="font-size: 0.75rem; color: #666; line-height: 1.2; margin-bottom: 0.3rem;">{friendly_desc}</div>
                <div style="font-size: 0.85rem; color: {cat_color}; font-weight: 600;">{status_emoji} {cat_status}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Quick Action Summary - More user-friendly
    st.subheader("📋 What Should You Do Next?")
    
    # Count issues by severity
    total_issues = len(validation_results["issues"])
    total_recommendations = len(validation_results["recommendations"])
    
    if total_issues == 0 and total_recommendations == 0:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #d4edda, #c3e6cb); border: 2px solid #28a745; border-radius: 12px; padding: 1.5rem; text-align: center; margin: 1rem 0;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎉</div>
            <h4 style="color: #155724; margin-bottom: 0.5rem;">Congratulations!</h4>
            <p style="color: #155724; margin: 0;">Your page is well-optimized for search engines. Keep up the great work!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Priority Actions
        priority_actions = []
        if total_issues > 0:
            if total_issues == 1:
                priority_actions.append("Fix 1 important issue")
            else:
                priority_actions.append(f"Fix {total_issues} important issues")
        
        if total_recommendations > 0:
            if total_recommendations <= 2:
                priority_actions.append("Consider our suggestions to improve further")
            else:
                priority_actions.append("Review our recommendations for better performance")
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fff3cd, #ffeaa7); border: 2px solid #ffc107; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🎯</div>
            <h4 style="color: #856404; margin-bottom: 1rem;">Your Action Plan</h4>
            <div style="color: #856404;">
                {"<br>".join([f"• {action}" for action in priority_actions])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create summary metrics with better labels
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="summary-card" style="border-left: 4px solid #667eea;">
            <div style="font-size: 1.8rem; font-weight: bold; color: #667eea;">{score}</div>
            <div style="font-size: 0.85rem; color: #666;">Health Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        color = "#dc3545" if total_issues > 3 else "#ffc107" if total_issues > 0 else "#28a745"
        issue_text = "No Issues" if total_issues == 0 else f"{total_issues} Issue{'s' if total_issues != 1 else ''}"
        st.markdown(f"""
        <div class="summary-card" style="border-left: 4px solid {color};">
            <div style="font-size: 1.8rem; font-weight: bold; color: {color};">{total_issues}</div>
            <div style="font-size: 0.85rem; color: #666;">Problems</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        color = "#17a2b8" if total_recommendations > 0 else "#28a745"
        st.markdown(f"""
        <div class="summary-card" style="border-left: 4px solid {color};">
            <div style="font-size: 1.8rem; font-weight: bold; color: {color};">{total_recommendations}</div>
            <div style="font-size: 0.85rem; color: #666;">Tips</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Calculate average category score
        avg_category_score = sum(cat["score"] for cat in category_scores.values()) // 4
        color = "#28a745" if avg_category_score >= 80 else "#ffc107" if avg_category_score >= 60 else "#dc3545"
        st.markdown(f"""
        <div class="summary-card" style="border-left: 4px solid {color};">
            <div style="font-size: 1.8rem; font-weight: bold; color: {color};">{avg_category_score}%</div>
            <div style="font-size: 0.85rem; color: #666;">Average</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Issues section - More beginner friendly
    if validation_results["issues"]:
        st.subheader("🚨 Things to Fix First")
        st.markdown("""
        <p style="color: #6c757d; margin-bottom: 1rem;">
            <em>These issues could prevent people from finding your page in search results</em>
        </p>
        """, unsafe_allow_html=True)
        
        for i, issue in enumerate(validation_results["issues"], 1):
            st.markdown(f"""
            <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 1rem; margin: 0.5rem 0; border-radius: 8px;">
                <div style="display: flex; align-items: flex-start;">
                    <div style="background: #ffc107; color: white; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: bold; margin-right: 0.75rem; flex-shrink: 0;">{i}</div>
                    <div style="color: #856404; line-height: 1.4;">
                        <strong>Issue:</strong> {issue}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #d4edda, #c3e6cb); border: 2px solid #28a745; border-radius: 12px; padding: 1.5rem; text-align: center; margin: 1rem 0;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">✅</div>
            <h4 style="color: #155724; margin-bottom: 0.5rem;">No Critical Issues!</h4>
            <p style="color: #155724; margin: 0;">Your page doesn't have any major problems that would hurt its search ranking.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommendations - More encouraging
    if validation_results["recommendations"]:
        st.subheader("💡 Ways to Make It Even Better")
        st.markdown("""
        <p style="color: #6c757d; margin-bottom: 1rem;">
            <em>These suggestions can help your page perform even better in search results</em>
        </p>
        """, unsafe_allow_html=True)
        
        for i, recommendation in enumerate(validation_results["recommendations"], 1):
            st.markdown(f"""
            <div style="background: #d1ecf1; border-left: 4px solid #17a2b8; padding: 1rem; margin: 0.5rem 0; border-radius: 8px;">
                <div style="display: flex; align-items: flex-start;">
                    <div style="background: #17a2b8; color: white; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: bold; margin-right: 0.75rem; flex-shrink: 0;">💡</div>
                    <div style="color: #0c5460; line-height: 1.4;">
                        <strong>Tip:</strong> {recommendation}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Social Media Previews with explanation
    st.header("📱 How Your Page Looks When Shared")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e3f2fd, #f8f9fa); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <p style="color: #1565c0; margin: 0; text-align: center;">
            <strong>💭 Why this matters:</strong> When people share your page on social media, this is what their friends will see. Good previews get more clicks!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different platforms
    tab1, tab2, tab3 = st.tabs(["📘 Facebook", "🐦 Twitter", "💼 LinkedIn"])
    
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
