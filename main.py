import discord
from discord.ext import commands
from google.cloud import speech
import os
import subprocess
import asyncio
from dotenv import load_dotenv
from groq import Groq
from desolation import information
from format import conversationSummarySchema

# Load environment variables from .env file
load_dotenv()

# Access environment variables
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Set up Google Cloud Speech-to-Text client
client = speech.SpeechClient()

# Set up Discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Keep track of the FFmpeg process
ffmpeg_process = None

# Function to transcribe audio to text using Google Cloud Speech-to-Text
def transcribe_audio(audio_file):
    with open(audio_file, "rb") as f:
        audio = speech.RecognitionAudio(content=f.read())

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    # Combine all transcriptions
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return transcript

def generate_summary_and_action_items(transcript):
    client = Groq(api_key=GROQ_API_KEY)
    # Desolation
    # prompt = (f"You are writing notes based on this transcript for the game Pokemon Desolation to help the people in the meeting.. "
    #           f"There are many important locations and characters, such as these {information}."
    #           f"Use the {conversationSummarySchema} to help you craft your response and please"
    #           f"\nsummarize the following transcript and provide clear action items for each person in the call:\n\n{transcript}\n\n")
    # General
    prompt = (f"You are writing notes based on this transcript to help the people in the meeting "
              f"Use the {conversationSummarySchema} to help you craft your response and please"
              f"\nsummarize the following transcript and provide clear action items for each person in the call:\n\n{transcript}\n\n")
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    return response.choices[0].message.content.strip()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def join(ctx):
    """Command to make the bot join the voice channel."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You need to join a voice channel first.")

@bot.command()
async def leave(ctx):
    """Command to make the bot leave the voice channel."""
    if ctx.voice_client:  # Check if the bot is already connected to a voice channel
        await ctx.send("Left the voice channel.")
        await ctx.voice_client.disconnect()
        quit()
    else:
        await ctx.send("I'm not connected to any voice channel.")

@bot.command()
async def start_recording(ctx):
    """Command to start recording audio."""
    global ffmpeg_process
    if ctx.voice_client:
        # Set up FFmpeg command to record audio from the voice channel
        audio_file = "recorded_audio.wav"

        # Remove if already existing
        if os.path.exists(audio_file): os.remove(audio_file)

        # Start recording with FFmpeg
        command = [
            "ffmpeg",
            "-f", "avfoundation",  # For macOS; use dshow for Windows or alsa for Linux
            "-i", ":0",  # Adjust this based on your OS (e.g., ":0" for macOS, ":1" for Windows, etc.)
            "-ac", "1",  # Mono channel
            "-ar", "16000",  # 16kHz sample rate
            "-t", "600",  # Record for 600 seconds (10 minutes default)
            audio_file
        ]

        # Start the process
        ffmpeg_process = subprocess.Popen(command)
        await ctx.send("🔴 Recording started. Listening to this conversation...")

    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command()
async def stop_recording(ctx):
    """Command to stop recording."""
    global ffmpeg_process
    if ctx.voice_client:
        if ffmpeg_process:
            # Stop the recording process (send stop signal to FFmpeg)
            ffmpeg_process.terminate()
            ffmpeg_process = None
            await ctx.send("Recording stopped. Generating Summary and Action Items...")

            # Process the recorded audio after stopping
            audio_file = "recorded_audio.wav"
            if os.path.exists(audio_file):
                # Transcribe the audio to text
                transcript = transcribe_audio(audio_file)

                # Generate summary and action items using Groq
                gen_response = generate_summary_and_action_items(transcript)

                # Send result to the channel (split into chunks if necessary)
                max_message_length = 2000
                if len(gen_response) > max_message_length:
                    for i in range(0, len(gen_response), max_message_length):
                        await ctx.send(gen_response[i:i + max_message_length])
                else:
                    await ctx.send(f"\n\n{gen_response}")
            else:
                await ctx.send(f"Error: {audio_file} was not found. Make sure the recording was completed.")
        else:
            await ctx.send("🚫 Not recording anything right now.")
    else:
        await ctx.send("🚫 Not connected to a voice channel.")

bot.run(DISCORD_BOT_TOKEN)
