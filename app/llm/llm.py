try:
    import google.genai as genai
    GENAI_AVAILABLE = True
except ImportError:
    try:
        import google.generativeai as genai
        GENAI_AVAILABLE = True
        print("Warning: google.generativeai is deprecated. Please install google-genai package")
    except ImportError:
        GENAI_AVAILABLE = False

import os
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_fixed
from app.config import settings

class LLMRouter:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE
        )
        
        # Initialize Gemini if available
        self.gemini_available = False
        if GENAI_AVAILABLE and hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.gemini_available = True
            except Exception as e:
                print(f"Failed to initialize Gemini: {e}")

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
    def call_gemini(self, prompt: str):
        if not self.gemini_available:
            raise Exception("Gemini not available")
        
        try:
            if 'google.genai' in str(type(genai)):
                # New google-genai package
                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                response = client.models.generate_content(
                    model=settings.PRIMARY_MODEL,
                    contents=prompt
                )
                return response.text
            else:
                # Old deprecated package
                model = genai.GenerativeModel(settings.PRIMARY_MODEL)
                response = model.generate_content(prompt)
                return response.text
        except Exception as e:
            print(f"Gemini API error: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def call_openai(self, prompt: str):
        response = self.client.chat.completions.create(
            model=settings.PRIMARY_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content

    def call_vllm(self, prompt: str):
        try:
            response = self.client.chat.completions.create(
                model=settings.FALLBACK_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                timeout=10.0,  # 10 second timeout
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"vLLM connection error: {e}")
            raise

    def call_fallback(self, prompt: str):
        """Fallback method for when all APIs fail"""
        return f"[OFFLINE MODE] Unable to process request due to API limitations. Original prompt: {prompt[:100]}..."

    def generate(self, prompt: str):
        errors = []
        
        try:
            return self.call_openai(prompt)
        except Exception as e:
            print(f"OpenAI API failed: {e}")
            errors.append(f"OpenAI failed: {e}")
        
        # Try Gemini
        try:
            return self.call_gemini(prompt)
        except Exception as e:
            errors.append(f"Gemini failed: {e}")
        
        # Try vLLM
        try:
            return self.call_vllm(prompt)
        except Exception as e:
            errors.append(f"vLLM failed: {e}")
        
        # Fallback
        print(f"All LLM providers failed: {'; '.join(errors)}")
        return self.call_fallback(prompt)