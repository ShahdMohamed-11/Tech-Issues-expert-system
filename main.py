from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton,
    QTextEdit, QScrollArea, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
from pyswip import Prolog
import sys

class DiagnosisApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Computer Diagnosis Expert System")
        self.setGeometry(200, 100, 800, 600)

        self.symptoms = [
            "slow_performance", "strange_noises", "corrupted_files", "boot_failure", "disk_errors",
            "frequent_crashes", "blue_screen", "random_restarts", "freezing", "memory_errors",
            "random_shutdowns", "system_freezes", "fans_running_loudly", "sluggish_performance", "hot_exterior",
            "failure_to_power_on", "system_shutdowns", "clicking_noises", "burning_smell",
            "pop_ups", "browser_redirection", "disabled_security", "unknown_processes",
            "device_malfunction", "device_not_recognized", "graphical_glitches", "audio_problems",
            "failure_to_boot", "beep_codes", "missing_hardware", "settings_reset", "incorrect_date_time",
            "intermittent_connectivity", "no_internet_access", "network_not_detected", "slow_connection", "driver_errors",
            "flickering_screen", "no_display", "distorted_colors", "dead_pixels", "vertical_lines",
            "unresponsive_keys", "stuck_keys", "ghost_typing", "delayed_response", "keyboard_not_detected",
            "display_artifacts", "screen_freezing", "display_driver_crashes", "blank_screen_with_system_running",
            "graphics_stuttering", "game_crashes", "gpu_fan_running_loudly", "performance_degradation_in_graphics", "display_corruption_under_load",
            "display_flickering", "color_distortion", "application_crashes_with_graphics", "black_screen_after_driver_update", "poor_3d_performance"
        ]

        self.prolog = Prolog()
        self.prolog.consult("info.pl")

        self.initUI()
        self.setStyleSheet(self.loadStyles())

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        title = QLabel("💻 Computer Diagnosis Expert System")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        main_layout.addWidget(title)

        instruction = QLabel("✔️ Select observed symptoms:")
        instruction.setFont(QFont("Segoe UI", 12))
        main_layout.addWidget(instruction)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        symptom_container = QWidget()
        symptom_layout = QVBoxLayout(symptom_container)
        symptom_layout.setSpacing(5)

        self.checkboxes = []
        for symptom in self.symptoms:
            cb = QCheckBox(symptom.replace("_", " ").capitalize())
            cb.setObjectName(symptom)
            cb.setFont(QFont("Segoe UI", 10))
            cb.setStyleSheet("padding: 5px;")
            self.checkboxes.append(cb)
            symptom_layout.addWidget(cb)

        scroll.setWidget(symptom_container)
        main_layout.addWidget(scroll, stretch=2)

        # Button row (Diagnose + Reset)
        button_layout = QHBoxLayout()
        diagnose_btn = QPushButton("Diagnose")
        diagnose_btn.clicked.connect(self.diagnose)

        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset)

        button_layout.addWidget(diagnose_btn)
        button_layout.addWidget(reset_btn)
        main_layout.addLayout(button_layout)

        # Results
        main_layout.addWidget(QLabel("📋 Diagnosis Results:"))
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setFont(QFont("Consolas", 10))
        main_layout.addWidget(self.result_box, stretch=1)

        self.setLayout(main_layout)

    def diagnose(self):
        selected = [cb.objectName() for cb in self.checkboxes if cb.isChecked()]
        if not selected:
            self.result_box.setText("⚠️ Please select at least one symptom.")
            return

        self.result_box.setText("🔎 Diagnosing...\n")
        query = f"diagnose_all([{','.join(selected)}], Results)."

        try:
            results = list(self.prolog.query(query))
            if not results:
                self.result_box.append("❌ No diagnosis found.")
                return

            prolog_result = results[0]["Results"]

            parsed_results = []
            for item in prolog_result:
                functor = str(item).strip()
                if functor.startswith("issue(") and functor.endswith(")"):
                    parts = functor[6:-1].split(",")
                    if len(parts) == 2:
                        issue = parts[0].strip()
                        percentage = float(parts[1].strip())
                        parsed_results.append((issue, percentage))

            if not parsed_results:
                self.result_box.append("❌ No matching issues found.")
                return

            parsed_results.sort(key=lambda x: x[1], reverse=True)
            output = ""
            for issue, percentage in parsed_results:
                name = issue.replace("_", " ").capitalize()
                output += f"✅ {name}: {percentage:.2f}% match\n"

            self.result_box.setText(output)

        except Exception as e:
            self.result_box.setText(f"❌ Error during diagnosis:\n{str(e)}")

    def reset(self):
        self.result_box.clear()
        for cb in self.checkboxes:
            cb.setChecked(False)

    def loadStyles(self):
        return """
            QWidget {
                background-color: #2b2b2b;
                color: #f0f0f0;
                font-family: 'Segoe UI';
            }
            QCheckBox {
                border-radius: 5px;
            }
            QPushButton {
                background-color: #5c8aff;
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a6eea;
            }
            QTextEdit {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 10px;
                border: 1px solid #444;
            }
            QLabel {
                margin-bottom: 4px;
            }
            QScrollArea {
                background-color: #2b2b2b;
                border: 1px solid #444;
                border-radius: 8px;
            }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiagnosisApp()
    window.show()
    sys.exit(app.exec())
