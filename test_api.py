import openai
import json
from config import OPENAI_API_KEY, OPENAI_CONFIG
import logging
import time
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GPTTester:
    def __init__(self, api_key: str, config: Dict[str, Any]):
        self.client = openai.OpenAI(api_key=api_key)
        self.config = config
        self.test_prompts = [
            "Write a simple hello world program in Python.",
            "What is the capital of France?",
            "Explain quantum computing in one sentence."
        ]
    
    def test_single_prompt(self, prompt: str) -> Dict[str, Any]:
        """Test the API with a single prompt and return the response."""
        try:
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                top_p=self.config["top_p"],
                frequency_penalty=self.config["frequency_penalty"],
                presence_penalty=self.config["presence_penalty"]
            )
            
            end_time = time.time()
            
            return {
                "prompt": prompt,
                "response": response.choices[0].message.content,
                "response_time": end_time - start_time,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error processing prompt: {prompt}")
            logger.error(f"Error details: {str(e)}")
            return {
                "prompt": prompt,
                "error": str(e),
                "status": "error"
            }
    
    def run_basic_tests(self) -> List[Dict[str, Any]]:
        """Run tests with all predefined prompts."""
        results = []
        for prompt in self.test_prompts:
            logger.info(f"Testing prompt: {prompt}")
            result = self.test_single_prompt(prompt)
            results.append(result)
            
            # Add a small delay between requests to avoid rate limiting
            time.sleep(1)
        
        return results
    
    def print_results(self, results: List[Dict[str, Any]]):
        """Print test results in a formatted way."""
        print("\n=== GPT API Test Results ===")
        print(f"Model: {self.config['model']}")
        print(f"Temperature: {self.config['temperature']}")
        print("===========================")
        
        for i, result in enumerate(results, 1):
            print(f"\nTest {i}:")
            print(f"Prompt: {result['prompt']}")
            if result['status'] == 'success':
                print(f"Response: {result['response']}")
                print(f"Response Time: {result['response_time']:.2f} seconds")
            else:
                print(f"Error: {result['error']}")
            print("---------------------------")

def main():
    logger.info("Starting GPT API tests")
    
    tester = GPTTester(OPENAI_API_KEY, OPENAI_CONFIG)
    results = tester.run_basic_tests()
    tester.print_results(results)
    
    logger.info("API tests completed")

if __name__ == "__main__":
    main()