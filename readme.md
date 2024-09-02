# TGmusic
TGmusic is a small Telegram bot that allows you to get tracks from VK by name or your profile link

# Install
git clone https://github.com/osf4/tgmusic
  
# Usage
1. Create .env file
2. Put that code into the .env file:

```

VK_ACCESS_TOKEN = 'your token from https://vkhost.github.io'
TELEGRAM_BOT_TOKEN = 'your telegram token from @BotFather'

TELEGRAM_BOT_URL = 't.me/ link to your bot. If provided, the bot will provide "via" capture for every track'
```

3. run ```python main.py```