import logging
import asyncio
import speech_recognition as sr
from gtts import gTTS
import pygame
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QSettings
from ui import setup_ui
from commands import process_command
from utils import get_system_uptime, speak, cleanup_temp_files
from datetime import datetime
import schedule
import json

class TACTICS(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("xAI", "TACTICS")
        self.conversation_history = []
        self.current_language = "vi-VN"
        self.last_youtube_query = ""
        self.youtube_results = []
        self.user_habits = self.settings.value("user_habits", {}, type=dict)
        self.weather_cache = self.settings.value("weather_cache", {}, type=dict)
        self.notes = self.settings.value("notes", [], type=list)
        self.reminders = []
        self.automated_tasks = []
        self.speech_enabled = True
        self.volume = 1.0
        self.audio_cache = {}
        self.init_speech()
        setup_ui(self)
        self.init_automation()
        cleanup_temp_files(self)

    def init_speech(self):
        self.recognizer = sr.Recognizer()
        try:
            pygame.mixer.quit()
            pygame.mixer.init(frequency=44100, size=-16, channels=2)
        except Exception as e:
            logging.error(f"Lỗi khởi tạo âm thanh: {str(e)}")
            self.conversation_history.append(("Hệ thống", f"Lỗi khởi tạo âm thanh: {str(e)}. Phản hồi giọng nói bị vô hiệu hóa.", datetime.now().strftime("%H:%M:%S")))
            self.update_conversation_display()
            self.speech_enabled = False
            self.speech_toggle.setChecked(False)

    def init_automation(self):
        if self.user_habits.get("giám sát", 0) > 3:
            self.schedule_task("monitor_system", 300)
            logging.info("Lập lịch giám sát hệ thống tự động.")
        if self.user_habits.get("thời tiết", 0) > 3:
            self.schedule_task("weather_check", 3600)
            logging.info("Lập lịch kiểm tra thời tiết tự động.")
        asyncio.ensure_future(self.run_scheduler())

    async def run_scheduler(self):
        while True:
            schedule.run_pending()
            for reminder in self.reminders[:]:
                if datetime.now() >= reminder["time"]:
                    self.conversation_history.append(("Hệ thống", f"Nhắc nhở: {reminder['content']}", datetime.now().strftime("%H:%M:%S")))
                    self.update_conversation_display()
                    if self.speech_enabled:
                        speak(self, f"Nhắc nhở: {reminder['content']}")
                    self.reminders.remove(reminder)
            await asyncio.sleep(1)

    def schedule_task(self, task, interval_seconds):
        schedule.every(interval_seconds).seconds.do(self.automated_task, task)
        self.automated_tasks.append(task)

    def automated_task(self, task):
        if task == "monitor_system":
            response = process_command(self, "giám sát hệ thống")
            self.conversation_history.append(("Hệ thống", f"Báo cáo tự động: {response}", datetime.now().strftime("%H:%M:%S")))
            self.update_conversation_display()
            if self.speech_enabled:
                speak(self, response)
        elif task == "weather_check":
            response = process_command(self, "thời tiết hà nội")
            self.conversation_history.append(("Hệ thống", f"Báo cáo tự động: {response}", datetime.now().strftime("%H:%M:%S")))
            self.update_conversation_display()
            if self.speech_enabled:
                speak(self, response)

    def update_volume(self):
        self.volume = self.volume_slider.value() / 100
        try:
            pygame.mixer.music.set_volume(self.volume)
        except Exception as e:
            logging.error(f"Lỗi điều chỉnh âm lượng: {str(e)}")

    def toggle_speech(self):
        self.speech_enabled = self.speech_toggle.isChecked()

    def listen_and_respond(self):
        self.status_label.setText("Trạng thái: Đang kiểm tra micro...")
        logging.info("Kiểm tra thiết bị micro...")
        try:
            devices = sr.Microphone.list_microphone_names()
            logging.info(f"Microphones available: {devices}")
            if not devices:
                raise Exception("Không tìm thấy micro nào.")
        except Exception as e:
            error_msg = f"Lỗi micro: {str(e)}. Kiểm tra thiết bị micro."
            self.conversation_history.append(("Hệ thống", error_msg, datetime.now().strftime("%H:%M:%S")))
            self.update_conversation_display()
            self.status_label.setText("Trạng thái: Lỗi micro. Nhập lệnh văn bản.")
            self.listen_button.setEnabled(True)
            self.text_input.setEnabled(True)
            return
        self.status_label.setText("Trạng thái: Đang chờ lệnh giọng nói...")
        self.status_animation.setStartValue("background-color: #4ade80; padding: 12px; border-radius: 10px; border: 2px solid #3b82f6;")
        self.status_animation.setEndValue("background-color: #1e293b; padding: 12px; border-radius: 10px; border: 2px solid #3b82f6;")
        self.status_animation.start()
        self.listen_button.setEnabled(False)
        self.text_input.setEnabled(False)
        retries = 3
        for attempt in range(retries):
            try:
                with sr.Microphone() as source:
                    logging.info("Điều chỉnh nhiễu micro...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                    logging.info("Lắng nghe lệnh giọng nói...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                logging.info("Nhận diện giọng nói qua Google API...")
                text = self.recognizer.recognize_google(audio, language=self.current_language)
                self.process_input(text)
                break
            except Exception as e:
                logging.error(f"Thử lần {attempt + 1}: Lỗi nhận diện giọng nói: {str(e)}")
                if attempt == retries - 1:
                    error_msg = f"Lỗi nhận diện giọng nói: {str(e)}. Vui lòng nhập lệnh văn bản."
                    self.conversation_history.append(("Hệ thống", error_msg, datetime.now().strftime("%H:%M:%S")))
                    self.update_conversation_display()
                    self.status_label.setText("Trạng thái: Nhập lệnh văn bản để tiếp tục.")
                    self.status_animation.setStartValue("background-color: #f87171; padding: 12px; border-radius: 10px;")
                    self.status_animation.setEndValue("background-color: #1e293b; padding: 12px; border-radius: 10px;")
                    self.status_animation.start()
        self.listen_button.setEnabled(True)
        self.text_input.setEnabled(True)

    def process_text_input(self):
        text = self.text_input.text().strip()
        if text:
            self.process_input(text)
            self.text_input.clear()

    def process_input(self, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.conversation_history.append(("Chủ nhân", text, timestamp))
        self.update_conversation_display()
        self.update_user_habits(text)
        response = process_command(self, text)
        self.conversation_history.append(("TACTICS", response, timestamp))
        self.update_conversation_display()
        if self.speech_enabled:
            speak(self, response)
        self.status_label.setText("Trạng thái hệ thống: Hoạt động bình thường. Đang chờ lệnh.")
        logging.info(json.dumps({"user": text, "tactics": response}, ensure_ascii=False))

    def update_user_habits(self, command):
        command_key = command.lower().split()[0] if command else "không xác định"
        self.user_habits[command_key] = self.user_habits.get(command_key, 0) + 1
        self.settings.setValue("user_habits", self.user_habits)
        if (command_key in ("giám sát", "kiểm tra", "thời gian") and self.user_habits[command_key] > 3 and "monitor_system" not in self.automated_tasks):
            self.schedule_task("monitor_system", 300)
            logging.info("Lập lịch giám sát hệ thống tự động do tần suất sử dụng cao.")
        if (command_key == "thời tiết" and self.user_habits[command_key] > 3 and "weather_check" not in self.automated_tasks):
            self.schedule_task("weather_check", 3600)
            logging.info("Lập lịch kiểm tra thời tiết tự động do tần suất sử dụng cao.")

    def update_conversation_display(self):
        display_text = ""
        for speaker, text, timestamp in self.conversation_history:
            if speaker == "Chủ nhân":
                display_text += f"<span style='color: #60a5fa; font-weight: bold;'>[{timestamp}] Người dùng:</span> {text}<br><br>"
            elif speaker == "TACTICS":
                display_text += f"<span style='color: #4CAF50; font-weight: bold;'>[{timestamp}] TACTICS:</span> {text}<br><br>"
            else:
                display_text += f"<span style='color: #f87171; font-weight: bold;'>[{timestamp}] Hệ thống:</span> {text}<br><br>"
        self.conversation_display.setHtml(display_text)
        self.conversation_display.verticalScrollBar().setValue(
            self.conversation_display.verticalScrollBar().maximum()
        )

    def clear_conversation(self):
        self.conversation_history = []
        self.conversation_display.setHtml("")
        self.status_label.setText("Nhật ký đã xóa. Trạng thái hệ thống: Hoạt động bình thường.")
        self.status_animation.setStartValue("background-color: #4ade80; padding: 12px; border-radius: 10px; border: 2px solid #3b82f6;")
        self.status_animation.setEndValue("background-color: #1e293b; padding: 12px; border-radius: 10px; border: 2px solid #3b82f6;")
        self.status_animation.start()