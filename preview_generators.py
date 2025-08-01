import streamlit as st
from urllib.parse import urlparse
import re

class PreviewGenerator:
    def render_google_preview(self, meta_tags, url):
        """
        Render Google search result preview
        """
        title = meta_tags.get('title', 'No title')
        description = meta_tags.get('description', 'No description available')
        
        # Truncate title for Google (typically ~60 characters)
        display_title = self._truncate_text(title, 60)
        
        # Truncate description for Google (typically ~160 characters)
        display_description = self._truncate_text(description, 160)
        
        # Extract domain from URL
        domain = urlparse(url).netloc if url else 'example.com'
        
        # Create Google-like preview
        st.markdown(f"""
        <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; margin: 10px 0; background: white;">
            <div style="color: #1a0dab; font-size: 18px; font-weight: normal; margin-bottom: 4px; cursor: pointer;">
                {display_title}
            </div>
            <div style="color: #006621; font-size: 14px; margin-bottom: 4px;">
                {domain}
            </div>
            <div style="color: #545454; font-size: 14px; line-height: 1.4;">
                {display_description}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show character counts
        col1, col2 = st.columns(2)
        with col1:
            title_color = "green" if len(title) <= 60 else "orange" if len(title) <= 70 else "red"
            st.markdown(f"**Title:** <span style='color: {title_color}'>{len(title)}/60 characters</span>", 
                       unsafe_allow_html=True)
        with col2:
            desc_color = "green" if len(description) <= 160 else "orange" if len(description) <= 170 else "red"
            st.markdown(f"**Description:** <span style='color: {desc_color}'>{len(description)}/160 characters</span>", 
                       unsafe_allow_html=True)
    
    def render_facebook_preview(self, meta_tags, url):
        """
        Render Facebook sharing preview
        """
        title = meta_tags.get('og:title', meta_tags.get('title', 'No title'))
        description = meta_tags.get('og:description', meta_tags.get('description', 'No description'))
        image = meta_tags.get('og:image', '')
        site_name = meta_tags.get('og:site_name', urlparse(url).netloc if url else 'Website')
        
        # Truncate for Facebook
        display_title = self._truncate_text(title, 100)
        display_description = self._truncate_text(description, 300)
        
        st.markdown(f"""
        <div style="border: 1px solid #dadde1; border-radius: 8px; overflow: hidden; background: white; max-width: 500px;">
            <div style="height: 200px; background: #f0f2f5; display: flex; align-items: center; justify-content: center; color: #8a8d91;">
                {f'<div style="font-size: 12px;">🖼️ Image: {image[:50]}...</div>' if image else '<div>No Open Graph image</div>'}
            </div>
            <div style="padding: 12px;">
                <div style="color: #8a8d91; font-size: 12px; text-transform: uppercase; margin-bottom: 4px;">
                    {site_name}
                </div>
                <div style="color: #1d2129; font-size: 16px; font-weight: 600; margin-bottom: 4px; line-height: 1.3;">
                    {display_title}
                </div>
                <div style="color: #606770; font-size: 14px; line-height: 1.3;">
                    {display_description}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show recommendations
        if not image:
            st.warning("⚠️ No og:image found. Facebook posts with images get 2.3x more engagement!")
        if not meta_tags.get('og:title'):
            st.info("💡 Consider adding og:title for better Facebook sharing")
    
    def render_twitter_preview(self, meta_tags, url):
        """
        Render Twitter card preview
        """
        card_type = meta_tags.get('twitter:card', 'summary')
        title = meta_tags.get('twitter:title', meta_tags.get('og:title', meta_tags.get('title', 'No title')))
        description = meta_tags.get('twitter:description', 
                                  meta_tags.get('og:description', 
                                              meta_tags.get('description', 'No description')))
        image = meta_tags.get('twitter:image', meta_tags.get('og:image', ''))
        site = meta_tags.get('twitter:site', '@website')
        
        # Truncate for Twitter
        display_title = self._truncate_text(title, 70)
        display_description = self._truncate_text(description, 200)
        
        # Determine card layout
        if card_type == 'summary_large_image':
            image_height = "200px"
        else:
            image_height = "120px"
        
        st.markdown(f"""
        <div style="border: 1px solid #cfd9de; border-radius: 12px; overflow: hidden; background: white; max-width: 500px;">
            <div style="height: {image_height}; background: #f7f9fa; display: flex; align-items: center; justify-content: center; color: #536471;">
                {f'<div style="font-size: 12px;">🖼️ Image: {image[:50]}...</div>' if image else '<div>No Twitter image</div>'}
            </div>
            <div style="padding: 12px;">
                <div style="color: #0f1419; font-size: 15px; font-weight: 700; margin-bottom: 4px; line-height: 1.3;">
                    {display_title}
                </div>
                <div style="color: #536471; font-size: 14px; line-height: 1.3; margin-bottom: 4px;">
                    {display_description}
                </div>
                <div style="color: #536471; font-size: 14px;">
                    🔗 {urlparse(url).netloc if url else 'example.com'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show card type info
        st.info(f"🐦 Card type: {card_type}")
        
        if card_type not in ['summary', 'summary_large_image']:
            st.warning("⚠️ Uncommon card type detected. Consider using 'summary' or 'summary_large_image'")
    
    def render_linkedin_preview(self, meta_tags, url):
        """
        Render LinkedIn sharing preview
        """
        title = meta_tags.get('og:title', meta_tags.get('title', 'No title'))
        description = meta_tags.get('og:description', meta_tags.get('description', 'No description'))
        image = meta_tags.get('og:image', '')
        site_name = meta_tags.get('og:site_name', urlparse(url).netloc if url else 'Website')
        
        # Truncate for LinkedIn
        display_title = self._truncate_text(title, 200)
        display_description = self._truncate_text(description, 300)
        
        st.markdown(f"""
        <div style="border: 1px solid #d0d0d0; border-radius: 2px; overflow: hidden; background: white; max-width: 520px;">
            <div style="height: 272px; background: #f3f2ef; display: flex; align-items: center; justify-content: center; color: #666666;">
                {f'<div style="font-size: 12px;">🖼️ Image: {image[:50]}...</div>' if image else '<div>No Open Graph image</div>'}
            </div>
            <div style="padding: 12px 16px 16px 16px;">
                <div style="color: #000000; font-size: 16px; font-weight: 600; margin-bottom: 4px; line-height: 1.4;">
                    {display_title}
                </div>
                <div style="color: #666666; font-size: 14px; line-height: 1.4; margin-bottom: 8px;">
                    {display_description}
                </div>
                <div style="color: #666666; font-size: 12px;">
                    {site_name}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # LinkedIn recommendations
        if not image:
            st.warning("⚠️ LinkedIn posts with images receive 2x more comments and shares!")
        
        st.info("💡 LinkedIn uses Open Graph tags. Optimize og:title, og:description, and og:image for best results.")
    
    def _truncate_text(self, text, max_length):
        """
        Truncate text with ellipsis if it exceeds max_length
        """
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
