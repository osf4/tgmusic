# tgmusic
tgmusic is a small Telegram bot that allows you to get your VK tracks in chat.

# Install
```git clone https://github.com/osf4/tgmusic```

# Usage
```python main.py```
or
```python main.py -c config_file_path```
if you want to use specific config file (by default it's *.env*)

# TODO
- Optimize sending audio files (Now it takes 2-3 seconds to send an audio file, but they can be cached in a private channel that allows the bot to send audio by FileID)
