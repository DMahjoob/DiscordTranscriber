# 🎙️ Discord Transciber - The Ultimate Discord Voice Transcription & Summarization Bot

## 🚀 Introduction
**TranscriptBot** is a powerful Discord bot that records voice chats, transcribes speech to text, and generates insightful summaries with action items. Whether you're hosting meetings, gaming, or having casual conversations, **TranscriptBot** ensures that no important detail is lost!

## ✨ Features
- 🎤 **Voice Channel Recording** - Easily record voice channels with a simple command.
- 📝 **Speech-to-Text Transcription** - Uses Google Cloud Speech-to-Text for accurate transcription.
- 🧠 **AI-Powered Summarization** - Groq AI extracts key insights and action items from conversations.
- 🔄 **Seamless Integration** - Works effortlessly in Discord servers with simple commands.
- 🏆 **User-Friendly Commands** - Intuitive commands make recording and summarizing a breeze.

## 📌 Commands
| Command | Description |
|---------|-------------|
| `!join` | Bot joins the voice channel. |
| `!leave` | Bot leaves the voice channel. |
| `!start_recording` | Starts recording the voice channel. |
| `!stop_recording` | Stops recording and provides a transcript. |

## 🔧 Installation & Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/TranscriptBot.git
   cd TranscriptBot
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Create your own bot -> https://discordpy.readthedocs.io/en/stable/discord.html**
   Follow this guide to create your own bot so you can run this code locally.
   
5. **Set up environment variables**
   Create a `.env` file and add:
   ```ini
   DISCORD_BOT_TOKEN=your_discord_bot_token_id
   GOOGLE_APPLICATION_CREDENTIALS=your_google_credentials.json
   GROQ_API_KEY=your_groq_api_key
   ```
6. **Run the bot**
   ```bash
   python main.py
   ```

## 🛠️ Technologies Used
- **Discord.py** - For seamless Discord bot integration.
- **Google Cloud Speech-to-Text** - For high-quality voice transcription.
- **Groq AI** - For intelligent conversation summarization.
- **FFmpeg** - For efficient audio recording.

## 🌟 Why Choose TranscriptBot?
✅ **High Accuracy** - Industry-leading transcription and summarization.
✅ **Time-Saving** - Focus on conversations, let the bot handle notes.
✅ **Customizable** - Easily extend or modify the bot for your needs.
✅ **Open Source** - Contribute and improve the project together!


---
