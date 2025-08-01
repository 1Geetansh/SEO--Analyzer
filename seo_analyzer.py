import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import validators

class SEOAnalyzer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def analyze_website(self, url):
        """
        Analyze a website's SEO meta tags
        """
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Fetch the webpage
            response = requests.get(url, headers=self.headers, timeout=10, allow_redirects=True)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract meta tags
            meta_tags = self._extract_meta_tags(soup)
            
            return {
                "success": True,
                "final_url": response.url,
                "status_code": response.status_code,
                "meta_tags": meta_tags,
                "error": None
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}",
                "meta_tags": {},
                "final_url": None,
                "status_code": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Analysis error: {str(e)}",
                "meta_tags": {},
                "final_url": None,
                "status_code": None
            }
    
    def _extract_meta_tags(self, soup):
        """
        Extract all relevant meta tags from HTML
        """
        meta_tags = {}
        
        # Title tag
        title_tag = soup.find('title')
        if title_tag:
            meta_tags['title'] = title_tag.get_text().strip()
        
        # Meta tags
        meta_elements = soup.find_all('meta')
        
        for meta in meta_elements:
            # Standard meta tags
            if meta.get('name'):
                name = meta.get('name').lower()
                content = meta.get('content', '').strip()
                if content:
                    meta_tags[name] = content
            
            # Property meta tags (Open Graph, etc.)
            elif meta.get('property'):
                property_name = meta.get('property').lower()
                content = meta.get('content', '').strip()
                if content:
                    meta_tags[property_name] = content
            
            # HTTP-equiv meta tags
            elif meta.get('http-equiv'):
                http_equiv = meta.get('http-equiv').lower()
                content = meta.get('content', '').strip()
                if content:
                    meta_tags[f"http-equiv-{http_equiv}"] = content
            
            # Charset
            elif meta.get('charset'):
                meta_tags['charset'] = meta.get('charset')
        
        # Canonical URL
        canonical = soup.find('link', rel='canonical')
        if canonical and canonical.get('href'):
            meta_tags['canonical'] = canonical.get('href')
        
        # H1 tags
        h1_tags = soup.find_all('h1')
        if h1_tags:
            meta_tags['h1_tags'] = [h1.get_text().strip() for h1 in h1_tags[:3]]  # First 3 H1s
        
        return meta_tags
    
    def validate_seo(self, meta_tags):
        """
        Validate SEO implementation and provide recommendations with category breakdown
        """
        issues = []
        recommendations = []
        score = 100
        
        # Category scores
        basic_meta_score = 100
        social_media_score = 100
        technical_seo_score = 100
        content_structure_score = 100
        
        # BASIC META TAGS VALIDATION
        title = meta_tags.get('title', '')
        if not title:
            issues.append("Missing title tag")
            basic_meta_score -= 50
            score -= 25
        else:
            if len(title) < 30:
                issues.append("Title is too short (< 30 characters)")
                recommendations.append("Consider expanding your title to 50-60 characters for optimal search visibility")
                basic_meta_score -= 20
                score -= 10
            elif len(title) > 60:
                issues.append("Title is too long (> 60 characters) - may be truncated in search results")
                recommendations.append("Shorten your title to 50-60 characters to prevent truncation")
                basic_meta_score -= 10
                score -= 5
        
        description = meta_tags.get('description', '')
        if not description:
            issues.append("Missing meta description")
            basic_meta_score -= 50
            score -= 20
        else:
            if len(description) < 120:
                issues.append("Meta description is too short (< 120 characters)")
                recommendations.append("Expand your meta description to 150-160 characters for better search snippets")
                basic_meta_score -= 20
                score -= 10
            elif len(description) > 160:
                issues.append("Meta description is too long (> 160 characters) - may be truncated")
                recommendations.append("Shorten your meta description to 150-160 characters")
                basic_meta_score -= 10
                score -= 5
        
        # SOCIAL MEDIA VALIDATION
        og_title = meta_tags.get('og:title')
        og_description = meta_tags.get('og:description')
        og_image = meta_tags.get('og:image')
        
        if not og_title:
            issues.append("Missing Open Graph title (og:title)")
            recommendations.append("Add og:title meta tag for better social media sharing")
            social_media_score -= 20
            score -= 5
        
        if not og_description:
            issues.append("Missing Open Graph description (og:description)")
            recommendations.append("Add og:description meta tag for social media previews")
            social_media_score -= 20
            score -= 5
        
        if not og_image:
            issues.append("Missing Open Graph image (og:image)")
            recommendations.append("Add og:image meta tag with a high-quality image (1200x630px recommended)")
            social_media_score -= 30
            score -= 5
        
        twitter_card = meta_tags.get('twitter:card')
        if not twitter_card:
            issues.append("Missing Twitter Card type")
            recommendations.append("Add twitter:card meta tag (summary_large_image recommended)")
            social_media_score -= 20
            score -= 5
        
        twitter_title = meta_tags.get('twitter:title')
        twitter_description = meta_tags.get('twitter:description')
        if not twitter_title and not og_title:
            social_media_score -= 10
        
        # TECHNICAL SEO VALIDATION 
        canonical = meta_tags.get('canonical')
        if not canonical:
            recommendations.append("Consider adding a canonical URL to prevent duplicate content issues")
            technical_seo_score -= 15
            score -= 3
        
        robots = meta_tags.get('robots')
        if robots and ('noindex' in robots.lower() or 'nofollow' in robots.lower()):
            issues.append("Page has restrictive robots meta tag")
            recommendations.append("Review robots meta tag - it may prevent search engine indexing")
            technical_seo_score -= 20
        
        viewport = meta_tags.get('viewport')
        if not viewport:
            issues.append("Missing viewport meta tag")
            recommendations.append("Add viewport meta tag for mobile responsiveness")
            technical_seo_score -= 25
            score -= 5
        
        charset = meta_tags.get('charset')
        if not charset:
            technical_seo_score -= 10
        
        # CONTENT STRUCTURE VALIDATION
        h1_tags = meta_tags.get('h1_tags', [])
        if not h1_tags:
            issues.append("No H1 tags found")
            recommendations.append("Add at least one H1 tag to structure your content")
            content_structure_score -= 40
            score -= 5
        elif len(h1_tags) > 1:
            recommendations.append("Multiple H1 tags found - consider using only one H1 per page")
            content_structure_score -= 20
        
        # Check for keywords
        keywords = meta_tags.get('keywords')
        if keywords:
            content_structure_score += 10  # Bonus for having keywords
        
        # Ensure scores don't go below 0 or above 100
        basic_meta_score = max(0, min(100, basic_meta_score))
        social_media_score = max(0, min(100, social_media_score))
        technical_seo_score = max(0, min(100, technical_seo_score))
        content_structure_score = max(0, min(100, content_structure_score))
        score = max(0, score)
        
        return {
            "score": score,
            "issues": issues,
            "recommendations": recommendations,
            "category_scores": {
                "basic_meta": {
                    "score": basic_meta_score,
                    "name": "Basic Meta Tags",
                    "description": "Title, description, and essential meta tags"
                },
                "social_media": {
                    "score": social_media_score,
                    "name": "Social Media",
                    "description": "Open Graph and Twitter Card optimization"
                },
                "technical_seo": {
                    "score": technical_seo_score,
                    "name": "Technical SEO",
                    "description": "Canonical URLs, robots, viewport, and charset"
                },
                "content_structure": {
                    "score": content_structure_score,
                    "name": "Content Structure",
                    "description": "H1 tags, keywords, and content organization"
                }
            }
        }
