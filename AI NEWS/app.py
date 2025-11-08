# app.py - Flask Backend for AI News Hub
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='.')

# Configure CORS - Allow all origins for development
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Get API keys from environment variables
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

NEWS_API_BASE = 'https://newsapi.org/v2'

# Initialize Gemini AI
gemini_model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # List available models to find the right one
        print("\n🔍 Checking available Gemini models...")
        available_models = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
                    print(f"   ✓ Found: {m.name}")
        except Exception as e:
            print(f"   ⚠️  Could not list models: {e}")
        
        # Try models in order of preference
        model_names_to_try = [
            'gemini-1.5-flash-latest',
            'gemini-1.5-flash',
            'gemini-1.5-pro-latest',
            'gemini-1.5-pro',
            'gemini-pro',
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.5-flash',
            'models/gemini-pro'
        ]
        
        # Add any models we found from the list
        model_names_to_try.extend(available_models)
        
        model_initialized = False
        for model_name in model_names_to_try:
            try:
                gemini_model = genai.GenerativeModel(model_name)
                # Test the model with a simple request
                test_response = gemini_model.generate_content("Say 'OK'")
                if test_response.text:
                    print(f"✓ Gemini AI initialized successfully with model: {model_name}")
                    model_initialized = True
                    break
            except Exception as e:
                continue
        
        if not model_initialized:
            print("❌ Could not initialize any Gemini model")
            print("   Available models:", available_models if available_models else "None found")
            gemini_model = None
            
    except Exception as e:
        print(f"⚠️  Gemini AI initialization failed: {e}")

# Demo articles for when API key is not available
def get_demo_articles():
    """Generate demo articles with current timestamps"""
    from datetime import datetime, timedelta
    import random
    
    now = datetime.utcnow()
    
    demo_data = [
        {
            'source': {'name': 'Tech Daily'},
            'title': 'Revolutionary AI System Achieves Human-Level Reasoning',
            'description': 'Scientists announce breakthrough in artificial intelligence that enables machines to solve complex problems with human-like reasoning capabilities.',
            'url': 'https://example.com/ai-breakthrough',
            'publishedAt': (now - timedelta(hours=random.randint(1, 5))).isoformat() + 'Z',
            'urlToImage': None
        },
        {
            'source': {'name': 'Global News Network'},
            'title': 'Sustainable Energy Solutions Transform Power Generation',
            'description': 'New renewable energy technology promises to revolutionize how we generate and store electricity, making clean energy more accessible.',
            'url': 'https://example.com/energy-solutions',
            'publishedAt': (now - timedelta(hours=random.randint(6, 12))).isoformat() + 'Z',
            'urlToImage': None
        },
        {
            'source': {'name': 'Innovation Weekly'},
            'title': 'Quantum Computing Reaches Commercial Milestone',
            'description': 'Major tech companies announce quantum computers are now available for enterprise applications, marking a new era in computing.',
            'url': 'https://example.com/quantum-computing',
            'publishedAt': (now - timedelta(hours=random.randint(13, 24))).isoformat() + 'Z',
            'urlToImage': None
        },
        {
            'source': {'name': 'Health Monitor'},
            'title': 'Medical AI Improves Early Disease Detection',
            'description': 'New artificial intelligence tools help doctors identify diseases earlier and with greater accuracy, improving patient outcomes.',
            'url': 'https://example.com/medical-ai',
            'publishedAt': (now - timedelta(hours=random.randint(25, 36))).isoformat() + 'Z',
            'urlToImage': None
        },
        {
            'source': {'name': 'Space Gazette'},
            'title': 'Mars Colony Project Enters New Phase',
            'description': 'International space agencies collaborate on ambitious plan to establish permanent human settlement on Mars by 2030.',
            'url': 'https://example.com/mars-colony',
            'publishedAt': (now - timedelta(hours=random.randint(37, 48))).isoformat() + 'Z',
            'urlToImage': None
        },
        {
            'source': {'name': 'Business Insider'},
            'title': 'Digital Currency Adoption Accelerates Globally',
            'description': 'Central banks worldwide move forward with digital currency initiatives as adoption rates surge across major economies.',
            'url': 'https://example.com/digital-currency',
            'publishedAt': (now - timedelta(hours=random.randint(49, 72))).isoformat() + 'Z',
            'urlToImage': None
        }
    ]
    
    return demo_data


# ============= SERVE HTML =============

@app.route('/')
def serve_html():
    """Serve the main HTML file"""
    try:
        return send_from_directory('.', 'index.html')
    except Exception as e:
        return jsonify({'error': 'index.html not found', 'message': str(e)}), 404

@app.route('/index.html')
def serve_index():
    """Alternative route for index.html"""
    return serve_html()


# ============= NEWS ENDPOINTS =============

@app.route('/api/trending', methods=['GET', 'OPTIONS'])
def get_trending():
    """Get trending news by category"""
    if request.method == 'OPTIONS':
        return '', 204
        
    category = request.args.get('category', 'general')
    
    if not NEWS_API_KEY:
        print(f"⚠️  WARNING: No News API key - Using demo data for category: {category}")
        print(f"   To get real news, add NEWS_API_KEY to your .env file")
        print(f"   Get your free key at: https://newsapi.org/register")
        
        demo_articles = get_demo_articles()
        print(f"   Generated {len(demo_articles)} demo articles with current timestamps")
        print(f"   Latest article date: {demo_articles[0]['publishedAt']}")
        
        return jsonify({
            'status': 'ok',
            'totalResults': len(demo_articles),
            'articles': demo_articles,
            'note': 'DEMO DATA - Add NEWS_API_KEY to .env for real news'
        })
    
    try:
        url = f"{NEWS_API_BASE}/top-headlines"
        params = {
            'category': category,
            'language': 'en',
            'pageSize': 20,
            'apiKey': NEWS_API_KEY
        }
        
        print(f"📡 Fetching REAL news from News API for category: {category}")
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            print(f"✓ Retrieved {len(data.get('articles', []))} REAL articles from News API")
            return jsonify(data)
        else:
            print(f"❌ News API error: {data.get('message', 'Unknown error')}")
            print(f"   Status code: {response.status_code}")
            if response.status_code == 401:
                print(f"   ERROR: Invalid API key! Check your NEWS_API_KEY in .env")
            elif response.status_code == 429:
                print(f"   ERROR: Rate limit exceeded. Using demo data as fallback.")
                return jsonify({
                    'status': 'ok',
                    'articles': get_demo_articles(),
                    'note': 'Rate limit exceeded - showing demo data'
                })
            return jsonify({'error': data.get('message', 'Failed to fetch news')}), response.status_code
            
    except Exception as e:
        print(f"❌ Error fetching news: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/search', methods=['POST', 'OPTIONS'])
def search_news():
    """Search news by query"""
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    if not NEWS_API_KEY:
        print(f"⚠️  WARNING: No News API key - Using demo data for search: {query}")
        return jsonify({
            'status': 'ok',
            'totalResults': len(get_demo_articles()),
            'articles': get_demo_articles(),
            'note': 'DEMO DATA - Add NEWS_API_KEY to .env for real search'
        })
    
    try:
        url = f"{NEWS_API_BASE}/everything"
        params = {
            'q': query,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 20,
            'apiKey': NEWS_API_KEY
        }
        
        print(f"🔍 Searching REAL news for: {query}")
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            print(f"✓ Found {len(data.get('articles', []))} REAL articles")
            return jsonify(data)
        else:
            print(f"❌ Search error: {data.get('message', 'Unknown error')}")
            return jsonify({'error': data.get('message', 'Search failed')}), response.status_code
            
    except Exception as e:
        print(f"❌ Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============= AI SUMMARIZATION ENDPOINTS =============

@app.route('/api/summarize', methods=['POST', 'OPTIONS'])
def summarize_article():
    """Summarize article using Gemini AI"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.get_json()
        print(f"\n📝 Summarize request received")
        print(f"   Data received: {bool(data)}")
        
        if not data:
            print("❌ No JSON data received")
            return jsonify({'error': 'No data received'}), 400
            
        text = data.get('text', '')
        print(f"   Text length: {len(text)} characters")
        
        if not text:
            print("❌ No text provided")
            return jsonify({'error': 'Text is required'}), 400
        
        if not gemini_model:
            print("⚠️  Gemini AI not configured, returning demo response")
            return jsonify({
                'summary': 'This is a demo summary. To get real AI-powered summaries, please configure your Gemini API key in the .env file. Visit https://makersuite.google.com/app/apikey to get your free API key.',
                'ai_model': 'Demo Mode',
                'note': 'Gemini API key not configured'
            }), 200
        
        prompt = f"""Please provide a concise and informative summary of the following article. 
        Include the main points and key takeaways in 3-4 sentences.
        
        Article:
        {text[:3000]}
        
        Summary:"""
        
        print("✨ Generating AI summary with Gemini...")
        
        # Configure generation settings for better results
        generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            top_p=0.8,
            top_k=40,
            max_output_tokens=500,
        )
        
        # Add safety settings to avoid blocks
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
        
        response = gemini_model.generate_content(
            prompt,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Check if response was blocked
        if not response.text:
            if response.prompt_feedback:
                print(f"⚠️  Response blocked: {response.prompt_feedback}")
            return jsonify({
                'error': 'Content generation was blocked by safety filters',
                'summary': 'Unable to generate summary for this content.'
            }), 200
        
        summary = response.text
        
        print(f"✓ Summary generated successfully ({len(summary)} characters)")
        return jsonify({
            'summary': summary,
            'original_length': len(text),
            'summary_length': len(summary),
            'ai_model': 'Gemini Pro'
        })
        
    except Exception as e:
        print(f"❌ Gemini AI error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'AI summarization failed: {str(e)}',
            'details': 'Check server logs for more information'
        }), 500

@app.route('/api/extract-url', methods=['POST', 'OPTIONS'])
def extract_from_url():
    """Extract article content from URL and summarize"""
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json()
    url = data.get('url', '')
    summarize = data.get('summarize', True)
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"🔗 Extracting content from: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        # Get title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else 'No title found'
        
        # Extract main content
        article_content = ''
        
        # Try common article containers
        for selector in ['article', 'main', '[role="main"]', '.article-content', '.post-content', '.entry-content']:
            content = soup.select_one(selector)
            if content:
                article_content = content.get_text(separator=' ', strip=True)
                break
        
        # Fallback to paragraphs
        if not article_content:
            paragraphs = soup.find_all('p')
            article_content = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        
        # Clean up whitespace
        article_content = ' '.join(article_content.split())
        
        print(f"✓ Extracted {len(article_content)} characters")
        
        result = {
            'url': url,
            'title': title_text,
            'content': article_content[:5000],
            'content_length': len(article_content)
        }
        
        # Generate AI summary if requested
        if summarize and article_content and gemini_model:
            try:
                prompt = f"""Please provide a comprehensive summary of this article:
                
                Title: {title_text}
                
                Content:
                {article_content[:3000]}
                
                Provide a summary that includes:
                1. Main topic and key points
                2. Important facts or findings
                3. Conclusions or implications
                
                Keep it concise (3-5 sentences).
                
                Summary:"""
                
                print("✨ Generating AI summary for extracted content...")
                
                generation_config = {
                    'temperature': 0.7,
                    'top_p': 0.8,
                    'top_k': 40,
                    'max_output_tokens': 800,
                }
                
                summary_response = gemini_model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                result['summary'] = summary_response.text
                result['ai_model'] = 'Gemini 1.5'
                print("✓ Summary generated successfully")
                
            except Exception as e:
                print(f"⚠️  Summary generation failed: {str(e)}")
                result['summary'] = "Summary generation unavailable. Please configure Gemini API key."
        elif summarize and not gemini_model:
            result['summary'] = "AI summarization unavailable. Please configure Gemini API key in .env file."
        
        return jsonify(result)
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch URL: {str(e)}")
        return jsonify({'error': f'Failed to fetch URL: {str(e)}'}), 500
    except Exception as e:
        print(f"❌ Error processing URL: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============= HEALTH CHECK =============

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check API health and configuration status"""
    status = {
        'status': 'healthy',
        'news_api_configured': bool(NEWS_API_KEY),
        'gemini_ai_configured': bool(gemini_model),
        'server_time': __import__('datetime').datetime.now().isoformat(),
        'endpoints': {
            'trending': '/api/trending?category=general',
            'search': '/api/search (POST)',
            'summarize': '/api/summarize (POST)',
            'extract_url': '/api/extract-url (POST)'
        }
    }
    
    print("🏥 Health check requested")
    print(f"   News API: {'✓ Configured' if NEWS_API_KEY else '✗ Not configured (using demo data)'}")
    print(f"   Gemini AI: {'✓ Configured' if gemini_model else '✗ Not configured'}")
    
    return jsonify(status)

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to verify server is running"""
    return jsonify({
        'status': 'success',
        'message': 'Server is running correctly!',
        'timestamp': __import__('datetime').datetime.now().isoformat()
    })


# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with detailed information"""
    return jsonify({
        'error': 'Endpoint not found',
        'path': request.path,
        'method': request.method,
        'available_endpoints': {
            'GET /': 'Serve HTML interface',
            'GET /api/health': 'Health check',
            'GET /api/trending?category=general': 'Get trending news',
            'POST /api/search': 'Search news',
            'POST /api/summarize': 'Summarize text',
            'POST /api/extract-url': 'Extract & summarize URL'
        }
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'details': str(error)}), 500

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'error': 'Method not allowed',
        'path': request.path,
        'method': request.method,
        'allowed_methods': 'Check endpoint documentation'
    }), 405


# ============= RUN SERVER =============

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 AI NEWS HUB - BACKEND SERVER")
    print("="*70)
    
    print("\n📋 Configuration Status:")
    print("-" * 70)
    
    if NEWS_API_KEY:
        print("✓ News API: Configured (Real data enabled)")
    else:
        print("⚠️  News API: Not configured")
        print("   Using demo data. Get your free API key at: https://newsapi.org")
    
    if GEMINI_API_KEY and gemini_model:
        print("✓ Gemini AI: Configured (AI summaries enabled)")
    else:
        print("⚠️  Gemini AI: Not configured")
        print("   AI features disabled. Get API key at: https://makersuite.google.com/app/apikey")
    
    print("-" * 70)
    print("\n🌐 Server Information:")
    print(f"   Local:    http://localhost:5000")
    print(f"   Network:  http://0.0.0.0:5000")
    print("\n📝 Available Endpoints:")
    print("   GET  /                     - Serve HTML interface")
    print("   GET  /api/health           - Health check")
    print("   GET  /api/trending         - Get trending news")
    print("   POST /api/search           - Search news")
    print("   POST /api/summarize        - Summarize text")
    print("   POST /api/extract-url      - Extract & summarize URL")
    
    print("\n💡 Quick Start:")
    print("   1. Open your browser")
    print("   2. Go to http://localhost:5000")
    print("   3. Start exploring news!")
    
    print("\n" + "="*70)
    print("Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )