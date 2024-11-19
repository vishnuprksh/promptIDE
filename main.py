import tkinter as tk
from tkinter import scrolledtext, filedialog, ttk, messagebox
from ai_service import AIServiceProcessor
import logging
from config import (
    LOGGING_ENABLED,
    LOG_FILE_PATH,
    OUTPUT_DIR,
    DEBUG_MODE
)
import os
from datetime import datetime

class AIGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Code Assistant")
        
        # Initialize AI Service
        self.current_service = "gemini"  # default service
        self.ai_processor = AIServiceProcessor(service=self.current_service)
        
        self.setup_logging()
        self.create_gui()
        
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
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Service selection
        service_frame = ttk.LabelFrame(main_frame, text="AI Service", padding="5")
        service_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.service_var = tk.StringVar(value=self.current_service)
        ttk.Radiobutton(service_frame, text="Gemini", variable=self.service_var, 
                       value="gemini", command=self.change_service).grid(row=0, column=0, padx=5)
        ttk.Radiobutton(service_frame, text="OpenAI", variable=self.service_var, 
                       value="openai", command=self.change_service).grid(row=0, column=1, padx=5)

        # Code input section
        code_frame = ttk.LabelFrame(main_frame, text="Original Code", padding="5")
        code_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.code_textbox = scrolledtext.ScrolledText(code_frame, height=10, width=60, wrap=tk.WORD)
        self.code_textbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button frame for code actions
        code_button_frame = ttk.Frame(code_frame)
        code_button_frame.grid(row=1, column=0, pady=5)
        
        ttk.Button(code_button_frame, text="Load Code", command=self.load_file).grid(row=0, column=0, padx=5)
        ttk.Button(code_button_frame, text="Clear", command=lambda: self.code_textbox.delete(1.0, tk.END)).grid(row=0, column=1, padx=5)

        # Prompt input section
        prompt_frame = ttk.LabelFrame(main_frame, text="Modification Prompt", padding="5")
        prompt_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.prompt_textbox = scrolledtext.ScrolledText(prompt_frame, height=4, width=60, wrap=tk.WORD)
        self.prompt_textbox.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Process button
        ttk.Button(main_frame, text="Process", command=self.process_code).grid(row=3, column=0, columnspan=2, pady=10)

        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Modified Code", padding="5")
        output_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.output_textbox = scrolledtext.ScrolledText(output_frame, height=10, width=60, wrap=tk.WORD)
        self.output_textbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button frame for output actions
        output_button_frame = ttk.Frame(output_frame)
        output_button_frame.grid(row=1, column=0, pady=5)
        
        ttk.Button(output_button_frame, text="Save Code", command=self.save_file).grid(row=0, column=0, padx=5)
        ttk.Button(output_button_frame, text="Clear", command=lambda: self.output_textbox.delete(1.0, tk.END)).grid(row=0, column=1, padx=5)
        ttk.Button(output_button_frame, text="Copy to Input", command=self.copy_to_input).grid(row=0, column=2, padx=5)

        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def change_service(self):
        """Change the AI service"""
        new_service = self.service_var.get()
        if new_service != self.current_service:
            try:
                self.ai_processor = AIServiceProcessor(service=new_service)
                self.current_service = new_service
                if LOGGING_ENABLED:
                    self.logger.info(f"Switched to {new_service} service")
                messagebox.showinfo("Service Changed", f"Successfully switched to {new_service} service")
            except Exception as e:
                error_msg = f"Error switching to {new_service} service: {str(e)}"
                if LOGGING_ENABLED:
                    self.logger.error(error_msg)
                messagebox.showerror("Error", error_msg)
                self.service_var.set(self.current_service)

    def process_code(self):
        """Process the code with selected AI service"""
        try:
            input_prompt = self.prompt_textbox.get("1.0", tk.END).strip()
            input_content = self.code_textbox.get("1.0", tk.END).strip()
            
            if not input_prompt or not input_content:
                messagebox.showwarning("Input Required", "Please provide both code and modification prompt")
                return
            
            if LOGGING_ENABLED:
                self.logger.info("Processing code with prompt")
            
            # Show processing indicator
            self.root.config(cursor="wait")
            self.root.update()
            
            # Process the code
            output_text = self.ai_processor.process_text(input_prompt, input_content)
            
            # Update output textbox
            self.output_textbox.delete("1.0", tk.END)
            self.output_textbox.insert(tk.END, output_text)
            
            if LOGGING_ENABLED:
                self.logger.info("Code processing completed successfully")
            
        except Exception as e:
            error_msg = f"Error processing code: {str(e)}"
            if LOGGING_ENABLED:
                self.logger.error(error_msg)
            messagebox.showerror("Error", error_msg)
        finally:
            # Reset cursor
            self.root.config(cursor="")

    def load_file(self):
        """Load code from a file"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[
                    ("Python files", "*.py"),
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )
            if file_path:
                with open(file_path, 'r') as file:
                    file_content = file.read()
                    self.code_textbox.delete("1.0", tk.END)
                    self.code_textbox.insert(tk.END, file_content)
                if LOGGING_ENABLED:
                    self.logger.info(f"Loaded file: {file_path}")
        except Exception as e:
            error_msg = f"Error loading file: {str(e)}"
            if LOGGING_ENABLED:
                self.logger.error(error_msg)
            messagebox.showerror("Error", error_msg)

    def save_file(self):
        """Save modified code to a file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"modified_code_{timestamp}.py"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".py",
                initialfile=default_filename,
                filetypes=[
                    ("Python files", "*.py"),
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(self.output_textbox.get("1.0", tk.END))
                if LOGGING_ENABLED:
                    self.logger.info(f"Saved file: {file_path}")
                messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            error_msg = f"Error saving file: {str(e)}"
            if LOGGING_ENABLED:
                self.logger.error(error_msg)
            messagebox.showerror("Error", error_msg)

    def copy_to_input(self):
        """Copy output code to input textbox"""
        output_text = self.output_textbox.get("1.0", tk.END)
        self.code_textbox.delete("1.0", tk.END)
        self.code_textbox.insert(tk.END, output_text)
        if LOGGING_ENABLED:
            self.logger.info("Copied output to input")

def main():
    """Main entry point"""
    try:
        root = tk.Tk()
        app = AIGUI(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        messagebox.showerror("Error", f"Application error: {str(e)}")

if __name__ == "__main__":
    main()