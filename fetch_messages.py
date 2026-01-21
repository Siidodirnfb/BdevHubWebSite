#!/usr/bin/env python3
"""
Telegram Channel Message Fetcher for @BdevHub
Automatically fetches and categorizes messages into Scripts and News
"""

import asyncio
import json
import os
import re
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from telethon.tl.types import Channel

# Telegram API credentials
API_ID = 30753680
API_HASH = 'c238c9c45ed3243c173058b2b64ef1fe'

# Channel username
CHANNEL_USERNAME = '@BdevHub'

# Session file
SESSION_NAME = 'bdevhub_session'

# Output directories
SCRIPTS_DIR = 'scripts'
NEWS_DIR = 'news'
SCRIPTS_FILE = os.path.join(SCRIPTS_DIR, 'messages.json')
NEWS_FILE = os.path.join(NEWS_DIR, 'messages.json')

class BdevHubFetcher:
    def __init__(self):
        self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        self.scripts = []
        self.news = []
        self.message_id_counter = 1

    async def connect(self):
        """Connect to Telegram"""
        try:
            print("Connecting to Telegram...")
            await self.client.start()

            # Check if we need to login
            if not await self.client.is_user_authorized():
                print("First time setup: You need to authenticate with Telegram.")
                print("Please run this script in an interactive terminal to complete authentication.")
                print("After authentication, you can run it again to fetch messages.")
                return False

            print("Successfully connected!")
            return True
        except Exception as e:
            print(f"Error connecting: {e}")
            return False

    async def fetch_channel_messages(self, limit=1000):
        """Fetch messages from the channel"""
        try:
            print(f"Fetching up to {limit} messages from {CHANNEL_USERNAME}...")

            # Get the channel entity
            channel = await self.client.get_entity(CHANNEL_USERNAME)
            print(f"Channel found: {channel.title}")

            # Fetch messages
            messages = []
            async for message in self.client.iter_messages(channel, limit=limit):
                if message.text:  # Only process text messages
                    messages.append({
                        'id': message.id,
                        'content': message.text,
                        'date': message.date.isoformat(),
                        'original_id': message.id
                    })

            print(f"Fetched {len(messages)} messages")
            return messages

        except Exception as e:
            print(f"Error fetching messages: {e}")
            return []

    def categorize_message(self, message):
        """Categorize message as script or news based on Lua syntax"""
        content = message['content']

        # Debug: Print message content for analysis
        print(f"\n[DEBUG] Analyzing message ID {message.get('id', 'unknown')}:")
        print(f"Content length: {len(content)} chars")
        print(f"Content preview: {content[:200]}...")
        if '```' in content:
            print("Found code blocks in message!")
        if 'loadstring' in content:
            print("Found loadstring in message!")

        # Primary indicators - actual code and script functions
        lua_code_patterns = [
            r'```lua',           # Code blocks marked as Lua
            r'```.*loadstring',  # Code blocks with loadstring
            r'loadstring\s*\(',  # loadstring function calls
            r'game\s*[:\.]',     # game: or game. references
            r'workspace\s*[:\.]', # workspace: or workspace. references
            r'Instance\.new',    # Roblox Instance.new
            r'local\s+\w+\s*=',  # local variable assignments
            r'function\s+\w+',   # function definitions
            r'end\s*$',          # end statements
            r'print\s*\(',       # print function calls
            r'HttpGet\s*\(',     # HTTP requests (common in scripts)
            r'require\s*\(',     # require statements
            r'getgenv\s*\(',     # getgenv (common in exploits)
            r'getsenv\s*\(',     # getsenv
            r'setclipboard\s*\(', # setclipboard
            r'hookfunction\s*\(', # hookfunction
            r'firetouchinterest\s*\(', # firetouchinterest
            r'fireclickdetector\s*\(', # fireclickdetector
            r'```[\s\S]*?```',   # Any code blocks (backticks)
            r'```\w+[\s\S]*?```', # Language-specific code blocks
        ]

        # Check for actual code patterns first (highest priority)
        has_code = any(re.search(pattern, content, re.IGNORECASE | re.MULTILINE) for pattern in lua_code_patterns)

        print(f"Has code patterns: {has_code}")

        if has_code:
            print("Categorized as: SCRIPTS (code detected)")
            return 'scripts'

        # Secondary check - script repository URLs
        has_script_url = bool(re.search(r'github\.com.*(?:script|hub|exploit|hack|lua)', content, re.IGNORECASE))
        has_raw_github = bool(re.search(r'raw\.githubusercontent\.com', content, re.IGNORECASE))

        print(f"Has script URLs: {has_script_url or has_raw_github}")

        if has_script_url or has_raw_github:
            print("Categorized as: SCRIPTS (script URL detected)")
            return 'scripts'

        # Tertiary check - specific script-related terms in context
        # Only if they appear near code-like elements
        script_context_indicators = [
            r'\bscript\b.*(?:loadstring|function|local)',
            r'(?:loadstring|function|local).*\bscript\b',
            r'\bhack\b.*(?:loadstring|function)',
            r'\bexploit\b.*(?:loadstring|function)',
            r'\bcheat\b.*(?:loadstring|function)',
        ]

        has_script_context = any(re.search(pattern, content, re.IGNORECASE | re.DOTALL) for pattern in script_context_indicators)

        print(f"Has script context: {has_script_context}")

        if has_script_context:
            print("Categorized as: SCRIPTS (script context detected)")
            return 'scripts'

        # Everything else is news/announcements
        print("Categorized as: NEWS (no script indicators found)")
        return 'news'

    def process_messages(self, messages):
        """Process and categorize all messages"""
        print("Categorizing messages...")

        for message in messages:
            category = self.categorize_message(message)

            # Add message ID and type
            processed_message = {
                'id': self.message_id_counter,
                'content': message['content'],
                'date': message['date'],
                'type': category
            }

            if category == 'scripts':
                self.scripts.append(processed_message)
            else:
                self.news.append(processed_message)

            self.message_id_counter += 1

        # Sort by date (newest first)
        self.scripts.sort(key=lambda x: x['date'], reverse=True)
        self.news.sort(key=lambda x: x['date'], reverse=True)

        print(f"Categorized: {len(self.scripts)} scripts, {len(self.news)} news messages")

    def save_to_json(self):
        """Save categorized messages to JSON files"""
        # Ensure directories exist
        os.makedirs(SCRIPTS_DIR, exist_ok=True)
        os.makedirs(NEWS_DIR, exist_ok=True)

        # Save scripts
        with open(SCRIPTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.scripts, f, indent=2, ensure_ascii=False)

        # Save news
        with open(NEWS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.news, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(self.scripts)} scripts to {SCRIPTS_FILE}")
        print(f"Saved {len(self.news)} news to {NEWS_FILE}")

    async def run(self, limit=1000):
        """Main execution method"""
        print("=== @BdevHub Message Fetcher ===\n")

        if not await self.connect():
            return False

        try:
            messages = await self.fetch_channel_messages(limit)
            if not messages:
                print("No messages fetched.")
                return False

            self.process_messages(messages)
            self.save_to_json()

            print("\n[SUCCESS] Successfully fetched and categorized messages!")
            return True

        except Exception as e:
            print(f"[ERROR] Error during execution: {e}")
            return False
        finally:
            await self.client.disconnect()

async def main():
    """Main function"""
    fetcher = BdevHubFetcher()

    # You can change the limit here (default: 1000 messages)
    success = await fetcher.run(limit=1000)

    if success:
        print("\n[SUCCESS] Done! Check your scripts/ and news/ folders.")
        print("You can now refresh the website to see the new messages.")
    else:
        print("\n[ERROR] Failed to fetch messages. Check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())