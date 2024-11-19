import sys
import os
import platform
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QRadioButton, QButtonGroup, QLabel,
    QGroupBox, QMessageBox, QFileDialog, QStyleFactory
)
from PyQt6.QtCore import Qt
from ai_service import AIServiceProcessor
import logging
from config import (
    LOGGING_ENABLED,
    LOG_FILE_PATH,
    OUTPUT_DIR,
    DEBUG_MODE
)
from datetime import datetime

# Environment check and setup
def check_display():
    """Check if running in X11/Wayland environment and configure accordingly"""
    if platform.system() == "Linux":
        # Check if running in WSL
        is_wsl = "microsoft" in platform.uname().release.lower()
        if is_wsl:
            os.environ.setdefault('DISPLAY', ':0')
        
        # Check for X11 or Wayland
        if not os.environ.get('DISPLAY') and not os.environ.get('WAYLAND_DISPLAY'):
            logging.warning("No display found. If running remotely, ensure X11 forwarding is enabled.")
            return False
    return True

class AIGUI(QMainWindow):
    def __init__(self, headless=False):
        super().__init__()
        self.headless = headless
        self.setWindowTitle("AI Code Assistant")
        
        # Initialize AI Service
        self.current_service = "gemini"  # default service
        self.ai_processor = AIServiceProcessor(service=self.current_service)
        
        self.setup_logging()
        self.setup_style()
        self.create_gui()
        
        # Set window size
        self.setMinimumSize(800, 600)
        if not self.headless:
            self.center_window()
        
    def setup_style(self):
        """Setup application style based on environment"""
        if platform.system() == "Linux":
            # Use Fusion style for better remote display compatibility
            QApplication.setStyle(QStyleFactory.create('Fusion'))
            
            # Set up a simpler palette that works well with X11 forwarding
            palette = self.palette()
            self.setPalette(palette)

    def setup_logging(self):
        """Setup logging configuration"""
        if LOGGING_ENABLED:
            os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            logging.basicConfig(
                filename=LOG_FILE_PATH,
                level=logging.DEBUG if DEBUG_MODE else logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            self.logger = logging.getLogger(__name__)

    def create_gui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)  # Increase spacing for better visibility in remote display
        
        # Service selection group
        service_group = QGroupBox("AI Service")
        service_layout = QHBoxLayout()
        
        self.service_button_group = QButtonGroup(self)
        gemini_radio = QRadioButton("Gemini")
        openai_radio = QRadioButton("OpenAI")
        gemini_radio.setChecked(True)
        
        # Make radio buttons larger for easier remote interaction
        for radio in (gemini_radio, openai_radio):
            radio.setMinimumHeight(30)
        
        self.service_button_group.addButton(gemini_radio, 1)
        self.service_button_group.addButton(openai_radio, 2)
        self.service_button_group.buttonClicked.connect(self.change_service)
        
        service_layout.addWidget(gemini_radio)
        service_layout.addWidget(openai_radio)
        service_group.setLayout(service_layout)
        main_layout.addWidget(service_group)
        
        # Code input section
        code_group = QGroupBox("Original Code")
        code_layout = QVBoxLayout()
        
        self.code_textbox = QTextEdit()
        self.code_textbox.setMinimumHeight(150)  # Ensure minimum height for remote viewing
        code_button_layout = QHBoxLayout()
        
        # Create buttons with minimum size for better remote interaction
        load_button = self.create_button("Load Code", self.load_file)
        clear_code_button = self.create_button("Clear", self.code_textbox.clear)
        
        code_button_layout.addWidget(load_button)
        code_button_layout.addWidget(clear_code_button)
        
        code_layout.addWidget(self.code_textbox)
        code_layout.addLayout(code_button_layout)
        code_group.setLayout(code_layout)
        main_layout.addWidget(code_group)
        
        # Prompt input section
        prompt_group = QGroupBox("Modification Prompt")
        prompt_layout = QVBoxLayout()
        self.prompt_textbox = QTextEdit()
        self.prompt_textbox.setMinimumHeight(80)
        self.prompt_textbox.setMaximumHeight(100)
        prompt_layout.addWidget(self.prompt_textbox)
        prompt_group.setLayout(prompt_layout)
        main_layout.addWidget(prompt_group)
        
        # Process button
        process_button = self.create_button("Process", self.process_code)
        process_button.setMinimumHeight(40)  # Make process button larger
        main_layout.addWidget(process_button)
        
        # Output section
        output_group = QGroupBox("Modified Code")
        output_layout = QVBoxLayout()
        
        self.output_textbox = QTextEdit()
        self.output_textbox.setMinimumHeight(150)
        output_button_layout = QHBoxLayout()
        
        save_button = self.create_button("Save Code", self.save_file)
        clear_output_button = self.create_button("Clear", self.output_textbox.clear)
        copy_to_input_button = self.create_button("Copy to Input", self.copy_to_input)
        
        output_button_layout.addWidget(save_button)
        output_button_layout.addWidget(clear_output_button)
        output_button_layout.addWidget(copy_to_input_button)
        
        output_layout.addWidget(self.output_textbox)
        output_layout.addLayout(output_button_layout)
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)

    def create_button(self, text, callback):
        """Create a button with standard remote-friendly settings"""
        button = QPushButton(text)
        button.setMinimumHeight(30)
        button.clicked.connect(callback)
        return button

    def center_window(self):
        """Center the window on the screen"""
        try:
            frame_geometry = self.frameGeometry()
            screen_center = self.screen().availableGeometry().center()
            frame_geometry.moveCenter(screen_center)
            self.move(frame_geometry.topLeft())
        except Exception as e:
            if LOGGING_ENABLED:
                self.logger.warning(f"Could not center window: {str(e)}")

    def change_service(self, button):
        """Change the AI service"""
        new_service = "gemini" if button.text() == "Gemini" else "openai"
        if new_service != self.current_service:
            try:
                self.ai_processor = AIServiceProcessor(service=new_service)
                self.current_service = new_service
                if LOGGING_ENABLED:
                    self.logger.info(f"Switched to {new_service} service")
                QMessageBox.information(self, "Service Changed", f"Successfully switched to {new_service} service")
            except Exception as e:
                error_msg = f"Error switching to {new_service} service: {str(e)}"
                if LOGGING_ENABLED:
                    self.logger.error(error_msg)
                QMessageBox.critical(self, "Error", error_msg)
                # Revert radio button selection
                self.service_button_group.buttons()[0 if self.current_service == "gemini" else 1].setChecked(True)

    def process_code(self):
        """Process the code with selected AI service"""
        try:
            input_prompt = self.prompt_textbox.toPlainText().strip()
            input_content = self.code_textbox.toPlainText().strip()
            
            if not input_prompt or not input_content:
                QMessageBox.warning(self, "Input Required", "Please provide both code and modification prompt")
                return
            
            if LOGGING_ENABLED:
                self.logger.info("Processing code with prompt")
            
            # Show processing cursor
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            
            # Process the code
            output_text = self.ai_processor.process_text(input_prompt, input_content)
            
            # Update output textbox
            self.output_textbox.setPlainText(output_text)
            
            if LOGGING_ENABLED:
                self.logger.info("Code processing completed successfully")
            
        except Exception as e:
            error_msg = f"Error processing code: {str(e)}"
            if LOGGING_ENABLED:
                self.logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
        finally:
            # Reset cursor
            QApplication.restoreOverrideCursor()

    def load_file(self):
        """Load code from a file"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Open File",
                "",
                "Python Files (*.py);;Text Files (*.txt);;All Files (*.*)"
            )
            if file_path:
                with open(file_path, 'r') as file:
                    file_content = file.read()
                    self.code_textbox.setPlainText(file_content)
                if LOGGING_ENABLED:
                    self.logger.info(f"Loaded file: {file_path}")
        except Exception as e:
            error_msg = f"Error loading file: {str(e)}"
            if LOGGING_ENABLED:
                self.logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)

    def save_file(self):
        """Save modified code to a file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"modified_code_{timestamp}.py"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save File",
                default_filename,
                "Python Files (*.py);;Text Files (*.txt);;All Files (*.*)"
            )
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(self.output_textbox.toPlainText())
                if LOGGING_ENABLED:
                    self.logger.info(f"Saved file: {file_path}")
                QMessageBox.information(self, "Success", "File saved successfully!")
        except Exception as e:
            error_msg = f"Error saving file: {str(e)}"
            if LOGGING_ENABLED:
                self.logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)

    def copy_to_input(self):
        """Copy output code to input textbox"""
        output_text = self.output_textbox.toPlainText()
        self.code_textbox.setPlainText(output_text)
        if LOGGING_ENABLED:
            self.logger.info("Copied output to input")

def main():
    """Main entry point"""
    try:
        # Check display environment
        has_display = check_display()
        
        # Initialize QApplication
        app = QApplication(sys.argv)
        
        # Set up application-wide style for remote compatibility
        if platform.system() == "Linux":
            app.setStyle(QStyleFactory.create('Fusion'))
        
        # Create and show window
        window = AIGUI(headless=not has_display)
        window.show()
        
        sys.exit(app.exec())
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        # Use print for headless environment
        print(f"Application error: {str(e)}")
        if has_display:
            QMessageBox.critical(None, "Error", f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()