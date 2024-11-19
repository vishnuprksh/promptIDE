import google.generativeai as genai
from openai import OpenAI
import logging
from config import (
    GEMINI_API_KEY, 
    OPENAI_API_KEY,
    GEMINI_CONFIG,
    GEMINI_SAFETY_SETTINGS,
    OPENAI_CONFIG,
    LOGGING_ENABLED,
    LOG_FILE_PATH,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    OUTPUT_DIR
)

# Setup logging
if LOGGING_ENABLED:
    logging.basicConfig(
        filename=LOG_FILE_PATH,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

class AIServiceProcessor:
    def __init__(self, service="gemini"):
        self.service = service.lower()
        self.retries = 0
        self._setup_client()
        
    def _setup_client(self):
        try:
            if self.service == "gemini":
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = self._setup_gemini()
            elif self.service == "openai":
                self.client = OpenAI(
                    api_key=OPENAI_API_KEY,
                    timeout=REQUEST_TIMEOUT
                )
            else:
                raise ValueError("Unsupported AI service. Choose 'gemini' or 'openai'")
                
            if LOGGING_ENABLED:
                logger.info(f"Successfully initialized {self.service} client")
                
        except Exception as e:
            error_msg = f"Error setting up {self.service} client: {str(e)}"
            if LOGGING_ENABLED:
                logger.error(error_msg)
            raise Exception(error_msg)
    
    def _setup_gemini(self):
        return genai.GenerativeModel(
            model_name=GEMINI_CONFIG["model"],
            generation_config={
                "temperature": GEMINI_CONFIG["temperature"],
                "top_p": GEMINI_CONFIG["top_p"],
                "top_k": GEMINI_CONFIG["top_k"],
                "max_output_tokens": GEMINI_CONFIG["max_output_tokens"],
            },
            safety_settings=GEMINI_SAFETY_SETTINGS
        )

    def _process_with_gemini(self, prompt_input, file_content):
        try:
            prompt = f"""
            Update the following code: {file_content} 
            according to the following suggestions: {prompt_input} 
            and return the code (as text, not as markdown block)
            """
            prompt_parts = [prompt]
            response = self.model.generate_content(prompt_parts)
            
            if LOGGING_ENABLED:
                logger.info("Successfully processed request with Gemini")
                
            return response.text
            
        except Exception as e:
            error_msg = f"Error processing with Gemini: {str(e)}"
            if LOGGING_ENABLED:
                logger.error(error_msg)
            
            if self.retries < MAX_RETRIES:
                self.retries += 1
                if LOGGING_ENABLED:
                    logger.info(f"Retrying request ({self.retries}/{MAX_RETRIES})")
                return self._process_with_gemini(prompt_input, file_content)
            else:
                raise Exception(error_msg)

    def _process_with_openai(self, prompt_input, file_content):
        try:
            prompt = f"""
            Update the following code: {file_content} 
            according to the following suggestions: {prompt_input} 
            and return the code (as text, not as markdown block)
            """
            
            response = self.client.chat.completions.create(
                model=OPENAI_CONFIG["model"],
                messages=[
                    {"role": "system", "content": "You are a helpful code assistant. Provide code updates as plain text without markdown formatting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=OPENAI_CONFIG["temperature"],
                max_tokens=OPENAI_CONFIG["max_tokens"],
                top_p=OPENAI_CONFIG["top_p"],
                frequency_penalty=OPENAI_CONFIG["frequency_penalty"],
                presence_penalty=OPENAI_CONFIG["presence_penalty"]
            )
            
            if LOGGING_ENABLED:
                logger.info("Successfully processed request with OpenAI")
                
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = f"Error processing with OpenAI: {str(e)}"
            if LOGGING_ENABLED:
                logger.error(error_msg)
            
            if self.retries < MAX_RETRIES:
                self.retries += 1
                if LOGGING_ENABLED:
                    logger.info(f"Retrying request ({self.retries}/{MAX_RETRIES})")
                return self._process_with_openai(prompt_input, file_content)
            else:
                raise Exception(error_msg)

    def process_text(self, prompt_input, file_content):
        self.retries = 0  # Reset retry counter
        if self.service == "gemini":
            return self._process_with_gemini(prompt_input, file_content)
        else:
            return self._process_with_openai(prompt_input, file_content)

def create_output_directories():
    """Create necessary directories for logs and output"""
    import os
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

if __name__ == "__main__":
    # Create necessary directories
    create_output_directories()
    
    # Example usage with error handling
    try:
        # Use with Gemini
        gemini_processor = AIServiceProcessor(service="gemini")
        result_gemini = gemini_processor.process_text(
            "Add error handling", 
            "def example():\n    return True"
        )
        print("Gemini result:", result_gemini)
        
        # Use with OpenAI
        openai_processor = AIServiceProcessor(service="openai")
        result_openai = openai_processor.process_text(
            "Add error handling", 
            "def example():\n    return True"
        )
        print("OpenAI result:", result_openai)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        if LOGGING_ENABLED:
            logger.error(f"Error in main execution: {str(e)}")