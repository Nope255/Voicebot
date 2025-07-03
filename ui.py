from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QLineEdit, QCheckBox, QSlider, QPushButton, QWidget, QScrollArea
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPixmap
import os

def setup_ui(tactics_instance):
    tactics_instance.setWindowTitle("T.A.C.T.I.C.S. - Hệ Thống Chiến Thuật")
    tactics_instance.setGeometry(100, 100, 1200, 850)
    tactics_instance.setMinimumSize(900, 650)
    tactics_instance.setStyleSheet(get_stylesheet("dark"))

    main_layout = QVBoxLayout()
    main_layout.setSpacing(12)
    main_layout.setContentsMargins(20, 20, 20, 20)

    header_layout = QHBoxLayout()
    header_layout.setSpacing(12)

    logo = QLabel()
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        logo.setPixmap(QPixmap(logo_path).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
    else:
        logo.setText("T")
        logo.setFont(QFont("Inter", 24, QFont.Weight.Bold))
        logo.setStyleSheet("color: #3b82f6; background: transparent; padding: 8px;")
    header_layout.addWidget(logo)

    title_label = QLabel("T.A.C.T.I.C.S.")
    title_label.setFont(QFont("Inter", 22, QFont.Weight.Bold))
    title_label.setStyleSheet("color: #3b82f6; background: transparent; padding: 8px;")
    header_layout.addWidget(title_label)

    tactics_instance.status_indicator = QLabel("●")
    tactics_instance.status_indicator.setFont(QFont("Inter", 16))
    tactics_instance.status_indicator.setStyleSheet("color: #22c55e; background: transparent; padding: 8px;")
    header_layout.addWidget(tactics_instance.status_indicator)
    header_layout.addStretch()
    main_layout.addLayout(header_layout)

    content_layout = QHBoxLayout()
    content_layout.setSpacing(12)

    tactics_instance.sidebar_container = QFrame()
    tactics_instance.sidebar_container.setObjectName("sidebar")
    tactics_instance.sidebar_container.setMinimumWidth(320)
    sidebar_layout = QVBoxLayout()
    sidebar_layout.setSpacing(8)
    sidebar_layout.setContentsMargins(15, 15, 15, 15)

    tactics_instance.sidebar_toggle = QPushButton("⫷")
    tactics_instance.sidebar_toggle.setFixedSize(30, 30)
    tactics_instance.sidebar_toggle.setStyleSheet("background-color: #3b82f6; color: white; border-radius: 5px; border: none; font-size: 14px;")
    tactics_instance.sidebar_toggle.clicked.connect(lambda: toggle_sidebar(tactics_instance))
    sidebar_layout.addWidget(tactics_instance.sidebar_toggle, alignment=Qt.AlignmentFlag.AlignRight)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setStyleSheet("border: none; background: transparent;")
    
    command_widget = QWidget()
    command_layout = QVBoxLayout()
    command_layout.setSpacing(8)
    
    command_header = QLabel("LỆNH HỖ TRỢ")
    command_header.setFont(QFont("Inter", 16, QFont.Weight.Bold))
    command_header.setStyleSheet("color: #60a5fa; padding: 8px; background: transparent;")
    command_layout.addWidget(command_header)

    tactics_instance.command_list = QLabel("""
        •➤ CHIẾN THUẬT:\n
          - Kích hoạt phòng thủ\n
          - Khóa cổng truy cập\n
          - Quét xâm nhập\n
          - Phản công IP [IP]\n
          - Phân tích nhật ký\n
          - Truy vết truy cập trái phép\n
          - Kích hoạt VPN\n
          - Tấn công DDoS [IP]\n
          - Phân tích lỗ hổng [IP/hệ thống]\n
          - Mã hóa dữ liệu [nội dung]\n
          - Giám sát mạng thời gian thực\n
        •➤ GIÁM SÁT:\n
          - Giám sát hệ thống\n
          - Kiểm tra tiến trình\n
          - Tối ưu hệ thống\n
          - Xem thông tin mạng\n
          - Kiểm tra pin\n
          - Thời gian hoạt động\n
        •➤ BẢO MẬT:\n
          - Ẩn danh hoàn toàn\n
          - Xóa dấu vết\n
          - Gửi OTP [số điện thoại] [dịch vụ]\n
        •➤ TIỆN ÍCH:\n
          - Thời tiết [địa điểm]\n
          - Giờ hiện tại\n
          - Ngày hôm nay\n
          - Ngày mai\n
          - Ngày hiện tại\n
          - Phát video [chủ đề/URL]\n
          - Phát tất cả\n
          - Tìm kiếm [nội dung]\n
          - Đặt lịch nhắc nhở [thời gian] [nội dung]\n
          - Tính toán [biểu thức]\n
          - Chuyển đổi đơn vị [giá trị] [đơn vị] sang [đơn vị]\n
          - Kiểm tra kết nối mạng\n
          - Ghi chú [nội dung]\n
          - Lịch sử lệnh\n
        •➤ ỨNG DỤNG:\n
          - Mở notepad\n
          - Mở chrome\n
          - Mở file explorer\n
          - Mở task manager\n
        •➤ HỆ THỐNG:\n
          - Trạng thái hệ thống\n
          - Chụp màn hình\n
          - Tắt máy\n
          - Khởi động lại\n
          - Điều chỉnh âm lượng [tăng/giảm]
        """)
    tactics_instance.command_list.setFont(QFont("Inter", 11))
    tactics_instance.command_list.setWordWrap(True)
    tactics_instance.command_list.setStyleSheet("padding: 12px; color: #d1d5db; background: rgba(31, 41, 55, 0.8); border-radius: 8px;")
    command_layout.addWidget(tactics_instance.command_list)
    command_widget.setLayout(command_layout)
    scroll_area.setWidget(command_widget)
    sidebar_layout.addWidget(scroll_area)
    
    tactics_instance.sidebar_container.setLayout(sidebar_layout)
    content_layout.addWidget(tactics_instance.sidebar_container)

    tactics_instance.main_content_layout = QVBoxLayout()
    tactics_instance.main_content_layout.setSpacing(12)

    tactics_instance.back_button = QPushButton("⫸")
    tactics_instance.back_button.setFont(QFont("Inter", 12))
    tactics_instance.back_button.setStyleSheet("""
        padding: 10px; 
        border-radius: 8px; 
        background-color: #3b82f6; 
        color: white; 
        font-weight: bold; 
        border: 1px solid #3b82f6;
        transition: all 0.3s ease;
        """)
    tactics_instance.back_button.clicked.connect(lambda: toggle_sidebar(tactics_instance))
    tactics_instance.back_button.hide()
    tactics_instance.main_content_layout.addWidget(tactics_instance.back_button, alignment=Qt.AlignmentFlag.AlignLeft)

    tactics_instance.status_label = QLabel("Trạng thái hệ thống: Hoạt động bình thường. Đang chờ lệnh.")
    tactics_instance.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    tactics_instance.status_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
    tactics_instance.status_label.setStyleSheet("padding: 15px; border-radius: 8px; background-color: rgba(31, 41, 55, 0.8); color: #60a5fa; border: 1px solid #3b82f6;")
    tactics_instance.main_content_layout.addWidget(tactics_instance.status_label)

    tactics_instance.conversation_display = QTextEdit()
    tactics_instance.conversation_display.setReadOnly(True)
    tactics_instance.conversation_display.setFont(QFont("Inter", 12))
    tactics_instance.conversation_display.setStyleSheet("border-radius: 8px; padding: 15px; background-color: rgba(17, 24, 39, 0.8); color: #f9fafb; border: 1px solid #374151;")
    tactics_instance.main_content_layout.addWidget(tactics_instance.conversation_display)

    input_panel = QFrame()
    input_panel.setStyleSheet("background-color: rgba(31, 41, 55, 0.8); border-radius: 8px; padding: 12px;")
    input_layout = QVBoxLayout()
    input_layout.setSpacing(8)

    tactics_instance.text_input = QLineEdit()
    tactics_instance.text_input.setPlaceholderText("Nhập lệnh tại đây...")
    tactics_instance.text_input.setFont(QFont("Inter", 13))
    tactics_instance.text_input.setStyleSheet("""
        padding: 12px; 
        border-radius: 8px; 
        border: 1px solid #374151; 
        background-color: rgba(17, 24, 39, 0.8); 
        color: #f9fafb;
        """)
    tactics_instance.text_input.returnPressed.connect(tactics_instance.process_text_input)
    input_layout.addWidget(tactics_instance.text_input)

    controls_layout = QHBoxLayout()
    controls_layout.setSpacing(10)

    tactics_instance.speech_toggle = QCheckBox("Phản hồi giọng nói")
    tactics_instance.speech_toggle.setChecked(True)
    tactics_instance.speech_toggle.setFont(QFont("Inter", 12))
    tactics_instance.speech_toggle.stateChanged.connect(tactics_instance.toggle_speech)
    controls_layout.addWidget(tactics_instance.speech_toggle)

    controls_layout.addWidget(QLabel("Âm lượng:", styleSheet="color: #f9fafb; font-size: 12px; font-family: 'Inter';"))
    tactics_instance.volume_slider = QSlider(Qt.Orientation.Horizontal)
    tactics_instance.volume_slider.setRange(0, 100)
    tactics_instance.volume_slider.setValue(100)
    tactics_instance.volume_slider.setStyleSheet("""
        QSlider::groove:horizontal {
            height: 8px;
            background: #374151;
            border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #22c55e;
            border: 1px solid #4ade80;
            width: 20px;
            margin: -6px 0;
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        QSlider::handle:horizontal:hover {
            background: #4ade80;
            transform: scale(1.1);
        }
        """)
    tactics_instance.volume_slider.valueChanged.connect(tactics_instance.update_volume)
    controls_layout.addWidget(tactics_instance.volume_slider)

    button_layout = QHBoxLayout()
    button_layout.setSpacing(10)
    tactics_instance.listen_button = QPushButton("🎙️ Nhập giọng nói")
    tactics_instance.listen_button.clicked.connect(lambda: start_listening(tactics_instance))
    tactics_instance.listen_button.setFont(QFont("Inter", 13, QFont.Weight.Bold))
    tactics_instance.listen_button.setStyleSheet("""
        padding: 10px; 
        border-radius: 0; 
        background-color: #3b82f6; 
        color: white; 
        font-weight: bold; 
        border: 1px solid #3b82f6;
        transition: all 0.3s ease;
        """)
    button_layout.addWidget(tactics_instance.listen_button)

    tactics_instance.clear_button = QPushButton("🧹 Xóa nhật ký")
    tactics_instance.clear_button.clicked.connect(tactics_instance.clear_conversation)
    tactics_instance.clear_button.setFont(QFont("Inter", 12))
    tactics_instance.clear_button.setStyleSheet("""
        padding: 12px; 
        border-radius: 8px; 
        background-color: #ef4444; 
        color: white; 
        font-weight: bold; 
        border: 1px solid #ef4444;
        transition: all 0.3s ease;
        """)
    button_layout.addWidget(tactics_instance.clear_button)

    input_layout.addLayout(controls_layout)
    input_layout.addLayout(button_layout)
    input_panel.setLayout(input_layout)
    tactics_instance.main_content_layout.addWidget(input_panel)

    content_layout.addLayout(tactics_instance.main_content_layout)
    main_layout.addLayout(content_layout)
    tactics_instance.setLayout(main_layout)

    tactics_instance.status_animation = QPropertyAnimation(tactics_instance.status_label, b"styleSheet")
    tactics_instance.status_animation.setDuration(600)
    tactics_instance.status_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

    tactics_instance.indicator_animation = QPropertyAnimation(tactics_instance.status_indicator, b"styleSheet")
    tactics_instance.indicator_animation.setDuration(1000)
    tactics_instance.indicator_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
    tactics_instance.indicator_animation.setStartValue("color: #22c55e; background: transparent; padding: 8px;")
    tactics_instance.indicator_animation.setEndValue("color: #4ade80; background: transparent; padding: 8px;")
    tactics_instance.indicator_animation.setLoopCount(-1)
    tactics_instance.indicator_animation.start()

    tactics_instance.conversation_animation = QPropertyAnimation(tactics_instance.conversation_display, b"styleSheet")
    tactics_instance.conversation_animation.setDuration(600)
    tactics_instance.conversation_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

    tactics_instance.listen_animation = QPropertyAnimation(tactics_instance.listen_button, b"styleSheet")
    tactics_instance.listen_animation.setDuration(400)
    tactics_instance.listen_animation.setEasingCurve(QEasingCurve.Type.InOutElastic)

def toggle_sidebar(tactics_instance):
    if tactics_instance.sidebar_container.isVisible():
        tactics_instance.sidebar_container.hide()
        tactics_instance.sidebar_toggle.setText("⫸")
        tactics_instance.back_button.show()
    else:
        tactics_instance.sidebar_container.show()
        tactics_instance.sidebar_toggle.setText("⫷")
        tactics_instance.back_button.hide()

def start_listening(tactics_instance):
    tactics_instance.listen_button.setText("🎙️ Đang nghe...")
    tactics_instance.listen_button.setFont(QFont("Inter", 14, QFont.Weight.Bold))
    tactics_instance.status_label.setText("Trạng thái: Đang nghe...")
    tactics_instance.listen_animation.setStartValue("padding: 10px; border-radius: 0; background-color: #3b82f6; color: white; font-weight: bold; border: 1px solid #3b82f6;")
    tactics_instance.listen_animation.setEndValue("padding: 10px; border-radius: 0; background-color: #f59e0b; color: white; font-weight: bold; border: 1px solid #f59e0b; transform: scale(1.1);")
    tactics_instance.listen_animation.setLoopCount(2)
    tactics_instance.listen_animation.start()
    try:
        tactics_instance.listen_and_respond()
    finally:
        tactics_instance.listen_button.setText("🎙️ Nhập giọng nói")
        tactics_instance.listen_button.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        tactics_instance.status_label.setText("Trạng thái hệ thống: Hoạt động bình thường. Đang chờ lệnh.")
        tactics_instance.listen_animation.setStartValue("padding: 10px; border-radius: 0; background-color: #f59e0b; color: white; font-weight: bold; border: 1px solid #f59e0b;")
        tactics_instance.listen_animation.setEndValue("padding: 10px; border-radius: 0; background-color: #3b82f6; color: white; font-weight: bold; border: 1px solid #3b82f6;")
        tactics_instance.listen_animation.setLoopCount(1)
        tactics_instance.listen_animation.start()

def get_stylesheet(theme):
    return """
        QWidget {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f172a, stop:1 #1e293b);
            color: #f9fafb;
            font-family: 'Inter', 'Roboto Mono', monospace;
        }
        QPushButton {
            background-color: #3b82f6;
            color: white;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #3b82f6;
            font-weight: bold;
            font-size: 13px;
            transition: all 0.3s ease;
        }
        QPushButton:hover {
            background-color: #2563eb;
            border: 1px solid #60a5fa;
            transform: scale(1.05);
        }
        QPushButton:pressed {
            background-color: #1e40af;
            border: 1px solid #1e40af;
            transform: scale(0.95);
        }
        QTextEdit, QLineEdit {
            background-color: rgba(17, 24, 39, 0.8);
            border: 1px solid #374151;
            color: #f9fafb;
            border-radius: 8px;
            padding: 12px;
            font-size: 13px;
            transition: border 0.3s ease;
        }
        QLineEdit:focus {
            border: 2px solid #06b6d4;
            background-color: rgba(17, 24, 39, 0.9);
        }
        QTextEdit {
            selection-background-color: #06b6d4;
            border: 1px solid #374151;
        }
        QSlider::groove:horizontal {
            height: 8px;
            background: #374151;
            border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #22c55e;
            border: 1px solid #4ade80;
            width: 20px;
            margin: -6px 0;
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        QSlider::handle:horizontal:hover {
            background: #4ade80;
            transform: scale(1.1);
        }
        QLabel {
            background: transparent;
            color: #f9fafb;
            font-size: 12px;
            font-family: 'Inter', 'Roboto Mono', monospace;
        }
        QFrame#sidebar {
            background-color: rgba(31, 41, 55, 0.8);
            border-radius: 8px;
            border: 1px solid #374151;
        }
        QCheckBox {
            color: #f9fafb;
            font-size: 12px;
            font-family: 'Inter', 'Roboto Mono', monospace;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 1px solid #374151;
            border-radius: 4px;
            background-color: rgba(17, 24, 39, 0.8);
        }
        QCheckBox::indicator:checked {
            background-color: #3b82f6;
            border: 1px solid #60a5fa;
        }
        QScrollArea {
            background: transparent;
            border: none;
        }
        QScrollBar:vertical {
            background: #1e293b;
            width: 10px;
            margin: 0;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background: #374151;
            border-radius: 5px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
            height: 0;
        }
    """