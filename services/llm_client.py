import openai
import time
import logging
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS

logger = logging.getLogger(__name__)

openai.api_key = OPENAI_API_KEY

class LLMClient:
    """Wrapper para OpenAI GPT con retries y timeout"""
    
    def __init__(self, model=OPENAI_MODEL, temperature=OPENAI_TEMPERATURE, 
                 max_tokens=OPENAI_MAX_TOKENS, retries=3, timeout=30):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.retries = retries
        self.timeout = timeout
    
    def generate(self, prompt, system_prompt=None, json_mode=False):
        """
        Generate text from LLM
        
        Args:
            prompt: User message
            system_prompt: System context
            json_mode: Request JSON output
        
        Returns:
            Generated text or dict if json_mode
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        for attempt in range(self.retries):
            try:
                kwargs = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                }
                
                if json_mode:
                    kwargs["response_format"] = {"type": "json_object"}
                
                response = openai.ChatCompletion.create(**kwargs)
                
                content = response.choices[0].message.content.strip()
                
                if json_mode:
                    import json
                    try:
                        return json.loads(content)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse JSON response: {content}")
                        return {"error": "Invalid JSON response", "raw": content}
                
                return content
                
            except openai.error.RateLimitError:
                if attempt < self.retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Rate limited. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error("Max retries exceeded for rate limit")
                    raise
            except openai.error.APIError as e:
                if attempt < self.retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"API error: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Max retries exceeded: {e}")
                    raise
            except Exception as e:
                logger.error(f"Unexpected error in LLM client: {e}")
                raise
    
    def generate_json(self, prompt, system_prompt=None):
        """Generate JSON from LLM"""
        return self.generate(prompt, system_prompt, json_mode=True)
