// === Conference App ===

class ConferenceApp {
    constructor() {
        this.data = null;
        this.faq = null;
        this.favorites = this.loadFavorites();
        this.currentRoom = 'all';
        this.apiUsageCount = this.loadApiUsage();
        this.conversationHistory = [];  // Store conversation context
        this.lastFaqAnswer = null;  // Store last FAQ answer for context
        this.init();
    }

    async init() {
        await this.loadData();
        await this.loadFAQ();
        this.autoAddCommonSessions();
        this.setupEventListeners();
        this.renderSchedule();
        this.updateRoomFilter();
    }

    async loadFAQ() {
        try {
            const response = await fetch('data/faq.json');
            this.faq = await response.json();
            console.log(`Loaded ${this.faq.length} FAQ entries`);
        } catch (error) {
            console.error('Error loading FAQ:', error);
            this.faq = [];
        }
    }

    loadApiUsage() {
        const stored = localStorage.getItem('apiUsageCount');
        return stored ? JSON.parse(stored) : { spent: 0.0, date: new Date().toDateString() };
    }

    saveApiUsage() {
        localStorage.setItem('apiUsageCount', JSON.stringify(this.apiUsageCount));
    }

    incrementApiUsage(cost) {
        const today = new Date().toDateString();
        if (this.apiUsageCount.date !== today) {
            // Reset counter for new day
            this.apiUsageCount = { spent: 0.0, date: today };
        }
        this.apiUsageCount.spent += cost;
        this.saveApiUsage();
    }

    autoAddCommonSessions() {
        // Automatically add breaks, lunch, and registration to favorites
        if (!this.data.sessions) return;

        const commonSessionIds = [
            'reg-1',      // Registration
            'break-1',    // Morning break
            'break-2',    // Mid-morning break
            'lunch-1',    // Lunch break
            'break-3',    // Afternoon break
            'break-4'     // Late afternoon break
        ];

        // Add each common session to favorites if it exists and isn't already added
        commonSessionIds.forEach(sessionId => {
            const sessionExists = this.data.sessions.some(s => s.id === sessionId);
            if (sessionExists && !this.favorites.includes(sessionId)) {
                this.favorites.push(sessionId);
            }
        });

        // Save updated favorites
        this.saveFavorites();
        console.log('Auto-added common sessions to My Schedule:', this.favorites.filter(id => commonSessionIds.includes(id)));
    }
    
    async loadData() {
        try {
            const response = await fetch('data/conference.json');
            this.data = await response.json();
            console.log('Data loaded:', this.data);
        } catch (error) {
            console.error('Error loading data:', error);
            // Fallback data
            this.data = { sessions: [], speakers: [], rooms: [] };
        }
    }
    
    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => this.switchTab(tab.dataset.tab));
        });
        
        // Room filter
        document.getElementById('room-filter').addEventListener('change', (e) => {
            this.currentRoom = e.target.value;
            this.renderSchedule();
        });
        
        // Chatbot
        document.getElementById('chat-send').addEventListener('click', () => this.sendChatMessage());
        document.getElementById('chat-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendChatMessage();
        });
        
        // Modal close
        document.querySelector('.modal-close').addEventListener('click', () => {
            document.getElementById('session-modal').classList.remove('active');
        });
        
        document.getElementById('session-modal').addEventListener('click', (e) => {
            if (e.target.id === 'session-modal') {
                document.getElementById('session-modal').classList.remove('active');
            }
        });
    }
    
    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
        document.getElementById(`${tabName}-tab`).classList.add('active');
        
        // Render my schedule if that tab is opened
        if (tabName === 'my-schedule') {
            this.renderMySchedule();
        }
    }
    
    updateRoomFilter() {
        const select = document.getElementById('room-filter');
        select.innerHTML = '<option value="all">All Rooms</option>';

        this.data.rooms.forEach(room => {
            const option = document.createElement('option');
            option.value = room.id;
            option.textContent = room.name;
            select.appendChild(option);
        });
    }
    
    renderSchedule() {
        const container = document.getElementById('schedule-grid');

        if (!this.data.sessions || this.data.sessions.length === 0) {
            container.innerHTML = '<div class="loading">No sessions to display</div>';
            return;
        }

        // Quick sessions IDs (10-minute sessions in Cubido Menuett)
        const quickSessionIds = ['s24', 's25', 's26', 's27', 's28'];

        // Group sessions by time
        const sessionsByTime = {};
        const quickSessions = [];
        this.data.sessions.forEach(session => {
            if (this.currentRoom !== 'all' && session.room_id !== this.currentRoom) {
                return;
            }

            // Separate quick sessions for special handling
            if (quickSessionIds.includes(session.id)) {
                quickSessions.push(session);
                return;
            }

            const timeKey = session.start;
            if (!sessionsByTime[timeKey]) {
                sessionsByTime[timeKey] = [];
            }
            sessionsByTime[timeKey].push(session);
        });

        // Add grouped quick sessions at 12:45 time slot
        if (quickSessions.length > 0 && (this.currentRoom === 'all' || this.currentRoom === 'menuett')) {
            const quickTimeKey = '2026-01-23T12:45:00Z';
            if (!sessionsByTime[quickTimeKey]) {
                sessionsByTime[quickTimeKey] = [];
            }
            // Add as single grouped item
            sessionsByTime[quickTimeKey].push({
                id: 'quick-sessions-group',
                isQuickGroup: true,
                quickSessions: quickSessions.sort((a, b) => a.start.localeCompare(b.start)),
                start: quickTimeKey,
                room: 'Cubido (Menuett)',
                title: 'Quick 10-Minute Sessions'
            });
        }

        // Sort by time
        const sortedTimes = Object.keys(sessionsByTime).sort();

        // Render
        container.innerHTML = '';
        sortedTimes.forEach(time => {
            const timeBlock = document.createElement('div');
            timeBlock.className = 'time-block';

            const sessions = sessionsByTime[time];
            const firstSession = sessions[0];
            const timeStr = this.formatTime(firstSession.start);

            timeBlock.innerHTML = `
                <div class="time-block-header">${timeStr}</div>
                <div class="sessions-row">
                    ${sessions.map(s => this.renderSessionCard(s)).join('')}
                </div>
            `;

            container.appendChild(timeBlock);
        });

        // Add click handlers for regular session cards
        document.querySelectorAll('.session-card:not(.break):not(.quick-sessions-group)').forEach(card => {
            card.addEventListener('click', (e) => {
                if (!e.target.classList.contains('favorite-btn')) {
                    this.showSessionDetail(card.dataset.id);
                }
            });
        });

        // Add click handlers for quick session items
        document.querySelectorAll('.quick-session-item').forEach(item => {
            item.addEventListener('click', (e) => {
                if (!e.target.classList.contains('favorite-btn')) {
                    this.showSessionDetail(item.dataset.id);
                }
            });
        });

        // Add click handlers for favorite buttons
        document.querySelectorAll('.favorite-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleFavorite(btn.dataset.id);
            });
        });
    }
    
    renderSessionCard(session) {
        // Handle quick sessions group
        if (session.isQuickGroup) {
            const quickSessionsHtml = session.quickSessions.map(qs => {
                const isFav = this.favorites.includes(qs.id);
                return `
                    <div class="quick-session-item" data-id="${qs.id}" style="padding: 0.75rem; margin: 0.5rem 0; background: white; border-radius: 6px; border-left: 3px solid var(--primary); cursor: pointer;">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div style="flex: 1;">
                                <div style="font-weight: 600; font-size: 0.9rem; margin-bottom: 0.25rem;">${qs.title}</div>
                                <div style="font-size: 0.8rem; color: #666;">${qs.speakers.join(', ')}</div>
                                <div style="font-size: 0.75rem; color: #999; margin-top: 0.25rem;">${this.formatTime(qs.start)} - ${this.formatTime(qs.end)}</div>
                            </div>
                            <button class="favorite-btn ${isFav ? 'active' : ''}" data-id="${qs.id}" style="margin-left: 0.5rem;">
                                ${isFav ? '⭐' : '☆'}
                            </button>
                        </div>
                    </div>
                `;
            }).join('');

            const startTime = this.formatTime(session.quickSessions[0].start);
            const endTime = this.formatTime(session.quickSessions[session.quickSessions.length - 1].end);

            return `
                <div class="session-card quick-sessions-group" style="background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 100%); border: 2px dashed var(--primary); padding: 1rem;">
                    <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem; color: var(--primary);">
                        ⚡ Quick 10-Minute Sessions (5 talks)
                    </div>
                    <div style="font-size: 0.85rem; color: #666; margin-bottom: 1rem;">
                        ${session.room} • ${startTime} - ${endTime}
                    </div>
                    <div class="quick-sessions-list">
                        ${quickSessionsHtml}
                    </div>
                </div>
            `;
        }

        const isFavorite = this.favorites.includes(session.id);
        const isBreak = session.title.toLowerCase().includes('break') ||
                       session.title.toLowerCase().includes('lunch') ||
                       session.title.toLowerCase().includes('registration');

        if (isBreak) {
            return `
                <div class="session-card break">
                    <div class="session-title">${session.title}</div>
                </div>
            `;
        }

        return `
            <div class="session-card" data-id="${session.id}">
                <button class="favorite-btn ${isFavorite ? 'active' : ''}" data-id="${session.id}">
                    ${isFavorite ? '⭐' : '☆'}
                </button>
                <div class="session-title">${session.title}</div>
                <div class="session-speaker">${session.speakers.join(', ')}</div>
                <div class="session-room">${session.room}</div>
            </div>
        `;
    }
    
    showSessionDetail(sessionId) {
        const session = this.data.sessions.find(s => s.id === sessionId);
        if (!session) return;

        const modal = document.getElementById('session-modal');
        const detail = document.getElementById('session-detail');

        const isFavorite = this.favorites.includes(sessionId);

        // Make speaker names clickable
        const speakerLinks = session.speakers.map(speakerName => {
            return `<a href="#" onclick="app.showSpeakerDetail('${speakerName}'); return false;" style="color: var(--primary); text-decoration: underline; cursor: pointer;">${speakerName}</a>`;
        }).join(', ');

        detail.innerHTML = `
            <h2>${session.title}</h2>
            <p><strong>Speaker(s):</strong> ${speakerLinks}</p>
            <p><strong>Room:</strong> ${session.room}</p>
            <p><strong>Time:</strong> ${this.formatTime(session.start)} - ${this.formatTime(session.end)}</p>

            <div style="margin-top: 1.5rem;">
                <h3 style="margin-bottom: 0.5rem;">Description</h3>
                <p style="line-height: 1.6;">${session.description}</p>
            </div>

            <button
                onclick="app.toggleFavorite('${sessionId}')"
                style="margin-top: 1.5rem; padding: 0.75rem 1.5rem; background: var(--primary); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;"
            >
                ${isFavorite ? '⭐ Remove from favorites' : '☆ Add to favorites'}
            </button>
        `;

        modal.classList.add('active');
        // Force scroll to top - try both modal and body
        setTimeout(() => {
            modal.scrollTop = 0;
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
        }, 10);
    }

    showSpeakerDetail(speakerName) {
        const speaker = this.data.speakers.find(s => s.name === speakerName);
        if (!speaker) return;

        const modal = document.getElementById('session-modal');
        const detail = document.getElementById('session-detail');

        // Find all sessions by this speaker
        const speakerSessions = this.data.sessions.filter(s => s.speakers.includes(speakerName));

        const sessionsHtml = speakerSessions.map(s => {
            return `<li><a href="#" onclick="app.showSessionDetail('${s.id}'); return false;" style="color: var(--primary); text-decoration: underline;">${s.title}</a> at ${this.formatTime(s.start)}</li>`;
        }).join('');

        detail.innerHTML = `
            <h2>${speaker.name}</h2>
            ${speaker.title ? `<p style="font-style: italic; color: #666;">${speaker.title}</p>` : ''}

            ${speaker.bio ? `
                <div style="margin-top: 1.5rem;">
                    <h3 style="margin-bottom: 0.5rem;">About</h3>
                    <p style="line-height: 1.6;">${speaker.bio}</p>
                </div>
            ` : ''}

            <div style="margin-top: 1.5rem;">
                <h3 style="margin-bottom: 0.5rem;">Sessions</h3>
                <ul style="line-height: 1.8;">
                    ${sessionsHtml}
                </ul>
            </div>

            <button
                onclick="document.getElementById('session-modal').classList.remove('active');"
                style="margin-top: 1.5rem; padding: 0.75rem 1.5rem; background: var(--primary); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;"
            >
                Close
            </button>
        `;

        modal.classList.add('active');
        // Force scroll to top - try both modal and body
        setTimeout(() => {
            modal.scrollTop = 0;
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
        }, 10);
    }

    toggleFavorite(sessionId) {
        // Prevent removing common sessions (breaks, lunch, registration)
        const commonSessionIds = ['reg-1', 'break-1', 'break-2', 'lunch-1', 'break-3', 'break-4'];
        const isCommonSession = commonSessionIds.includes(sessionId);

        const index = this.favorites.indexOf(sessionId);
        if (index > -1) {
            // Don't allow removing common sessions
            if (isCommonSession) {
                console.log('Cannot remove common sessions (breaks, lunch, registration)');
                return;
            }
            this.favorites.splice(index, 1);
        } else {
            this.favorites.push(sessionId);
        }

        this.saveFavorites();
        this.renderSchedule();
        this.renderMySchedule();

        // Close and reopen modal to update favorite button
        const modal = document.getElementById('session-modal');
        if (modal.classList.contains('active')) {
            modal.classList.remove('active');
            setTimeout(() => this.showSessionDetail(sessionId), 100);
        }
    }
    
    renderMySchedule() {
        const container = document.getElementById('my-schedule-list');

        if (this.favorites.length === 0) {
            container.innerHTML = '<p class="empty-state">You haven\'t selected any sessions yet. Mark them with a star in the schedule!</p>';
            return;
        }
        
        const favSessions = this.data.sessions
            .filter(s => this.favorites.includes(s.id))
            .sort((a, b) => a.start.localeCompare(b.start));
        
        container.innerHTML = favSessions.map(s => {
            const isCommon = s.title.toLowerCase().includes('break') ||
                           s.title.toLowerCase().includes('lunch') ||
                           s.title.toLowerCase().includes('registration');

            if (isCommon) {
                // Centered layout for breaks/lunch/registration (no star, with time)
                // The dash "-" in time is centered exactly under the center of the title
                const timeStr = `${this.formatTime(s.start)} - ${this.formatTime(s.end)}`;
                const titleLength = s.title.length;
                const timeLength = timeStr.length;

                // Calculate center positions
                const titleCenter = titleLength / 2;
                const timeCenter = timeLength / 2;

                // Calculate padding needed to align centers
                // Using monospace for precise alignment
                return `
                    <div class="session-card break" style="margin: 0 auto 1rem auto; max-width: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                        <div class="session-title" style="font-family: monospace; letter-spacing: 0.05em;">${s.title}</div>
                        <div style="margin-top: 0.5rem; font-size: 0.9rem; opacity: 0.9; font-family: monospace; letter-spacing: 0.05em;">
                            ${timeStr}
                        </div>
                    </div>
                `;
            }

            // Regular session with star
            return `
                <div class="session-card" data-id="${s.id}" style="margin-bottom: 1rem; cursor: pointer;">
                    <button class="favorite-btn active" data-id="${s.id}">⭐</button>
                    <div class="session-title">${s.title}</div>
                    <div class="session-speaker">${s.speakers.join(', ')}</div>
                    <div style="margin-top: 0.5rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                        <div class="session-room">${s.room}</div>
                        <div class="session-room">${this.formatTime(s.start)} - ${this.formatTime(s.end)}</div>
                    </div>
                </div>
            `;
        }).join('');
        
        // Add click handlers only for regular sessions (not breaks)
        container.querySelectorAll('.session-card:not(.break)').forEach(card => {
            card.addEventListener('click', (e) => {
                if (!e.target.classList.contains('favorite-btn')) {
                    this.showSessionDetail(card.dataset.id);
                }
            });
        });
        
        container.querySelectorAll('.favorite-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleFavorite(btn.dataset.id);
            });
        });
    }
    
    async sendChatMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message
        this.addChatMessage(message, 'user');
        input.value = '';
        
        // Disable send button
        const sendBtn = document.getElementById('chat-send');
        sendBtn.disabled = true;
        sendBtn.textContent = 'Thinking...';

        try {
            // Try Claude API first, fallback to rule-based
            const response = await this.getChatbotResponse(message);
            this.addChatMessage(response, 'bot');
        } catch (error) {
            console.error('Chatbot error:', error);
            this.addChatMessage('Sorry, something went wrong. Please try again.', 'bot');
        }

        sendBtn.disabled = false;
        sendBtn.textContent = 'Send';
    }
    
    // Simple fuzzy match - calculates similarity between two strings
    fuzzyMatch(str1, str2) {
        const s1 = str1.toLowerCase();
        const s2 = str2.toLowerCase();

        // Exact match
        if (s1 === s2) return 1.0;

        // One contains the other
        if (s1.includes(s2) || s2.includes(s1)) return 0.8;

        // Calculate Levenshtein distance for similarity
        const longer = s1.length > s2.length ? s1 : s2;
        const shorter = s1.length > s2.length ? s2 : s1;

        if (longer.length === 0) return 1.0;

        // Count matching characters
        let matches = 0;
        for (let i = 0; i < shorter.length; i++) {
            if (longer.includes(shorter[i])) matches++;
        }

        return matches / longer.length;
    }

    searchFAQ(message) {
        if (!this.faq || this.faq.length === 0) return null;

        const messageLower = message.toLowerCase();
        let bestMatches = [];
        let fuzzyMatches = [];

        // If this looks like a follow-up question and we have context, try to use it
        const followUpWords = ['more', 'else', 'about him', 'about her', 'information', 'details', 'více', 'další', 'mehr', 'weitere'];
        const isFollowUp = followUpWords.some(word => messageLower.includes(word));

        if (isFollowUp && this.lastFaqAnswer) {
            // Try to extract names from last answer to search for related info
            const nameMatches = this.lastFaqAnswer.match(/([A-Z][a-z]+ [A-Z][a-z]+)/g);
            if (nameMatches) {
                // Search for speaker info with these names
                for (const name of nameMatches) {
                    for (const faqItem of this.faq) {
                        if (faqItem.category === 'speaker' && faqItem.question.toLowerCase().includes(name.toLowerCase())) {
                            return faqItem.answer;
                        }
                    }
                }
            }
        }

        // Search through FAQ
        for (const faqItem of this.faq) {
            let score = 0;

            // Check if any keywords match exactly
            for (const keyword of faqItem.keywords) {
                if (messageLower.includes(keyword.toLowerCase())) {
                    score += 10;
                }
            }

            // Check if question is similar
            if (messageLower.includes(faqItem.question.toLowerCase().substring(0, 20))) {
                score += 20;
            }

            // Fuzzy matching for speaker names (typos)
            if (faqItem.category === 'speaker') {
                const questionWords = faqItem.question.toLowerCase().split(' ');
                const messageWords = messageLower.split(' ');

                for (const qWord of questionWords) {
                    if (qWord.length > 3) {  // Only check significant words
                        for (const mWord of messageWords) {
                            const similarity = this.fuzzyMatch(qWord, mWord);
                            if (similarity > 0.7 && similarity < 1.0) {
                                // Good fuzzy match - add to suggestions
                                fuzzyMatches.push({
                                    faqItem,
                                    similarity,
                                    matchedWord: qWord,
                                    userWord: mWord
                                });
                            }
                        }
                    }
                }
            }

            if (score > 0) {
                bestMatches.push({ ...faqItem, score });
            }
        }

        // Sort by score
        bestMatches.sort((a, b) => b.score - a.score);

        // If we have fuzzy matches but no exact matches, suggest correction
        if (bestMatches.length === 0 && fuzzyMatches.length > 0) {
            // Sort by similarity
            fuzzyMatches.sort((a, b) => b.similarity - a.similarity);
            const best = fuzzyMatches[0];

            // Extract the speaker name from question "Who is X?"
            const nameMatch = best.faqItem.question.match(/Who is (.+)\?/);
            if (nameMatch) {
                const correctName = nameMatch[1];
                return {
                    isSuggestion: true,
                    suggestion: correctName,
                    message: `Did you mean "${correctName}"?`
                };
            }
        }

        if (bestMatches.length === 0) return null;

        // Check if it's a complex question asking for multiple items
        const isMultiRequest = messageLower.match(/(all|every|each|summarize.*all|všech|všechny|alle)/);

        if (isMultiRequest && bestMatches.length > 1) {
            // Combine multiple answers for complex questions
            console.log(`Combining ${Math.min(bestMatches.length, 10)} FAQ answers`);
            const answers = bestMatches.slice(0, 10).map(m => m.answer).join('\n\n');
            return answers;
        }

        // Only return FAQ if score is high enough (good match)
        // Lower threshold means more false positives
        if (bestMatches[0].score >= 15) {
            return bestMatches[0].answer;
        }

        // Score too low - let API handle it
        return null;
    }

    checkRateLimit() {
        const MAX_SPEND_PER_DAY = 0.20;  // $0.20 per user (~10 API calls = ~100 effective questions with FAQ)
        const CONFERENCE_DATE = new Date('2026-01-23');
        const today = new Date();

        // Set both dates to midnight for accurate comparison
        CONFERENCE_DATE.setHours(0, 0, 0, 0);
        const todayMidnight = new Date(today);
        todayMidnight.setHours(0, 0, 0, 0);

        // Check if conference is over (after January 23, 2026)
        if (todayMidnight > CONFERENCE_DATE) {
            const language = this.detectLanguage('en');
            const messages = {
                en: `Hope you enjoyed the conference! 😴\n\nI'm sleeping now after doing a great job.\n\nYou can still browse the schedule and your favorites!`,
                cs: `Doufám, že jsi si užil konferenci! 😴\n\nTeď spím po skvěle odvedené práci.\n\nStále můžeš prohlížet program a oblíbené!`,
                de: `Ich hoffe, die Konferenz hat dir gefallen! 😴\n\nIch schlafe jetzt nach getaner Arbeit.\n\nDu kannst weiterhin den Zeitplan und Favoriten durchsuchen!`
            };

            return {
                allowed: false,
                message: messages[language] || messages.en
            };
        }

        const todayString = today.toDateString();

        if (this.apiUsageCount.date !== todayString) {
            // New day, reset counter
            this.apiUsageCount = { spent: 0.0, date: todayString };
            this.saveApiUsage();
        }

        if (this.apiUsageCount.spent >= MAX_SPEND_PER_DAY) {
            const language = this.detectLanguage('en');
            const messages = {
                en: `⚠️ Daily AI spending limit reached ($${MAX_SPEND_PER_DAY.toFixed(2)} per day).\n\nThis helps keep costs under control.\n\nYou can still browse the schedule and favorites!\n\nTip: Try rephrasing your question - the FAQ might have the answer!`,
                cs: `⚠️ Denní limit AI nákladů dosažen ($${MAX_SPEND_PER_DAY.toFixed(2)} denně).\n\nToto pomáhá udržet náklady pod kontrolou.\n\nStále můžeš prohlížet program a oblíbené!\n\nTip: Zkus přeformulovat otázku - FAQ možná má odpověď!`,
                de: `⚠️ Tägliches KI-Ausgabenlimit erreicht ($${MAX_SPEND_PER_DAY.toFixed(2)} pro Tag).\n\nDies hilft, die Kosten unter Kontrolle zu halten.\n\nDu kannst weiterhin den Zeitplan und Favoriten durchsuchen!\n\nTipp: Versuche, deine Frage umzuformulieren - die FAQ könnte die Antwort haben!`
            };

            return {
                allowed: false,
                message: messages[language] || messages.en
            };
        }

        return { allowed: true };
    }

    async getChatbotResponse(message) {
        console.log('Getting chatbot response for:', message);

        try {
            // Check if this is a follow-up question about the last FAQ answer
            const followUpKeywords = ['more', 'tell me more', 'any more', 'information', 'else', 'about him', 'about her', 'about them', 'více', 'více informací', 'mehr', 'weitere'];
            const isFollowUp = followUpKeywords.some(keyword => message.toLowerCase().includes(keyword));

            // STEP 1: Try FAQ first (free, instant)
            const faqAnswer = this.searchFAQ(message);

            // Check if FAQ returned a suggestion (fuzzy match)
            if (faqAnswer && faqAnswer.isSuggestion) {
                console.log('💡 Suggesting correction for typo');
                return faqAnswer.message;
            }

            // If this is a follow-up question asking for MORE info, use API instead of FAQ
            if (isFollowUp && (faqAnswer || this.lastFaqAnswer)) {
                console.log('🔄 Follow-up question detected, using API for detailed answer');
                // Don't return FAQ answer, fall through to API call
                // API will have full context and can provide more detailed information
            } else if (faqAnswer) {
                console.log('✅ Answered from FAQ (no API call)');
                this.lastFaqAnswer = faqAnswer;  // Store for context
                return faqAnswer;
            }

            // If follow-up but no context at all
            if (isFollowUp && !this.lastFaqAnswer && !faqAnswer) {
                const language = this.detectLanguage(message);
                const messages = {
                    en: "I need more context. What would you like to know more about?",
                    cs: "Potřebuji více kontextu. O čem chceš vědět více?",
                    de: "Ich brauche mehr Kontext. Worüber möchtest du mehr erfahren?"
                };
                return messages[language] || messages.en;
            }

            // STEP 2: Check rate limit before using API
            const rateLimit = this.checkRateLimit();
            if (!rateLimit.allowed) {
                return rateLimit.message;
            }

            // STEP 3: Use Claude API for complex questions
            console.log('Using Claude API for complex question...');

            // Detect language and prepare context
            const language = this.detectLanguage(message);
            console.log('Detected language:', language);
            const conferenceContext = this.buildConferenceContext(language);

            // Add conversation history context
            let contextPrompt = conferenceContext;
            if (this.lastFaqAnswer) {
                contextPrompt += `\n\nPrevious answer given to user: ${this.lastFaqAnswer}`;
            }

            // Prepare the full prompt
            const fullPrompt = `${contextPrompt}\n\nConference attendee question: ${message}`;

            // Call our backend proxy
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    prompt: fullPrompt,
                    language: language
                })
            });

            console.log('Backend response status:', response.status);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error('Backend error:', response.status, errorData);

                // If backend is not running, show helpful message
                if (response.status === 404 || !response.status) {
                    return this.getBackendErrorMessage(language);
                }

                throw new Error(`Backend error: ${response.status}`);
            }

            const data = await response.json();
            console.log('API response received successfully');

            // Track spending after successful API call
            const cost = data.cost || 0.02;  // Backend sends cost, fallback to estimate
            this.incrementApiUsage(cost);
            console.log(`💰 This call cost: $${cost.toFixed(4)}, Total spent today: $${this.apiUsageCount.spent.toFixed(4)}`);

            return data.content[0].text;

        } catch (error) {
            console.error('Chatbot error:', error);
            console.error('Error type:', error.name);
            console.error('Error message:', error.message);

            // Check if backend is not running (connection refused)
            if (error.message.includes('fetch') || error.name === 'TypeError' || error.message.includes('Failed to fetch')) {
                const language = this.detectLanguage(message);
                return this.getBackendErrorMessage(language);
            }

            // Fallback to rule-based response
            const language = this.detectLanguage(message);
            return this.generateFallbackResponse(message);
        }
    }

    getBackendErrorMessage(language) {
        const messages = {
            en: `⚠️ **Backend Server Not Running**\n\nThe AI chatbot needs a backend server to work.\n\n**To start the server:**\n\`\`\`bash\n# Install dependencies (first time only)\npip install -r requirements.txt\n\n# Start the server\npython server.py\n\`\`\`\n\nThen refresh this page and try again!\n\nFor now, I can answer basic questions. Try:\n• "Which sessions start at 9:15?"\n• "How many speakers?"`,
            cs: `⚠️ **Backend server neběží**\n\nAI chatbot potřebuje backend server.\n\n**Spuštění serveru:**\n\`\`\`bash\n# Nainstaluj závislosti (jen poprvé)\npip install -r requirements.txt\n\n# Spusť server\npython server.py\n\`\`\`\n\nPotom obnov stránku a zkus znovu!\n\nProzatím mohu odpovídat na základní otázky. Zkus:\n• "Které session začínají v 9:15?"\n• "Kolik je speakerů?"`,
            de: `⚠️ **Backend-Server läuft nicht**\n\nDer KI-Chatbot benötigt einen Backend-Server.\n\n**Server starten:**\n\`\`\`bash\n# Abhängigkeiten installieren (nur beim ersten Mal)\npip install -r requirements.txt\n\n# Server starten\npython server.py\n\`\`\`\n\nDann Seite neu laden und erneut versuchen!\n\nVorerst kann ich grundlegende Fragen beantworten. Versuche:\n• "Welche Sessions beginnen um 9:15?"\n• "Wie viele Speaker gibt es?"`
        };
        return messages[language] || messages.en;
    }


    detectLanguage(message) {
        // Simple language detection
        const lower = message.toLowerCase();

        // Czech patterns - expanded
        if (lower.match(/\b(který|která|které|kde|kdy|jak|proč|co|jsem|jsi|jsou|přednáška|místnost|mi|můžeš|odpovíš|udělej|shrň|česky|čeština|přehled|vět)\b/)) {
            console.log('Czech language detected!');
            return 'cs';
        }

        // German patterns
        if (lower.match(/\b(welche|welcher|wo|wann|wie|warum|was|ich|du|sind|vortrag|raum|deutsch)\b/)) {
            console.log('German language detected!');
            return 'de';
        }

        // Default to English
        console.log('English language detected (default)');
        return 'en';
    }
    
    buildConferenceContext(language = 'en') {
        // Build complete session information with descriptions
        const sessionsInfo = this.data.sessions
            .filter(s => s.speakers.length > 0) // Only real sessions
            .map(s => {
                const time = s.start.substring(11, 16);
                return `[${time}] "${s.title}" by ${s.speakers.join(', ')} in ${s.room}\nDescription: ${s.description}`;
            })
            .join('\n\n');

        // Language-specific instructions
        const instructions = {
            en: `You are an intelligent assistant for the Data Community Austria Day 2026 conference (January 23, 2026 at JUFA Hotel Wien).

CONFERENCE SCHEDULE:
${sessionsInfo}

Instructions:
- Answer in ENGLISH, be concise and friendly
- Use structured formatting for readability:
  * Use line breaks between different items
  * Use bullet points (•) for lists
  * Add blank lines between sections for clarity
  * Number items when showing sequences
- You can answer complex questions like:
  * "Which sessions start at 1:45 PM?"
  * "Summarize each session in 2 sentences"
  * "What topics does speaker X cover?"
  * "Tell me about sessions in Room Y"
- Always use 24-hour time format (e.g., 13:45)
- When describing sessions, include: title, time, room, and speaker
- You can provide summaries, comparisons, and recommendations
- Be helpful and conversational`,

            cs: `Jsi inteligentní asistent na konferenci Data Community Austria Day 2026 (23. ledna 2026 v JUFA Hotel Wien).

PROGRAM KONFERENCE:
${sessionsInfo}

DŮLEŽITÉ: Vždy odpovídej V ČEŠTINĚ! Uživatel se ptá česky, proto odpovídej VŽDY ČESKY!

Instrukce:
- VŽDY odpovídej ČESKY, nikdy anglicky
- Buď stručný a přátelský
- Používej strukturované formátování pro lepší čitelnost:
  * Používej odřádkování mezi různými položkami
  * Používej odrážky (•) pro seznamy
  * Přidávej prázdné řádky mezi sekcemi
  * Čísluj položky při sekvencích
- Umíš odpovídat na složité dotazy jako:
  * "Které přednášky začínají ve 13:45?"
  * "Připrav shrnutí každé přednášky na 2 věty"
  * "O čem mluví speaker X?"
  * "Jaké sessions jsou v místnosti Y?"
- Vždy používej 24hodinový formát času (např. 13:45)
- Když popisuješ session, uveď: název, čas, místnost a speakera
- Umíš dělat shrnutí, srovnání a doporučení
- Buď nápomocný a přátelský`,

            de: `Du bist ein intelligenter Assistent für die Data Community Austria Day 2026 Konferenz (23. Januar 2026 im JUFA Hotel Wien).

KONFERENZPROGRAMM:
${sessionsInfo}

WICHTIG: Antworte IMMER AUF DEUTSCH! Der Benutzer fragt auf Deutsch, also antworte IMMER AUF DEUTSCH!

Anweisungen:
- IMMER auf DEUTSCH antworten, niemals auf Englisch
- Sei prägnant und freundlich
- Verwende strukturierte Formatierung für bessere Lesbarkeit:
  * Nutze Zeilenumbrüche zwischen verschiedenen Punkten
  * Verwende Aufzählungszeichen (•) für Listen
  * Füge Leerzeilen zwischen Abschnitten ein
  * Nummeriere Elemente bei Sequenzen
- Du kannst komplexe Fragen beantworten wie:
  * "Welche Sessions beginnen um 13:45 Uhr?"
  * "Fasse jede Session in 2 Sätzen zusammen"
  * "Worüber spricht Speaker X?"
  * "Welche Sessions finden in Raum Y statt?"
- Verwende immer das 24-Stunden-Zeitformat (z.B. 13:45)
- Bei der Beschreibung von Sessions nenne: Titel, Zeit, Raum und Speaker
- Du kannst Zusammenfassungen, Vergleiche und Empfehlungen geben
- Sei hilfsbereit und kommunikativ`
        };

        return instructions[language] || instructions.en;
    }
    
    generateFallbackResponse(message) {
        // Fallback response when API key is not configured
        const lowerMsg = message.toLowerCase();
        const language = this.detectLanguage(message);

        const responses = {
            en: {
                apiKeyMissing: `⚠️ Claude AI is not configured yet.\n\nTo enable intelligent chatbot:\n1. Get API key from https://console.anthropic.com/\n2. Add it to config.js\n3. Reload the page\n\nFor now, try basic questions like:\n• "Which sessions start at 9:15?"\n• "How many speakers?"`,
                timeQuery: (time, sessions) => `Sessions starting at ${time}:\n\n${sessions.map(s => `• ${s.title} in ${s.room}`).join('\n')}`,
                speakerQuery: `We have ${this.data.speakers.length} amazing speakers! Including: ${this.data.speakers.slice(0, 3).map(s => s.name).join(', ')} and more.`,
                roomQuery: `The conference takes place in ${this.data.rooms.length} rooms: ${this.data.rooms.map(r => r.name).join(', ')}.`,
                default: `Thanks for your question! Currently in fallback mode. Try questions like:\n• "Which sessions start at 9:15?"\n• "How many speakers?"\n• "What rooms are available?"`
            },
            cs: {
                apiKeyMissing: `⚠️ Claude AI zatím není nakonfigurován.\n\nPro aktivaci inteligentního chatbota:\n1. Získej API klíč z https://console.anthropic.com/\n2. Přidej ho do config.js\n3. Obnov stránku\n\nProzatím zkus základní otázky jako:\n• "Které session začínají v 9:15?"\n• "Kolik je speakerů?"`,
                timeQuery: (time, sessions) => `Sessions začínající v ${time}:\n\n${sessions.map(s => `• ${s.title} v ${s.room}`).join('\n')}`,
                speakerQuery: `Máme ${this.data.speakers.length} skvělých speakerů! Mezi nimi: ${this.data.speakers.slice(0, 3).map(s => s.name).join(', ')} a další.`,
                roomQuery: `Konference probíhá v ${this.data.rooms.length} místnostech: ${this.data.rooms.map(r => r.name).join(', ')}.`,
                default: `Díky za dotaz! Momentálně v záložním režimu. Zkus se zeptat:\n• "Které session začínají v 9:15?"\n• "Kolik je speakerů?"\n• "Jaké jsou místnosti?"`
            },
            de: {
                apiKeyMissing: `⚠️ Claude AI ist noch nicht konfiguriert.\n\nUm den intelligenten Chatbot zu aktivieren:\n1. Hol dir einen API-Schlüssel von https://console.anthropic.com/\n2. Füge ihn zu config.js hinzu\n3. Lade die Seite neu\n\nVorerst versuche einfache Fragen wie:\n• "Welche Sessions beginnen um 9:15?"\n• "Wie viele Speaker gibt es?"`,
                timeQuery: (time, sessions) => `Sessions um ${time}:\n\n${sessions.map(s => `• ${s.title} in ${s.room}`).join('\n')}`,
                speakerQuery: `Wir haben ${this.data.speakers.length} großartige Speaker! Darunter: ${this.data.speakers.slice(0, 3).map(s => s.name).join(', ')} und mehr.`,
                roomQuery: `Die Konferenz findet in ${this.data.rooms.length} Räumen statt: ${this.data.rooms.map(r => r.name).join(', ')}.`,
                default: `Danke für deine Frage! Momentan im Fallback-Modus. Versuche Fragen wie:\n• "Welche Sessions beginnen um 9:15?"\n• "Wie viele Speaker gibt es?"\n• "Welche Räume gibt es?"`
            }
        };

        const msgs = responses[language];

        // Time-based queries
        const timeMatch = message.match(/(\d{1,2}):(\d{2})/);
        if (timeMatch) {
            const sessions = this.getSessionsByTime(timeMatch[0]);
            if (sessions.length > 0) {
                return msgs.timeQuery(timeMatch[0], sessions);
            }
        }

        // Speaker queries
        if (lowerMsg.includes('speaker') || lowerMsg.includes('přednášející') || lowerMsg.includes('sprecher')) {
            return msgs.speakerQuery;
        }

        // Room queries
        if (lowerMsg.includes('room') || lowerMsg.includes('místnost') || lowerMsg.includes('raum')) {
            return msgs.roomQuery;
        }

        // API key missing hint
        if (typeof CONFIG === 'undefined' || CONFIG.ANTHROPIC_API_KEY === 'YOUR_API_KEY_HERE') {
            return msgs.apiKeyMissing;
        }

        // Default
        return msgs.default;
    }
    
    getSessionsByTime(timeStr) {
        return this.data.sessions.filter(s => {
            const sessionTime = this.formatTime(s.start);
            return sessionTime.includes(timeStr);
        });
    }
    
    addChatMessage(text, type) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;

        // Format text with proper line breaks and structure
        const formattedText = this.formatChatText(text);
        messageDiv.innerHTML = formattedText;

        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    formatChatText(text) {
        // Convert newlines to <br> tags
        // Preserve double line breaks as paragraph breaks
        // Handle bullet points and numbered lists

        // Replace double newlines with paragraph breaks
        let formatted = text.replace(/\n\n+/g, '</p><p>');

        // Replace single newlines with <br>
        formatted = formatted.replace(/\n/g, '<br>');

        // Detect and format bullet points (•, -, *)
        formatted = formatted.replace(/^([•\-\*])\s+(.+?)(<br>|$)/gm, '<span style="display: block; margin-left: 1rem;">$1 $2</span>');

        // Detect and format numbered lists (1., 2., etc.)
        formatted = formatted.replace(/^(\d+\.)\s+(.+?)(<br>|$)/gm, '<span style="display: block; margin-left: 1rem;">$1 $2</span>');

        // Wrap in paragraph tags
        formatted = `<p>${formatted}</p>`;

        // Clean up any empty paragraphs
        formatted = formatted.replace(/<p><\/p>/g, '');

        return formatted;
    }
    
    formatTime(isoString) {
        const date = new Date(isoString);
        return date.toLocaleTimeString('cs-CZ', { 
            hour: '2-digit', 
            minute: '2-digit',
            timeZone: 'Europe/Vienna'
        });
    }
    
    loadFavorites() {
        const saved = localStorage.getItem('conference-favorites');
        return saved ? JSON.parse(saved) : [];
    }
    
    saveFavorites() {
        localStorage.setItem('conference-favorites', JSON.stringify(this.favorites));
    }
}

// Initialize app
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new ConferenceApp();
});

// Service Worker registration for PWA
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('sw.js')
            .then(reg => console.log('Service Worker registered'))
            .catch(err => console.log('Service Worker registration failed'));
    });
}
