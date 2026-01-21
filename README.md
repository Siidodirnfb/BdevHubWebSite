# @BdevHub Archive Website

A website for archiving and organizing messages from the @BdevHub Telegram channel with automatic fetching capabilities.

## Features

- **Automatic Message Fetching**: Fetch messages directly from @BdevHub Telegram channel
- **Smart Categorization**: Automatically separates Scripts (Lua syntax) from News
- **Filtering System**: Filter messages by Scripts (Lua syntax) and News (regular messages)
- **Live Refresh**: Refresh button to fetch latest messages without reopening browser
- **Responsive Design**: Works on desktop and mobile devices

## Files Overview

### Core Files:
- **`index.html`** - Main website
- **`styles.css`** - Website styling
- **`script.js`** - Website functionality
- **`fetch_messages.py`** - Python script to fetch messages from Telegram
- **`auth_telegram.py`** - Authentication script for first-time setup
- **`create_session_string.py`** - Generate session string for GitHub Actions

### Batch Files (Windows):
- **`open-website.bat`** - Opens the website in browser
- **`fetch-messages.bat`** - Runs the message fetching script
- **`auth-telegram.bat`** - Runs the authentication script
- **`create-session.bat`** - Creates session string for GitHub Actions

### GitHub Actions:
- **`.github/workflows/fetch-messages.yml`** - Automated message fetching workflow

### Data Folders:
- **`scripts/`** - Contains `messages.json` with Lua scripts
- **`news/`** - Contains `messages.json` with news/announcements

### Scripts Folder (`scripts/`)
Contains messages that have Lua syntax (indicated by ```lua code blocks). These are typically:
- Code snippets
- Scripts
- Technical implementations
- Programming tutorials

### News Folder (`news/`)
Contains messages without any syntax. These are typically:
- Announcements
- Updates
- General information
- Community posts

## Automatic Message Fetching

The easiest way to add messages is to use the automatic fetching system:

### Option 1: Local Setup (Recommended for Development)

#### First Time Setup:
1. **Clone Repository**: `git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git`
2. **Authenticate with Telegram**: Run `auth-telegram.bat` (Windows) or `python auth_telegram.py`
3. Follow the authentication prompts in your browser or Telegram app
4. **Fetch Messages**: Run `fetch-messages.bat` (Windows) or `fetch-messages.ps1` (PowerShell)
5. The script will connect to Telegram and fetch all messages from @BdevHub
6. Messages are automatically categorized into Scripts and News folders

#### Updating Messages:
- **Via Script**: Run `fetch-messages.bat` again to get the latest messages
- **Via Website**: Click the "🔄 Refresh Messages" button on the website
- **Commit Changes**: `git add . && git commit -m "Update messages" && git push`

### Option 2: GitHub Actions (Fully Automated)

Set up automatic message fetching on GitHub so your repository updates itself daily:

#### GitHub Actions Setup:

1. **Add Repository Secrets:**
   - Go to your GitHub repo → Settings → Secrets and variables → Actions
   - Add these secrets:
     - `TELEGRAM_API_ID`: `30753680`
     - `TELEGRAM_API_HASH`: `c238c9c45ed3243c173058b2b64ef1fe`
     - `TELEGRAM_SESSION`: (See step 2)

2. **Create Session String:**
   ```bash
   # Run locally after authenticating:
   python create_session_string.py
   ```
   Copy the generated session string to GitHub as `TELEGRAM_SESSION`

3. **Push the Workflow:**
   The `.github/workflows/fetch-messages.yml` file is already created and will:
   - Run daily at 2 AM UTC
   - Fetch latest messages from @BdevHub
   - Update `scripts/messages.json` and `news/messages.json`
   - Commit and push changes automatically

4. **Manual Triggers:**
   - Go to Actions tab in your repo
   - Click "Fetch @BdevHub Messages"
   - Click "Run workflow" to trigger manually

#### Benefits of GitHub Actions:
- ✅ Fully automated daily updates
- ✅ No local setup required after initial config
- ✅ Version controlled message history
- ✅ Public website automatically stays current

### Manual Message Addition

If you prefer to add messages manually:

#### For Scripts (Lua code):
1. Open `scripts/messages.json`
2. Add a new object to the array with this format:
```json
{
    "id": 3,
    "content": "```lua\n-- Your Lua code here\nprint(\"Hello World!\")\n```",
    "date": "2024-01-21T15:30:00Z",
    "type": "scripts"
}
```

#### For News (regular messages):
1. Open `news/messages.json`
2. Add a new object to the array with this format:
```json
{
    "id": 3,
    "content": "Your news message here. Can include emojis and line breaks.",
    "date": "2024-01-21T15:30:00Z",
    "type": "news"
}
```

#### Message Format Guidelines:
- **id**: Unique number for each message
- **content**: The actual message content. Use ```lua for code blocks in scripts
- **date**: ISO date format (YYYY-MM-DDTHH:mm:ssZ)
- **type**: Either "scripts" or "news"

## Running the Website

Simply open `index.html` in any modern web browser. No server required!

## Technologies Used

### Frontend:
- HTML5
- CSS3 (with modern features like Flexbox and CSS Grid)
- Vanilla JavaScript (ES6+)

### Backend/Data:
- Python 3
- Telethon (Telegram API library)
- JSON for data storage