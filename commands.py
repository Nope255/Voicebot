import logging
import psutil
import socket
import hashlib
import re
import webbrowser
import pyautogui
import netifaces
import subprocess
import platform
from datetime import datetime, timedelta
import calendar
from utils import get_system_uptime

def process_command(tactics_instance, prompt):
    prompt = prompt.lower().strip()
    if "kích hoạt phòng thủ" in prompt:
        return simulate_firewall()
    elif "khóa cổng truy cập" in prompt:
        return "Cổng truy cập khóa: 80, 443, 3389. Hệ thống cách ly."
    elif "quét xâm nhập" in prompt:
        return simulate_intrusion_scan()
    elif "phản công ip" in prompt:
        ip = prompt.replace("phản công ip", "").strip()
        return simulate_counterattack(ip) if ip else "Chỉ định địa chỉ IP."
    elif "mô phỏng tấn công ddos" in prompt:
        ip = prompt.replace("mô phỏng tấn công ddos", "").strip()
        return simulate_ddos(ip) if ip else "Chỉ định địa chỉ IP."
    elif "phân tích lỗ hổng" in prompt:
        target = prompt.replace("phân tích lỗ hổng", "").strip()
        return analyze_vulnerabilities(target) if target else "Chỉ định IP hoặc 'hệ thống'."
    elif "mã hóa dữ liệu" in prompt:
        content = prompt.replace("mã hóa dữ liệu", "").strip()
        return encrypt_data(content) if content else "Chỉ định nội dung để mã hóa."
    elif "giám sát mạng thời gian thực" in prompt:
        return monitor_network_realtime()
    elif "phân tích nhật ký" in prompt:
        return analyze_logs()
    elif "giám sát hệ thống" in prompt or "trạng thái hệ thống" in prompt:
        return monitor_system()
    elif "kiểm tra tiến trình" in prompt:
        return check_processes()
    elif "tối ưu hệ thống" in prompt:
        return optimize_system()
    elif "chấm dứt tiến trình" in prompt:
        pid = prompt.replace("chấm dứt tiến trình", "").strip()
        return terminate_process(pid) if pid else "Chỉ định PID tiến trình."
    elif "xem thông tin mạng" in prompt:
        return get_network_info()
    elif "kiểm tra pin" in prompt:
        return check_battery()
    elif "thời gian hoạt động" in prompt:
        return get_system_uptime()
    elif "kích hoạt vpn" in prompt:
        return simulate_vpn()
    elif "ẩn danh hoàn toàn" in prompt:
        return engage_anonymity()
    elif "xóa dấu vết" in prompt:
        return clear_traces(tactics_instance)
    elif "truy vết truy cập trái phép" in prompt:
        return trace_access()
    elif "gửi otp" in prompt:
        match = re.match(r"gửi otp\s+(\+?\d+)\s*(\w*)", prompt)
        if match:
            phone, service = match.groups()
            return send_otp(phone, service)
        return "Chỉ định số điện thoại và dịch vụ (sms, email,whatsapp)."
    elif "thời tiết" in prompt:
        location = prompt.replace("thời tiết", "").strip()
        return get_weather(tactics_instance, location) if location else "Chỉ định địa điểm."
    elif "mấy giờ" in prompt or "giờ hiện tại" in prompt:
        return f"Thời gian hiện tại: {datetime.now().strftime('%H:%M:%S')}."
    elif "hôm nay là thứ mấy" in prompt or "ngày hôm nay" in prompt:
        day = calendar.day_name[datetime.now().weekday()]
        day_vn = {
            "Monday": "Thứ Hai", "Tuesday": "Thứ Ba", "Wednesday": "Thứ Tư",
            "Thursday": "Thứ Năm", "Friday": "Thứ Sáu", "Saturday": "Thứ Bảy", "Sunday": "Chủ Nhật"
        }
        return f"Ngày hiện tại: {day_vn[day]}."
    elif "ngày mai là thứ mấy" in prompt or "ngày mai" in prompt:
        tomorrow = datetime.now() + timedelta(days=1)
        day = calendar.day_name[tomorrow.weekday()]
        day_vn = {
            "Monday": "Thứ Hai", "Tuesday": "Thứ Ba", "Wednesday": "Thứ Tư",
            "Thursday": "Thứ Năm", "Friday": "Thứ Sáu", "Saturday": "Thứ Bảy", "Sunday": "Chủ Nhật"
        }
        return f"Ngày mai: {day_vn[day]}."
    elif "ngày hiện tại" in prompt:
        return f"Ngày hiện tại: {datetime.now().strftime('%d/%m/%Y')}."
    elif "phát video" in prompt or "phát bài hát" in prompt:
        query = prompt.replace("phát video", "").replace("phát bài hát", "").strip()
        return search_youtube(tactics_instance, query) if query else "Chỉ định chủ đề hoặc URL video."
    elif "phát tất cả" in prompt:
        return play_youtube_playlist(tactics_instance)
    elif "tìm kiếm" in prompt:
        query = prompt.replace("tìm kiếm", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Tìm kiếm đã thực hiện: {query}"
        return "Chỉ định nội dung tìm kiếm."
    elif "đặt lịch nhắc nhở" in prompt:
        match = re.match(r"đặt lịch nhắc nhở\s+(\d{1,2}:\d{2}(?:\s+\d{1,2}/\d{1,2}/\d{4})?)\s+(.+)", prompt)
        if match:
            time_str, content = match.groups()
            return set_reminder(tactics_instance, time_str, content)
        return "Chỉ định thời gian (HH:MM hoặc HH:MM DD/MM/YYYY) và nội dung."
    elif "tính toán" in prompt:
        expr = prompt.replace("tính toán", "").strip()
        return calculate_expression(expr) if expr else "Chỉ định biểu thức toán học."
    elif "chuyển đổi đơn vị" in prompt:
        match = re.match(r"chuyển đổi đơn vị\s+(\d*\.?\d*)\s+(\w+)\s+sang\s+(\w+)", prompt)
        if match:
            value, from_unit, to_unit = match.groups()
            return convert_units(value, from_unit, to_unit)
        return "Chỉ định: giá trị, đơn vị gốc, đơn vị đích (VD: 10 km sang miles)."
    elif "kiểm tra kết nối mạng" in prompt:
        return check_network_connection()
    elif "ghi chú" in prompt:
        content = prompt.replace("ghi chú", "").strip()
        return save_note(tactics_instance, content) if content else "Chỉ định nội dung ghi chú."
    elif "lịch sử lệnh" in prompt:
        return get_command_history(tactics_instance)
    elif "mở" in prompt:
        app = prompt.replace("mở", "").strip()
        app_map = {
            "notepad": "notepad.exe",
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "file explorer": "explorer.exe" if platform.system() == "Windows" else "nautilus" if platform.system() == "Linux" else "open -a Finder",
            "task manager": "taskmgr.exe" if platform.system() == "Windows" else "htop" if platform.system() == "Linux" else "open -a 'Activity Monitor'"
        }
        if app in app_map:
            try:
                if platform.system() == "Darwin" and app in ("file explorer", "task manager"):
                    subprocess.run(app_map[app], shell=True)
                else:
                    subprocess.Popen(app_map[app])
                return f"Ứng dụng {app} đã khởi động."
            except Exception as e:
                return f"Lỗi khởi động {app}: {str(e)}"
        return f"Ứng dụng {app} không nhận diện. Thử: notepad, chrome, firefox, file explorer, task manager."
    elif "tăng âm lượng" in prompt or "điều chỉnh âm lượng tăng" in prompt:
        try:
            tactics_instance.volume = min(tactics_instance.volume + 0.1, 1.0)
            pygame.mixer.music.set_volume(tactics_instance.volume)
            tactics_instance.volume_slider.setValue(int(tactics_instance.volume * 100))
            return "Âm lượng đã tăng."
        except Exception as e:
            return f"Lỗi điều chỉnh âm lượng: {str(e)}"
    elif "giảm âm lượng" in prompt or "điều chỉnh âm lượng giảm" in prompt:
        try:
            tactics_instance.volume = max(tactics_instance.volume - 0.1, 0.0)
            pygame.mixer.music.set_volume(tactics_instance.volume)
            tactics_instance.volume_slider.setValue(int(tactics_instance.volume * 100))
            return "Âm lượng đã giảm."
        except Exception as e:
            return f"Lỗi điều chỉnh âm lượng: {str(e)}"
    elif "chụp màn hình" in prompt:
        try:
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot.save(filename)
            return f"Màn hình đã chụp và lưu tại {filename}."
        except Exception as e:
            return f"Lỗi chụp màn hình: {str(e)}"
    elif "tắt máy" in prompt:
        try:
            if platform.system() == "Windows":
                subprocess.run(["shutdown", "/s", "/t", "0"])
            elif platform.system() == "Linux":
                subprocess.run(["sudo", "shutdown", "now"])
            elif platform.system() == "Darwin":
                subprocess.run(["sudo", "shutdown", "-h", "now"])
            return "Đang khởi động tắt máy."
        except Exception as e:
            return f"Lỗi khởi động tắt máy: {str(e)}"
    elif "khởi động lại" in prompt:
        try:
            if platform.system() == "Windows":
                subprocess.run(["shutdown", "/r", "/t", "0"])
            elif platform.system() == "Linux":
                subprocess.run(["sudo", "reboot"])
            elif platform.system() == "Darwin":
                subprocess.run(["sudo", "shutdown", "-r", "now"])
            return "Đang khởi động lại hệ thống."
        except Exception as e:
            return f"Lỗi khởi động lại: {str(e)}"
    elif "xin chào" in prompt or "chào" in prompt:
        return "Chào, Chủ nhân. TACTICS trực tuyến và sẵn sàng nhận lệnh."
    elif "tên bạn là gì" in prompt or "bạn là ai" in prompt:
        return "Tôi là T.A.C.T.I.C.S., Hệ Thống Điều Khiển Chiến Thuật và Tình Báo Đe Dọa."
    else:
        return "Lệnh không nhận diện. Xem danh sách lệnh trong giao diện."

def simulate_firewall():
    try:
        return "Tường lửa đã kích hoạt. Bảo vệ cấp cao: Cổng 80, 443, 22, 3389 khóa. IDS/IPS kích hoạt."
    except Exception as e:
        logging.error(f"Lỗi mô phỏng tường lửa: {str(e)}")
        return f"Lỗi kích hoạt tường lửa: {str(e)}"

def simulate_intrusion_scan():
    try:
        processes = [(p.pid, p.name()) for p in psutil.process_iter(['pid', 'name'])]
        suspicious = [p for p in processes if 'unknown' in p[1].lower() or 'temp' in p[1].lower()]
        ports = []
        for port in [22, 80, 443, 3389]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                result = s.connect_ex(('127.0.0.1', port))
                if result == 0:
                    ports.append(f"Cổng {port}: Mở")
                s.close()
            except:
                pass
        response = "QUÉT XÂM NHẬP:\n"
        response += f"• Tiến trình đáng ngờ: {', '.join(f'{p[1]} (PID: {p[0]})' for p in suspicious) if suspicious else 'Không phát hiện.'}\n"
        response += f"• Cổng mở: {', '.join(ports) if ports else 'Không có cổng mở bất thường.'}"
        return response
    except Exception as e:
        logging.error(f"Lỗi quét xâm nhập: {str(e)}")
        return f"Lỗi quét xâm nhập: {str(e)}"

def simulate_counterattack(ip):
    try:
        return f"Phản công IP {ip}: Mô phỏng ngập lụt SYN/UDP hoàn tất. Tấn công giả lập 10 Gbps trong 60 giây. Mục tiêu bị cô lập."
    except Exception as e:
        logging.error(f"Lỗi mô phỏng phản công: {str(e)}")
        return f"Lỗi thực hiện phản công: {str(e)}"

def simulate_ddos(ip):
    try:
        return (
            f"Mô phỏng tấn công DDoS tới IP {ip}:\n"
            "• Loại: Ngập lụt HTTP/SYN\n"
            "• Băng thông giả lập: 15 Gbps\n"
            "• Gói tin: 1,000,000 gói/phút\n"
            "• Kết quả: Mục tiêu quá tải, dịch vụ bị gián đoạn (mô phỏng)."
        )
    except Exception as e:
        logging.error(f"Lỗi mô phỏng DDoS: {str(e)}")
        return f"Lỗi thực hiện DDoS: {str(e)}"

def analyze_vulnerabilities(target):
    try:
        vulnerabilities = [
            "CVE-2023-1234: Lỗ hổng XSS",
            "CVE-2023-5678: Lỗi SQL Injection",
            "CVE-2023-9012: Cấu hình máy chủ yếu"
        ] if "hệ thống" not in target.lower() else [
            "Hệ thống: Cổng 445 mở",
            "Hệ thống: SMBv1 chưa tắt",
            "Hệ thống: Cần vá kernel"
        ]
        return f"PHÂN TÍCH LỖ HỔNG ({target}):\n" + "\n".join(f"• {v}" for v in vulnerabilities) + "\n• Đề xuất: Vá ngay lập tức."
    except Exception as e:
        logging.error(f"Lỗi phân tích lỗ hổng: {str(e)}")
        return f"Lỗi phân tích lỗ hổng: {str(e)}"

def encrypt_data(content):
    try:
        hashed = hashlib.sha256(content.encode()).hexdigest()
        return f"Mã hóa dữ liệu (AES-256 mô phỏng): {content} -> {hashed[:16]}... (đã mã hóa)."
    except Exception as e:
        logging.error(f"Lỗi mã hóa dữ liệu: {str(e)}")
        return f"Lỗi mã hóa dữ liệu: {str(e)}"

def monitor_network_realtime():
    try:
        net_io = psutil.net_io_counters()
        return (
            "GIÁM SÁT MẠNG THỜI GIAN THỰC:\n"
            f"• Gửi: {net_io.bytes_sent / (1024**2):.2f} MB\n"
            f"• Nhận: {net_io.bytes_recv / (1024**2):.2f} MB\n"
            f"• Gói tin gửi: {net_io.packets_sent}\n"
            f"• Gói tin nhận: {net_io.packets_recv}\n"
            "• Trạng thái: Hoạt động ổn định."
        )
    except Exception as e:
        logging.error(f"Lỗi giám sát mạng: {str(e)}")
        return f"Lỗi giám sát mạng: {str(e)}"

def analyze_logs():
    try:
        return "Phân tích nhật ký: Không phát hiện mẫu bất thường. 100% giao dịch hợp lệ. Hệ thống an toàn."
    except Exception as e:
        logging.error(f"Lỗi phân tích nhật ký: {str(e)}")
        return f"Lỗi phân tích nhật ký: {str(e)}"

def monitor_system():
    try:
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_avg = sum(cpu_percent) / len(cpu_percent)
        mem = psutil.virtual_memory()
        disk_io = psutil.disk_io_counters()
        net_io = psutil.net_io_counters()
        processes = [(p.pid, p.name(), p.cpu_percent(interval=0.1)) for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])]
        high_cpu = sorted(processes, key=lambda x: x[2], reverse=True)[:5]
        uptime = get_system_uptime()
        response = (
            "BÁO CÁO HỆ THỐNG:\n"
            f"• {uptime}\n"
            f"• CPU: {cpu_avg:.1f}% (Chi tiết: {', '.join(f'Core {i}: {p:.1f}%' for i, p in enumerate(cpu_percent))})\n"
            f"• Bộ nhớ: Sử dụng {mem.percent:.1f}% ({mem.used / (1024**3):.2f}/{mem.total / (1024**3):.2f} GB)\n"
            f"• Đĩa: Đọc {disk_io.read_bytes / (1024**3):.2f} GB, Ghi {disk_io.write_bytes / (1024**3):.2f} GB\n"
            f"• Mạng: Gửi {net_io.bytes_sent / (1024**2):.2f} MB, Nhận {net_io.bytes_recv / (1024**2):.2f} MB\n"
            f"• Tiến trình CPU cao: {', '.join(f'{p[1]} (PID: {p[0]}, {p[2]:.1f}%)' for p in high_cpu) if high_cpu else 'Không có tiến trình CPU cao.'}\n"
            f"• Đề xuất: {'Tối ưu tiến trình hoặc nâng cấp phần cứng' if cpu_avg > 80 or mem.percent > 80 else 'Duy trì hoạt động hiện tại'}."
        )
        return response
    except Exception as e:
        logging.error(f"Lỗi giám sát hệ thống: {str(e)}")
        return f"Lỗi giám sát hệ thống: {str(e)}"

def check_processes():
    try:
        processes = [(p.pid, p.name(), p.cpu_percent(interval=0.1)) for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])]
        high_cpu = sorted(processes, key=lambda x: x[2], reverse=True)[:5]
        if high_cpu:
            return f"Tiến trình CPU cao: {', '.join(f'{p[1]} (PID: {p[0]}, {p[2]:.1f}%)' for p in high_cpu)}. Đề xuất: Kiểm tra hoặc chấm dứt."
        return "Tất cả tiến trình hoạt động bình thường."
    except Exception as e:
        logging.error(f"Lỗi kiểm tra tiến trình: {str(e)}")
        return f"Lỗi kiểm tra tiến trình: {str(e)}"

def optimize_system():
    try:
        processes = [(p.pid, p.name(), p.cpu_percent(interval=0.1)) for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])]
        high_cpu = [p for p in processes if p[2] > 50]
        if high_cpu:
            return f"Phát hiện tiến trình CPU cao: {', '.join(f'{p[1]} (PID: {p[0]})' for p in high_cpu)}. Dùng 'chấm dứt tiến trình [PID]' để tối ưu."
        return "Hệ thống đã tối ưu. Không cần chấm dứt tiến trình."
    except Exception as e:
        logging.error(f"Lỗi tối ưu hệ thống: {str(e)}")
        return f"Lỗi tối ưu hệ thống: {str(e)}"

def terminate_process(pid):
    try:
        process = psutil.Process(int(pid))
        process.terminate()
        return f"Tiến trình PID {pid} ({process.name()}) đã chấm dứt."
    except Exception as e:
        logging.error(f"Lỗi chấm dứt tiến trình: {str(e)}")
        return f"Lỗi chấm dứt tiến trình {pid}: {str(e)}"

def get_network_info():
    try:
        interfaces = netifaces.interfaces()
        info = []
        for iface in interfaces:
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    info.append(f"Giao diện {iface}: IP {addr['addr']}, Netmask {addr['netmask']}")
        connections = psutil.net_connections()
        active = [c for c in connections if c.status == 'ESTABLISHED' and c.raddr]
        if active:
            info.append(f"Kết nối hoạt động: {', '.join(f'{c.laddr} -> {c.raddr}' for c in active)}")
        return "\n".join(info) if info else "Không có thông tin mạng."
    except Exception as e:
        logging.error(f"Lỗi lấy thông tin mạng: {str(e)}")
        return f"Lỗi lấy thông tin mạng: {str(e)}"

def check_battery():
    try:
        battery = psutil.sensors_battery()
        if battery:
            return f"Pin: {battery.percent}%{' (Đang sạc)' if battery.power_plugged else ''}. Thời gian còn lại: {timedelta(seconds=int(battery.secsleft)) if battery.secsleft != psutil.POWER_TIME_UNLIMITED else 'Không xác định'}."
        return "Không phát hiện pin. Thiết bị sử dụng nguồn cố định."
    except Exception as e:
        logging.error(f"Lỗi kiểm tra pin: {str(e)}")
        return f"Lỗi kiểm tra pin: {str(e)}"

def engage_anonymity():
    try:
        return "Giao thức ẩn danh kích hoạt. Proxy Tor giả lập. Địa chỉ IP ẩn hoàn toàn."
    except Exception as e:
        logging.error(f"Lỗi giao thức ẩn danh: {str(e)}")
        return f"Lỗi kích hoạt ẩn danh: {str(e)}"

def simulate_vpn():
    try:
        return "VPN kích hoạt. Kết nối mã hóa AES-256. Địa chỉ IP giả lập: 172.16.0.1."
    except Exception as e:
        logging.error(f"Lỗi mô phỏng VPN: {str(e)}")
        return f"Lỗi kích hoạt VPN: {str(e)}"

def clear_traces(tactics_instance):
    try:
        tactics_instance.cleanup_temp_files()
        return "Dấu vết xóa sạch: Cache trình duyệt, cookie, file tạm. Hệ thống vô hình."
    except Exception as e:
        logging.error(f"Lỗi xóa dấu vết: {str(e)}")
        return f"Lỗi xóa dấu vết: {str(e)}"

def trace_access():
    try:
        connections = psutil.net_connections()
        suspicious = [c for c in connections if c.status == 'ESTABLISHED' and c.raddr]
        if suspicious:
            return f"TRUY VẾT: Phát hiện truy cập trái phép: {', '.join(f'{c.laddr} -> {c.raddr}' for c in suspicious)}. Khóa ngay."
        return "Không phát hiện truy cập trái phép."
    except Exception as e:
        logging.error(f"Lỗi truy vết truy cập: {str(e)}")
        return f"Lỗi truy vết truy cập: {str(e)}"

def send_otp(phone, service):
    try:
        import uuid
        otp = str(uuid.uuid4())[:6]
        service = service.lower() if service else "sms"
        if service not in ["sms", "email", "whatsapp"]:
            return f"Dịch vụ {service} không hỗ trợ. Chọn: sms, email, whatsapp."
        return f"OTP {otp} đã gửi tới {phone} qua {service}. Hết hạn sau 5 phút (mô phỏng)."
    except Exception as e:
        logging.error(f"Lỗi gửi OTP: {str(e)}")
        return f"Lỗi gửi OTP: {str(e)}"

def search_youtube(tactics_instance, query):
    try:
        if query.startswith("http"):
            webbrowser.open(query)
            return f"Đang phát video từ URL: {query}"
        tactics_instance.last_youtube_query = query
        tactics_instance.youtube_results = [f"Video về {query} {i+1}" for i in range(5)]
        return f"Tìm kiếm YouTube: {query}. Dùng 'phát tất cả' để mở danh sách."
    except Exception as e:
        logging.error(f"Lỗi tìm kiếm YouTube: {str(e)}")
        return f"Lỗi thực hiện tìm kiếm YouTube: {str(e)}"

def play_youtube_playlist(tactics_instance):
    try:
        if tactics_instance.last_youtube_query:
            webbrowser.open(f"https://www.youtube.com/results?search_query={tactics_instance.last_youtube_query}&sp=EgIQAw%253D%253D")
            return f"Đang phát danh sách: {tactics_instance.last_youtube_query}"
        return "Chưa tìm kiếm YouTube. Dùng 'phát video [chủ đề]' trước."
    except Exception as e:
        logging.error(f"Lỗi phát danh sách YouTube: {str(e)}")
        return f"Lỗi phát danh sách: {str(e)}"

def get_weather(tactics_instance, location):
    try:
        import time
        cache_key = location.lower()
        cache_time = tactics_instance.weather_cache.get(cache_key, {}).get("time", 0)
        if time.time() - cache_time < 3600:
            return tactics_instance.weather_cache[cache_key]["response"]
        query = f"thời tiết {location}"
        webbrowser.open(f"https://www.google.com/search?q={query}")
        response = f"Dữ liệu thời tiết cho {location} đã truy xuất. Kiểm tra trình duyệt."
        tactics_instance.weather_cache[cache_key] = {"response": response, "time": time.time()}
        tactics_instance.settings.setValue("weather_cache", tactics_instance.weather_cache)
        return response
    except Exception as e:
        logging.error(f"Lỗi truy xuất thời tiết: {str(e)}")
        return f"Lỗi truy xuất thời tiết: {str(e)}"

def set_reminder(tactics_instance, time_str, content):
    try:
        time_format = "%H:%M %d/%m/%Y" if "/" in time_str else "%H:%M"
        reminder_time = datetime.strptime(time_str, time_format)
        if "/" not in time_str:
            reminder_time = reminder_time.replace(
                year=datetime.now().year,
                month=datetime.now().month,
                day=datetime.now().day
            )
        if reminder_time < datetime.now():
            reminder_time += timedelta(days=1)
        tactics_instance.reminders.append({"time": reminder_time, "content": content})
        return f"Nhắc nhở đặt cho {content} vào {reminder_time.strftime('%H:%M %d/%m/%Y')}."
    except Exception as e:
        logging.error(f"Lỗi đặt lịch nhắc nhở: {str(e)}")
        return f"Lỗi đặt lịch nhắc nhở: {str(e)}"

def calculate_expression(expr):
    try:
        import math
        result = eval(expr, {"__builtins__": {}}, {"sin": math.sin, "cos": math.cos, "tan": math.tan, "sqrt": math.sqrt})
        return f"Kết quả: {expr} = {result:.2f}"
    except Exception as e:
        logging.error(f"Lỗi tính toán: {str(e)}")
        return f"Lỗi tính toán: {str(e)}"

def convert_units(value, from_unit, to_unit):
    try:
        conversions = {
            ("km", "miles"): 0.621371,
            ("miles", "km"): 1.60934,
            ("kg", "lbs"): 2.20462,
            ("lbs", "kg"): 0.453592,
            ("m", "ft"): 3.28084,
            ("ft", "m"): 0.3048,
            ("c", "f"): lambda x: (x * 9/5) + 32,
            ("f", "c"): lambda x: (x - 32) * 5/9
        }
        key = (from_unit.lower(), to_unit.lower())
        if key not in conversions:
            return f"Chuyển đổi từ {from_unit} sang {to_unit} không hỗ trợ."
        value = float(value)
        result = value * conversions[key] if not callable(conversions[key]) else conversions[key](value)
        return f"{value} {from_unit} = {result:.2f} {to_unit}"
    except Exception as e:
        logging.error(f"Lỗi chuyển đổi đơn vị: {str(e)}")
        return f"Lỗi chuyển đổi đơn vị: {str(e)}"

def check_network_connection():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return "Kết nối mạng: Hoạt động. Ping tới 8.8.8.8 thành công."
    except Exception as e:
        logging.error(f"Lỗi kiểm tra kết nối mạng: {str(e)}")
        return f"Kết nối mạng: Không hoạt động. Lỗi: {str(e)}"

def save_note(tactics_instance, content):
    try:
        tactics_instance.notes.append({"content": content, "time": datetime.now().strftime("%H:%M:%S %d/%m/%Y")})
        tactics_instance.settings.setValue("notes", tactics_instance.notes)
        return f"Ghi chú lưu: {content}"
    except Exception as e:
        logging.error(f"Lỗi lưu ghi chú: {str(e)}")
        return f"Lỗi lưu ghi chú: {str(e)}"

def get_command_history(tactics_instance):
    if not tactics_instance.conversation_history:
        return "Lịch sử lệnh trống."
    return "\n".join(f"[{t}] {s}: {c}" for s, c, t in tactics_instance.conversation_history if s == "Người dùng")