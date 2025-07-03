import logging
import os
import tempfile
import pygame
import platform
import subprocess
from datetime import datetime
import time
import psutil
from gtts import gTTS
import uuid
import json

def get_system_uptime():
    try:
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        days = int(uptime_seconds // (24 * 3600))
        hours = int((uptime_seconds % (24 * 3600)) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        return f"Thời gian hoạt động: {days} ngày, {hours} giờ, {minutes} phút."
    except Exception as e:
        logging.error(f"Lỗi lấy thời gian hoạt động: {str(e)}")
        return f"Lỗi lấy thời gian hoạt động: {str(e)}"

def speak(tactics_instance, text):
    if not tactics_instance.speech_enabled:
        return
    try:
        cache_key = text[:50].replace(" ", "_")
        if cache_key in tactics_instance.audio_cache:
            temp_file = tactics_instance.audio_cache[cache_key]
            if os.path.exists(temp_file):
                play_audio(tactics_instance, temp_file)
                return
        filename = f"temp_{uuid.uuid4()}.mp3"
        temp_file = os.path.join(tempfile.gettempdir(), filename)
        retries = 2
        for attempt in range(retries):
            try:
                tts = gTTS(text=text, lang="vi", slow=False, tld="com.vn")
                tts.save(temp_file)
                break
            except Exception as e:
                if attempt == retries - 1:
                    logging.error(f"Lỗi tạo âm thanh gTTS: {str(e)}")
                    tactics_instance.conversation_history.append(("Hệ thống", f"Lỗi tạo âm thanh: {str(e)}.", datetime.now().strftime("%H:%M:%S")))
                    tactics_instance.update_conversation_display()
                    return
        if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
            logging.error("File MP3 không được tạo hoặc rỗng")
            tactics_instance.conversation_history.append(("Hệ thống", "Lỗi tạo file âm thanh.", datetime.now().strftime("%H:%M:%S")))
            tactics_instance.update_conversation_display()
            return
        tactics_instance.audio_cache[cache_key] = temp_file
        play_audio(tactics_instance, temp_file)
    except Exception as e:
        logging.error(f"Lỗi âm thanh chung: {str(e)}")
        tactics_instance.conversation_history.append(("Hệ thống", f"Lỗi hệ thống âm thanh: {str(e)}.", datetime.now().strftime("%H:%M:%S")))
        tactics_instance.update_conversation_display()

def play_audio(tactics_instance, temp_file):
    try:
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.set_volume(tactics_instance.volume)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
    except Exception as e:
        logging.error(f"Lỗi phát âm thanh Pygame: {str(e)}")
        try:
            if platform.system() == "Windows":
                subprocess.run(["start", "", temp_file], shell=True)
            elif platform.system() == "Darwin":
                subprocess.run(["afplay", temp_file])
            elif platform.system() == "Linux":
                subprocess.run(["aplay", temp_file])
            pygame.time.wait(3000)
        except Exception as e2:
            logging.error(f"Lỗi phát âm thanh dự phòng: {str(e2)}")
            tactics_instance.conversation_history.append(("Hệ thống", f"Lỗi phát âm thanh: {str(e)}.", datetime.now().strftime("%H:%M:%S")))
            tactics_instance.update_conversation_display()
    finally:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            if len(tactics_instance.audio_cache) > 10:
                oldest_key = next(iter(tactics_instance.audio_cache))
                os.remove(tactics_instance.audio_cache.pop(oldest_key))
        except Exception as e:
            logging.error(f"Lỗi xóa file tạm {temp_file}: {str(e)}")

def cleanup_temp_files(tactics_instance):
    try:
        temp_dir = tempfile.gettempdir()
        for file in os.listdir(temp_dir):
            if file.endswith(".mp3") and file.startswith("temp_"):
                try:
                    os.remove(os.path.join(temp_dir, file))
                except:
                    pass
    except Exception as e:
        logging.error(f"Lỗi dọn dẹp file tạm: {str(e)}")