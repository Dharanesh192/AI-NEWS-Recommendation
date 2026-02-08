const API_BASE = "";
        let currentCategory = 'general';
        let currentSearchMode = 'trending';

        window.onload = function() {
            console.log('🚀 AI News Hub initialized');
            createFloatingParticles();
            checkBackendConnection();
            loadTrendingNews(currentCategory);
        };

        function createFloatingParticles() {
            const bgElements = document.querySelector('.bg-elements');
            const particleCount = 30;
            
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                
                // Random positioning
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 15 + 's';
                particle.style.animationDuration = (15 + Math.random() * 10) + 's';
                
                // Random size variation
                const size = 2 + Math.random() * 4;
                particle.style.width = size + 'px';
                particle.style.height = size + 'px';
                
                bgElements.appendChild(particle);
            }
            
            console.log('✨ Created ' + particleCount + ' floating particles');
        }

        async function checkBackendConnection() {
            try {
                const response = await fetch(`${API_BASE}/health`);
                const data = await response.json();
                console.log('✓ Backend connected:', data);
                
                if (!data.news_api_configured) {
                    console.warn('⚠️  Using demo data - News API not configured');
                }
                if (!data.gemini_ai_configured) {
                    console.warn('⚠️  AI features limited - Gemini API not configured');
                }
            } catch (error) {
                console.error('❌ Backend connection failed:', error);
                console.error('Make sure the Python backend is running');
                alert('⚠️  Cannot connect to backend server.\n\nPlease make sure:\n1. Python backend is running (python app.py)\n2. Server is on http://localhost:5000');
            }
        }

        function switchSearchTab(mode) {
            currentSearchMode = mode;
            document.querySelectorAll('.search-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');

            const input = document.getElementById('mainSearchInput');
            if (mode === 'url') {
                input.placeholder = 'Paste article URL to get AI summary...';
            } else if (mode === 'search') {
                input.placeholder = 'Search for news topics...';
            } else {
                input.placeholder = 'Search for news, topics, or paste URL...';
            }
        }

        function performSearch() {
            const input = document.getElementById('mainSearchInput').value.trim();
            if (!input) return;

            if (currentSearchMode === 'url' || input.startsWith('http')) {
                summarizeUrl(input);
            } else {
                searchNews(input);
            }
        }

        function selectCategory(category) {
            currentCategory = category;
            document.querySelectorAll('.category-card').forEach(card => {
                card.classList.remove('active');
            });
            event.target.closest('.category-card').classList.add('active');
            loadTrendingNews(category);
        }

        async function loadTrendingNews(category) {
            console.log(`📰 Loading ${category} news...`);
            showLoading(true);
            try {
                // Add cache busting parameter
                const cacheBuster = new Date().getTime();
                const response = await fetch(`${API_BASE}/trending?category=${category}&_=${cacheBuster}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                console.log('=== API RESPONSE ===');
                console.log('Total articles:', data.articles?.length || 0);
                console.log('First article date:', data.articles?.[0]?.publishedAt);
                console.log('Response note:', data.note);
                console.log('==================');
                
                // Check if using demo data
                if (data.note && data.note.includes('DEMO DATA')) {
                    console.warn('⚠️ USING DEMO DATA - Add NEWS_API_KEY to .env for real news');
                    console.warn('Get your free API key at: https://newsapi.org/register');
                    showDemoWarning();
                }
                
                if (data.articles) {
                    displayNews(data.articles);
                } else {
                    console.error('No articles in response:', data);
                }
            } catch (error) {
                console.error('❌ Error loading news:', error);
                alert('Failed to load news. Please check if the backend server is running.');
            } finally {
                showLoading(false);
            }
        }

        function showDemoWarning() {
            const warning = document.createElement('div');
            warning.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(135deg, #d4af37 0%, #ffd700 100%);
                color: #1a1410;
                padding: 15px 25px;
                border-radius: 12px;
                font-weight: 600;
                z-index: 9999;
                box-shadow: 0 5px 20px rgba(212, 175, 55, 0.4);
                animation: slideIn 0.3s ease;
            `;
            warning.innerHTML = '⚠️ Using Demo Data - Add NEWS_API_KEY for real news';
            
            document.body.appendChild(warning);
            
            setTimeout(() => {
                warning.style.opacity = '0';
                warning.style.transition = 'opacity 0.5s';
                setTimeout(() => warning.remove(), 500);
            }, 5000);
        }

        async function searchNews(query) {
            console.log(`🔍 Searching for: ${query}`);
            showLoading(true);
            try {
                const response = await fetch(`${API_BASE}/search`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                console.log(`✓ Found ${data.articles?.length || 0} articles`);
                if (data.articles) {
                    displayNews(data.articles);
                } else {
                    alert('No articles found. Try a different search term.');
                }
            } catch (error) {
                console.error('❌ Search error:', error);
                alert('Search failed. Please try again.');
            } finally {
                showLoading(false);
            }
        }

        async function summarizeUrl(url) {
            showLoading(true);
            try {
                const response = await fetch(`${API_BASE}/extract-url`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url, summarize: true })
                });
                const data = await response.json();
                if (data.summary) {
                    showModal(data.title, data.summary);
                }
            } catch (error) {
                console.error('Error:', error);
            } finally {
                showLoading(false);
            }
        }

        function displayNews(articles) {
            const grid = document.getElementById('newsGrid');
            grid.innerHTML = '';

            const validArticles = articles.filter(a => a.title && a.title !== '[Removed]');
            document.getElementById('articleCount').textContent = validArticles.length;

            validArticles.forEach(article => {
                const card = document.createElement('div');
                card.className = 'news-card';

                const imageUrl = article.urlToImage || `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='220'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23d4af37'/%3E%3Cstop offset='100%25' style='stop-color:%23ffd700'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect fill='url(%23g)' width='400' height='220'/%3E%3Ctext fill='white' x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='sans-serif' font-size='24'%3E📰%3C/text%3E%3C/svg%3E`;

                const dateObj = new Date(article.publishedAt);
                const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
                const date = `${dateObj.getDate().toString().padStart(2, '0')}-${monthNames[dateObj.getMonth()]}-${dateObj.getFullYear()}`;


                const cardTitle = document.createElement('div');
                cardTitle.className = 'news-title';
                cardTitle.textContent = article.title;

                const cardDesc = document.createElement('div');
                cardDesc.className = 'news-description';
                cardDesc.textContent = article.description || 'No description available.';

                const summarizeBtn = document.createElement('button');
                summarizeBtn.className = 'action-btn btn-summarize';
                summarizeBtn.innerHTML = '✨ Summarize';
                summarizeBtn.onclick = function(e) {
                    e.stopPropagation();
                    summarizeArticle(article.title, article.description || '');
                };

                const readBtn = document.createElement('button');
                readBtn.className = 'action-btn btn-read';
                readBtn.innerHTML = '📖 Read More';
                readBtn.onclick = function(e) {
                    e.stopPropagation();
                    window.open(article.url, '_blank');
                };

                card.innerHTML = `
                    <div class="news-image-container">
                        <img src="${imageUrl}" alt="Article" class="news-image" onerror="this.src='${imageUrl}'">
                        <span class="news-category-badge">${currentCategory.toUpperCase()}</span>
                    </div>
                    <div class="news-content">
                        <div class="news-meta">
                            <span class="news-source">📡 ${article.source.name || 'Unknown'}</span>
                            <span>🕐 ${date}</span>
                        </div>
                    </div>
                `;

                const newsContent = card.querySelector('.news-content');
                newsContent.appendChild(cardTitle);
                newsContent.appendChild(cardDesc);

                const actionsDiv = document.createElement('div');
                actionsDiv.className = 'news-actions';
                actionsDiv.appendChild(summarizeBtn);
                actionsDiv.appendChild(readBtn);
                newsContent.appendChild(actionsDiv);

                grid.appendChild(card);
            });
        }

        async function summarizeArticle(title, description) {
            console.log('=== SUMMARIZE REQUEST ===');
            console.log('Title:', title);
            console.log('Description:', description);
            console.log('========================');
            
            if (!title || !description) {
                alert('⚠️ Cannot summarize: Missing article content');
                return;
            }
            
            showLoading(true);
            try {
                const textToSummarize = `${title}\n\n${description}`;
                console.log('Sending to API:', textToSummarize.substring(0, 100) + '...');
                
                const response = await fetch(`${API_BASE}/summarize`, {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ text: textToSummarize })
                });
                
                console.log('Response status:', response.status);
                const data = await response.json();
                console.log('Response data:', data);
                
                if (data.summary) {
                    console.log('✓ Summary received successfully');
                    showModal(title, data.summary);
                } else if (data.demo_summary) {
                    console.log('⚠️ Using demo summary');
                    showModal(title, data.demo_summary + '\n\n⚠️ ' + data.error);
                } else if (data.error) {
                    console.error('API error:', data.error);
                    alert('❌ ' + data.error);
                } else {
                    console.error('Unexpected response:', data);
                    alert('Failed to generate summary. Please check console for details.');
                }
            } catch (error) {
                console.error('❌ Summarization error:', error);
                alert('Network error: ' + error.message + '\n\nMake sure backend is running!');
            } finally {
                showLoading(false);
            }
        }

        function showModal(title, text) {
            document.getElementById('modalTitle').textContent = title;
            document.getElementById('modalText').textContent = text;
            document.getElementById('summaryModal').classList.add('show');
        }

        function closeModal(event) {
            if (!event || event.target.id === 'summaryModal') {
                document.getElementById('summaryModal').classList.remove('show');
            }
        }

        function showLoading(show) {
            document.getElementById('loadingIndicator').style.display = show ? 'block' : 'none';
        }

        document.getElementById('mainSearchInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') performSearch();
        });

        document.addEventListener("DOMContentLoaded", () => {
        loadTrendingNews();
        });

        function loadTrendingNews() {
        fetch("/api/trending?category=general")
            .then(res => res.json())
            .then(data => {
            console.log("Trending News:", data);
            // TODO: render news cards here
            })
            .catch(err => console.error("API error:", err));
        }
