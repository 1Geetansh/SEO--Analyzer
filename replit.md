# SEO Meta Tag Analyzer

## Overview

The SEO Meta Tag Analyzer is a Streamlit-based web application that analyzes websites for SEO optimization. It fetches and examines meta tags from any given URL, providing insights into how the website appears in Google search results and social media platforms. The tool offers actionable feedback to help users improve their SEO implementation by analyzing title tags, descriptions, Open Graph tags, and other critical SEO elements.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - chosen for rapid prototyping and easy deployment of data-driven web applications
- **Layout**: Wide layout with collapsed sidebar for maximum content visibility
- **UI Components**: Text input for URL entry, buttons for analysis triggers, and custom HTML rendering for preview displays
- **State Management**: Streamlit's built-in session state and caching mechanisms

### Backend Architecture
- **Core Components**:
  - `SEOAnalyzer` class: Handles web scraping, HTML parsing, and meta tag extraction
  - `PreviewGenerator` class: Renders visual previews of how content appears on different platforms
- **Web Scraping**: Uses requests library with custom headers to mimic browser behavior and avoid blocking
- **HTML Parsing**: BeautifulSoup for reliable HTML parsing and meta tag extraction
- **Caching Strategy**: Streamlit's `@st.cache_resource` decorator for analyzer instances to improve performance

### Data Processing Pipeline
1. **URL Validation**: Uses validators library to ensure proper URL format
2. **Web Fetching**: HTTP requests with error handling and timeout protection
3. **Content Parsing**: Extraction of title, description, Open Graph, and other meta tags
4. **Preview Generation**: Real-time rendering of Google search and social media previews
5. **Analysis Feedback**: Character count validation and SEO recommendations

### Error Handling and Validation
- **Input Validation**: URL format validation before processing
- **Network Error Handling**: Comprehensive exception handling for various request failures
- **Graceful Degradation**: Fallback displays when meta tags are missing or incomplete

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for the user interface
- **BeautifulSoup4**: HTML parsing and meta tag extraction
- **Requests**: HTTP client for fetching web pages
- **Validators**: URL validation functionality

### Web Standards and Protocols
- **HTTP/HTTPS**: Standard web protocols for fetching website content
- **HTML Meta Tags**: Standard meta tag specifications including Open Graph and Twitter Cards
- **User-Agent Simulation**: Mimics browser behavior to avoid bot detection

### Platform Integrations
- **Google Search Preview**: Simulates Google search result appearance
- **Facebook/Open Graph**: Renders social media sharing previews
- **Character Limits**: Implements platform-specific character limitations for optimal display

The application follows a modular design pattern with clear separation of concerns between analysis logic, preview generation, and user interface components.