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
        <div class="preview-card" style="border: 1px solid #e0e0e0; padding: 16px; background: white; max-width: 100%;">
            <div style="color: #1a0dab; font-size: 1.1rem; font-weight: normal; margin-bottom: 4px; cursor: pointer; word-wrap: break-word;">
                {display_title}
            </div>
            <div style="color: #006621; font-size: 0.9rem; margin-bottom: 4px;">
                {domain}
            </div>
            <div style="color: #545454; font-size: 0.9rem; line-height: 1.4; word-wrap: break-word;">
                {display_description}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show character counts with responsive design
        title_color = "#28a745" if len(title) <= 60 else "#ffc107" if len(title) <= 70 else "#dc3545"
        desc_color = "#28a745" if len(description) <= 160 else "#ffc107" if len(description) <= 170 else "#dc3545"
        
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <div style="display: flex; flex-wrap: wrap; gap: 1rem; justify-content: space-between;">
                <div><strong>Title:</strong> <span style='color: {title_color}; font-weight: 600;'>{len(title)}/60 characters</span></div>
                <div><strong>Description:</strong> <span style='color: {desc_color}; font-weight: 600;'>{len(description)}/160 characters</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
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
        <div class="preview-card" style="border: 1px solid #dadde1; overflow: hidden; background: white; max-width: 100%; width: 100%;">
            <div style="height: 200px; background: #f0f2f5; display: flex; align-items: center; justify-content: center; color: #8a8d91;">
                {f'<div style="font-size: 0.8rem; text-align: center; padding: 1rem;">🖼️ Image: {image[:50]}...</div>' if image else '<div>No Open Graph image</div>'}
            </div>
            <div style="padding: 12px;">
                <div style="color: #8a8d91; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 4px;">
                    {site_name}
                </div>
                <div style="color: #1d2129; font-size: 1rem; font-weight: 600; margin-bottom: 4px; line-height: 1.3; word-wrap: break-word;">
                    {display_title}
                </div>
                <div style="color: #606770; font-size: 0.9rem; line-height: 1.3; word-wrap: break-word;">
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
        <div class="preview-card" style="border: 1px solid #cfd9de; overflow: hidden; background: white; max-width: 100%; width: 100%;">
            <div style="height: {image_height}; background: #f7f9fa; display: flex; align-items: center; justify-content: center; color: #536471;">
                {f'<div style="font-size: 0.8rem; text-align: center; padding: 1rem;">🖼️ Image: {image[:50]}...</div>' if image else '<div>No Twitter image</div>'}
            </div>
            <div style="padding: 12px;">
                <div style="color: #0f1419; font-size: 0.95rem; font-weight: 700; margin-bottom: 4px; line-height: 1.3; word-wrap: break-word;">
                    {display_title}
                </div>
                <div style="color: #536471; font-size: 0.9rem; line-height: 1.3; margin-bottom: 4px; word-wrap: break-word;">
                    {display_description}
                </div>
                <div style="color: #536471; font-size: 0.85rem;">
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
        <div class="preview-card" style="border: 1px solid #d0d0d0; overflow: hidden; background: white; max-width: 100%; width: 100%;">
            <div style="height: 272px; background: #f3f2ef; display: flex; align-items: center; justify-content: center; color: #666666;">
                {f'<div style="font-size: 0.8rem; text-align: center; padding: 1rem;">🖼️ Image: {image[:50]}...</div>' if image else '<div>No Open Graph image</div>'}
            </div>
            <div style="padding: 12px 16px 16px 16px;">
                <div style="color: #000000; font-size: 1rem; font-weight: 600; margin-bottom: 4px; line-height: 1.4; word-wrap: break-word;">
                    {display_title}
                </div>
                <div style="color: #666666; font-size: 0.9rem; line-height: 1.4; margin-bottom: 8px; word-wrap: break-word;">
                    {display_description}
                </div>
                <div style="color: #666666; font-size: 0.75rem;">
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
