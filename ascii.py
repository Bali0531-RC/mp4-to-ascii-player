#!/usr/bin/env python3
import cv2
import numpy as np
import pygame
import threading
import time
import sys
import os
import subprocess
import shutil
import requests
from threading import Event

# Single built-in video URL
APPLE_URL = "https://panel.newdream.hu/apple.mp4"
APPLE_FILENAME = "apple.mp4"

def download_apple():
    """Download Apple video"""
    # Check if already downloaded
    if os.path.exists(APPLE_FILENAME):
        print(f"'{APPLE_FILENAME}' already downloaded.")
        return APPLE_FILENAME
    
    print(f"Downloading: {APPLE_URL}")
    
    try:
        # Stream download with progress bar
        response = requests.get(APPLE_URL, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(APPLE_FILENAME, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Progress bar
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        progress_bar = "█" * int(percent / 2) + "░" * (50 - int(percent / 2))
                        print(f"\r[{progress_bar}] {percent:.1f}% ({downloaded}/{total_size} bytes)", end='')
                    else:
                        print(f"\rDownloaded: {downloaded} bytes", end='')
        
        print(f"\nSuccessful download: {APPLE_FILENAME}")
        return APPLE_FILENAME
        
    except requests.RequestException as e:
        print(f"Download error: {e}")
        if os.path.exists(APPLE_FILENAME):
            os.remove(APPLE_FILENAME)  # Remove partially downloaded file
        return None
    except Exception as e:
        print(f"General error: {e}")
        return None

class ASCIIVideoPlayer:
    def __init__(self, video_path, audio_path=None, custom_fps=None, use_blocks=False):
        self.video_path = video_path
        self.audio_path = audio_path or video_path
        self.cap = cv2.VideoCapture(video_path)
        
        self.original_fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.fps = custom_fps if custom_fps else self.original_fps
        self.frame_delay = 1.0 / self.fps
        self.fps_multiplier = self.fps / self.original_fps
        
        self.stop_event = Event()
        
        # Choose between two character sets
        self.ascii_chars1 = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
        self.ascii_chars2 = " .'`^\",:;Il!i~+_-?|\\tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$░▒▓█"
        
        # Character set selection
        if use_blocks:
            self.ascii_chars = self.ascii_chars2
            print("Using charset: Block characters (░▒▓█)")
        else:
            self.ascii_chars = self.ascii_chars1
            print("Using charset: Standard ASCII")
        
        self.update_terminal_size()
        
        print(f"Original FPS: {self.original_fps:.2f} -> Playback FPS: {self.fps:.2f} (x{self.fps_multiplier:.2f})")

    def update_terminal_size(self):
        try:
            terminal_size = shutil.get_terminal_size()
            self.width = terminal_size.columns
            self.height = terminal_size.lines - 3
            
            self.width = max(40, min(200, self.width))
            self.height = max(20, min(60, self.height))
            
            print(f"Terminal size: {self.width}x{self.height}")
            
        except Exception as e:
            print(f"Size determination error: {e}")
            self.width = 120
            self.height = 40

    def update_terminal_size(self):
        try:
            terminal_size = shutil.get_terminal_size()
            self.width = terminal_size.columns
            self.height = terminal_size.lines - 3
            
            self.width = max(40, min(200, self.width))
            self.height = max(20, min(60, self.height))
            
            print(f"Terminál méret: {self.width}x{self.height}")
            
        except Exception as e:
            print(f"Méret meghatározás hiba: {e}")
            self.width = 120
            self.height = 40

    def get_current_terminal_size(self):
        try:
            terminal_size = shutil.get_terminal_size()
            new_width = terminal_size.columns
            new_height = terminal_size.lines - 3
            
            new_width = max(40, min(200, new_width))
            new_height = max(20, min(60, new_height))
            
            return new_width, new_height
        except:
            return self.width, self.height

    def frame_to_ascii(self, frame):
        current_width, current_height = self.get_current_terminal_size()
        
        if current_width != self.width or current_height != self.height:
            self.width = current_width
            self.height = current_height
        
        frame = cv2.resize(frame, (self.width, self.height))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ascii_frame = ""
        for row in gray:
            ascii_row = ""
            for pixel in row:
                ascii_index = int(pixel / 255 * (len(self.ascii_chars) - 1))
                ascii_row += self.ascii_chars[ascii_index]
            ascii_frame += ascii_row + "\n"
        return ascii_frame

    def play_audio_with_ffplay(self):
        try:
            if abs(self.fps_multiplier - 1.0) < 0.01:
                cmd = ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', self.video_path]
            else:
                tempo = self.fps_multiplier
                cmd = [
                    'ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet',
                    '-af', f'atempo={tempo}', self.video_path
                ]
            
            self.audio_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            while self.audio_process.poll() is None and not self.stop_event.is_set():
                time.sleep(0.1)
        except FileNotFoundError:
            print("ffplay not found. Install ffmpeg: sudo apt install ffmpeg")
            self.play_audio_pygame()
        except Exception as e:
            print(f"ffplay error: {e}")
            self.play_audio_pygame()

    def play_audio_pygame(self):
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
            if self.audio_path != self.video_path and os.path.exists(self.audio_path):
                pygame.mixer.music.load(self.audio_path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() and not self.stop_event.is_set():
                    time.sleep(0.1)
            else:
                print("Pygame cannot play MP4 audio directly.")
        except Exception as e:
            print(f"Audio error: {e}")

    def play_audio(self):
        self.play_audio_with_ffplay()

    def play(self):
        """Simple playback - normal mode only"""
        if not self.cap.isOpened():
            print("Error: Failed to open video!")
            return
        
        try:
            print('\033[?25l\033[?1049h', end='')
            print('\033[2J\033[H', end='')
            
            audio_thread = threading.Thread(target=self.play_audio)
            audio_thread.daemon = True
            audio_thread.start()
            
            print("ASCII Video Player")
            print("Press CTRL+C to exit...")
            time.sleep(2)
            
            frame_count = 0
            start_time = time.time()
            fps_counter = 0
            fps_start_time = time.time()
            
            prev_frame = ""
            
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                ascii_frame = self.frame_to_ascii(frame)
                
                if ascii_frame != prev_frame:
                    output = '\033[H' + ascii_frame
                    print(output, end='')
                    prev_frame = ascii_frame
            
                fps_counter += 1
                if fps_counter % 60 == 0:
                    current_fps = 60 / (time.time() - fps_start_time)
                    print(f"\033[{self.height + 2};1HFPS: {current_fps:.1f}", end='')
                    fps_start_time = time.time()
                
                sys.stdout.flush()
                
                frame_count += 1
                expected_time = start_time + (frame_count * self.frame_delay)
                current_time = time.time()
                
                if current_time < expected_time:
                    time.sleep(expected_time - current_time)
                
        except KeyboardInterrupt:
            pass
        
        finally:
            print('\033[?1049l\033[?25h', end='')
            sys.stdout.flush()
            
            self.stop_event.set()
            if hasattr(self, 'audio_process'):
                self.audio_process.terminate()
            self.cap.release()
            pygame.mixer.quit()

def extract_audio_with_ffmpeg(video_path, audio_path):
    try:
        cmd = [
            'ffmpeg', '-i', video_path, 
            '-vn', '-acodec', 'pcm_s16le', 
            '-ar', '44100', '-ac', '2', 
            '-y', audio_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print(f"FFmpeg error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("FFmpeg not found. Install with: sudo apt install ffmpeg")
        return False
    except Exception as e:
        print(f"Audio extraction error: {e}")
        return False

def extract_audio_from_video(video_path, audio_path):
    if extract_audio_with_ffmpeg(video_path, audio_path):
        return True
    try:
        import moviepy.editor as mp
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        video.close()
        return True
    except ImportError:
        print("MoviePy not installed. Use: pip install moviepy")
        return False
    except Exception as e:
        print(f"MoviePy audio extraction error: {e}")
        return False

def parse_boolean(value):
    """Convert string value to boolean"""
    if isinstance(value, bool):
        return value
    if value.lower() in ('true', '1', 'yes', 'on', 'y'):
        return True
    elif value.lower() in ('false', '0', 'no', 'off', 'n'):
        return False
    else:
        raise ValueError(f"Invalid boolean value: {value}")

def main():
    if len(sys.argv) < 2:
        print("ASCII Video Player")
        print("=" * 50)
        print("Usage:")
        print("  python ascii.py <video> [fps] [blocks]")
        print("")
        print("Parameters:")
        print("  <video>      'apple' or video file name")
        print("  [fps]        Optional FPS (e.g.: 30, 60)")
        print("  [blocks]     true/false - use block characters")
        print("")
        print("Examples:")
        print("  python ascii.py apple                      # Bad Apple video, normal charset")
        print("  python ascii.py apple 60                   # Bad Apple video 60 FPS")
        print("  python ascii.py apple 30 true              # Bad Apple video, block characters")
        print("  python ascii.py myfile.mp4 24 false        # Custom file, normal charset")
        print("  python ascii.py video.mp4 30 true          # Custom file, block characters")
        print("")
        print("Charset types:")
        print("  false/0: Standard ASCII characters")
        print("  true/1:  Block characters (░▒▓█)")
        return
    
    video_arg = sys.argv[1]
    custom_fps = None
    use_blocks = False
    
    # FPS parameter (2nd argument)
    if len(sys.argv) > 2:
        try:
            custom_fps = float(sys.argv[2])
        except ValueError:
            print(f"Invalid FPS value: {sys.argv[2]}")
            return
    
    # Block characters parameter (3rd argument)
    if len(sys.argv) > 3:
        try:
            use_blocks = parse_boolean(sys.argv[3])
        except ValueError:
            print(f"Invalid blocks value: {sys.argv[3]}")
            print("Use: true/false, 1/0, yes/no")
            return
    
    # Determine video file
    video_path = None
    
    # If "apple", download it
    if video_arg.lower() == "apple":
        print("Downloading Apple video...")
        video_path = download_apple()
        if not video_path:
            print("Download failed!")
            return
    # If existing file
    elif os.path.exists(video_arg):
        video_path = video_arg
    # Try with .mp4 extension
    elif os.path.exists(video_arg + ".mp4"):
        video_path = video_arg + ".mp4"
    else:
        print(f"Error: '{video_arg}' not found!")
        print("Use 'python ascii.py apple' to download the Apple video.")
        return
    
    # Audio extraction
    audio_temp_path = "temp_audio.wav"
    print("Extracting audio from video...")
    if extract_audio_from_video(video_path, audio_temp_path):
        audio_path = audio_temp_path
        print("Audio successfully extracted!")
    else:
        print("Audio extraction failed, trying with ffplay...")
        audio_path = video_path
    
    # Playback
    player = ASCIIVideoPlayer(video_path, audio_path, custom_fps, use_blocks)
    player.play()
    
    # Cleanup
    if audio_path == "temp_audio.wav" and os.path.exists(audio_path):
        os.remove(audio_path)

if __name__ == "__main__":
    main()
