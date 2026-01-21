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

### Batch Files (Windows):
- **`open-website.bat`** - Opens the website in browser
- **`fetch-messages.bat`** - Runs the message fetching script
- **`auth-telegram.bat`** - Runs the authentication script

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

### First Time Setup:
1. **Authenticate with Telegram**: Run `auth-telegram.bat` (Windows) or `python auth_telegram.py`
2. Follow the authentication prompts in your browser or Telegram app
3. **Fetch Messages**: Run `fetch-messages.bat` (Windows) or `fetch-messages.ps1` (PowerShell)
4. The script will connect to Telegram and fetch all messages from @BdevHub
5. Messages are automatically categorized into Scripts and News folders

### Updating Messages:
- **Via Script**: Run the fetch script again to get the latest messages
- **Via Website**: Click the "🔄 Refresh Messages" button on the website

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