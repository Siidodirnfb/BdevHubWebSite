// Message data structure - this will be populated from scripts/ and news/ folders
let allMessages = [];

// DOM elements
const allBtn = document.getElementById('allBtn');
const scriptsBtn = document.getElementById('scriptsBtn');
const newsBtn = document.getElementById('newsBtn');
const messageContainer = document.getElementById('messageContainer');

// Initialize the application
async function init() {
    try {
        await loadMessages();
        renderMessages('all');
        setupEventListeners();
    } catch (error) {
        console.error('Error initializing app:', error);
        messageContainer.innerHTML = '<p class="error">Error loading messages. Please check the console for details.</p>';
    }
}

// Load messages from scripts and news folders
async function loadMessages() {
    allMessages = [];

    try {
        // Load scripts (Lua syntax messages)
        const scriptsResponse = await fetch('scripts/messages.json');
        if (scriptsResponse.ok) {
            const scriptsData = await scriptsResponse.json();
            allMessages.push(...scriptsData.map(msg => ({ ...msg, type: 'scripts' })));
        }
    } catch (error) {
        console.warn('Could not load scripts/messages.json:', error);
    }

    try {
        // Load news (regular messages)
        const newsResponse = await fetch('news/messages.json');
        if (newsResponse.ok) {
            const newsData = await newsResponse.json();
            allMessages.push(...newsData.map(msg => ({ ...msg, type: 'news' })));
        }
    } catch (error) {
        console.warn('Could not load news/messages.json:', error);
    }

    // Sort messages by date (newest first)
    allMessages.sort((a, b) => new Date(b.date) - new Date(a.date));
}

// Render messages based on filter
function renderMessages(filter) {
    let filteredMessages = allMessages;

    if (filter === 'scripts') {
        filteredMessages = allMessages.filter(msg => msg.type === 'scripts');
    } else if (filter === 'news') {
        filteredMessages = allMessages.filter(msg => msg.type === 'news');
    }

    messageContainer.innerHTML = '';

    if (filteredMessages.length === 0) {
        messageContainer.innerHTML = `
            <div class="message">
                <div class="message-content">
                    <p>No messages found in this category yet. Messages will appear here once added to the respective folders.</p>
                </div>
            </div>
        `;
        return;
    }

    filteredMessages.forEach((message, index) => {
        const messageElement = createMessageElement(message, index);
        messageContainer.appendChild(messageElement);
    });
}

// Create message element
function createMessageElement(message, index) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${message.type}`;
    messageDiv.style.animationDelay = `${index * 0.1}s`;

    const contentHtml = message.content.includes('```lua') || message.content.includes('```')
        ? `<pre><code>${escapeHtml(message.content)}</code></pre>`
        : `<p>${message.content.replace(/\n/g, '<br>')}</p>`;

    messageDiv.innerHTML = `
        <div class="message-content">
            ${contentHtml}
        </div>
        <div class="message-meta">
            <span class="message-date">${formatDate(message.date)}</span>
            <span class="message-type">${message.type}</span>
        </div>
    `;

    return messageDiv;
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Setup event listeners for filter buttons
function setupEventListeners() {
    allBtn.addEventListener('click', () => {
        setActiveButton(allBtn);
        renderMessages('all');
    });

    scriptsBtn.addEventListener('click', () => {
        setActiveButton(scriptsBtn);
        renderMessages('scripts');
    });

    newsBtn.addEventListener('click', () => {
        setActiveButton(newsBtn);
        renderMessages('news');
    });
}

// Set active button state
function setActiveButton(activeBtn) {
    [allBtn, scriptsBtn, newsBtn].forEach(btn => {
        btn.classList.remove('active');
    });
    activeBtn.classList.add('active');
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', init);