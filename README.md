# @BdevHub Archive Website

A website for archiving and organizing messages from the @BdevHub Telegram channel.

## Features

- **Filtering System**: Filter messages by Scripts (Lua syntax) and News (regular messages)
- **Responsive Design**: Works on desktop and mobile devices
- **Easy Content Management**: Simply add messages to JSON files in respective folders

## Structure

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

## How to Add New Messages

### For Scripts (Lua code):
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

### For News (regular messages):
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

### Message Format Guidelines:
- **id**: Unique number for each message
- **content**: The actual message content. Use ```lua for code blocks in scripts
- **date**: ISO date format (YYYY-MM-DDTHH:mm:ssZ)
- **type**: Either "scripts" or "news"

## Running the Website

Simply open `index.html` in any modern web browser. No server required!

## Technologies Used

- HTML5
- CSS3 (with modern features like Flexbox and CSS Grid)
- Vanilla JavaScript (ES6+)
- JSON for data storage