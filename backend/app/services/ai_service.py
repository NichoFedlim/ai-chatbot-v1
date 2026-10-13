"""
AI service for interacting with OpenAI API or fallback to free alternatives.
"""
import httpx
import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
import time

from ..config import settings

# Configure logging
logger = logging.getLogger(__name__)

class AIService:
    """Service class for AI interactions."""
    
    def __init__(self):
        self.api_key = settings.openai_api_key
        self.model = settings.openai_model
        self.max_tokens = settings.openai_max_tokens
        self.temperature = settings.openai_temperature
        self.system_prompt = settings.system_prompt
        
        # Free AI API fallbacks
        self.free_apis = [
            {
                "name": "HuggingFace Inference API",
                "url": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
                "headers": {"Authorization": f"Bearer {settings.openai_api_key}"}
            },
            {
                "name": "Together AI",
                "url": "https://api.together.xyz/v1/chat/completions",
                "headers": {"Authorization": f"Bearer {settings.openai_api_key}"}
            }
        ]
    
    async def get_response(self, message: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Get AI response for user message.
        Tries OpenAI first, falls back to free alternatives.
        """
        start_time = time.time()
        
        # Prepare messages with history
        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            messages.extend(history[-10:])  # Include last 10 messages for context
        messages.append({"role": "user", "content": message})
        
        # Try OpenAI API first
        if self.api_key and not self.api_key.startswith("your_"):
            try:
                response = await self._call_openai(messages)
                if response:
                    response["latency_ms"] = int((time.time() - start_time) * 1000)
                    return response
            except Exception as e:
                logger.error(f"OpenAI API error: {str(e)}")
        
        # Fallback to free APIs
        try:
            response = await self._call_free_api(messages)
            if response:
                response["latency_ms"] = int((time.time() - start_time) * 1000)
                return response
        except Exception as e:
            logger.error(f"Free API error: {str(e)}")
        
        # Ultimate fallback with local response
        return {
            "message": self._generate_local_response(message),
            "model": "local-fallback",
            "tokens_used": 0,
            "latency_ms": int((time.time() - start_time) * 1000)
        }
    
    async def _call_openai(self, messages: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
        """Call OpenAI API."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "message": data["choices"][0]["message"]["content"],
                    "model": data.get("model", self.model),
                    "tokens_used": data.get("usage", {}).get("total_tokens", None)
                }
            else:
                logger.error(f"OpenAI API returned status {response.status_code}: {response.text}")
                return None
    
    async def _call_free_api(self, messages: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
        """Call free alternative AI APIs."""
        for api in self.free_apis:
            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    if "huggingface" in api["url"]:
                        # HuggingFace Inference API format
                        prompt = self._format_messages_for_hf(messages)
                        response = await client.post(
                            api["url"],
                            headers=api["headers"],
                            json={"inputs": prompt, "parameters": {"max_new_tokens": self.max_tokens}}
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            if isinstance(data, list) and len(data) > 0:
                                return {
                                    "message": data[0].get("generated_text", ""),
                                    "model": api["name"],
                                    "tokens_used": None
                                }
                    else:
                        # Together AI format (OpenAI-compatible)
                        response = await client.post(
                            api["url"],
                            headers=api["headers"],
                            json={
                                "model": "mistralai/Mistral-7B-Instruct-v0.2",
                                "messages": messages,
                                "max_tokens": self.max_tokens,
                                "temperature": self.temperature
                            }
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            return {
                                "message": data["choices"][0]["message"]["content"],
                                "model": api["name"],
                                "tokens_used": data.get("usage", {}).get("total_tokens", None)
                            }
            except Exception as e:
                logger.error(f"Error calling {api['name']}: {str(e)}")
                continue
        
        return None
    
    def _format_messages_for_hf(self, messages: List[Dict[str, str]]) -> str:
        """Format messages for HuggingFace API."""
        formatted = []
        for msg in messages:
            if msg["role"] == "system":
                formatted.append(f"System: {msg['content']}")
            elif msg["role"] == "user":
                formatted.append(f"Human: {msg['content']}")
            elif msg["role"] == "assistant":
                formatted.append(f"Assistant: {msg['content']}")
        
        formatted.append("Assistant: ")
        return "\n".join(formatted)
    
    def _generate_local_response(self, message: str) -> str:
        """Generate a simple local response when no API is available."""
        # Simple rule-based responses
        greetings = ["hello", "hi", "hey", "greetings"]
        questions = ["how are you", "what's up", "how do you do"]
        
        message_lower = message.lower()
        
        if any(greeting in message_lower for greeting in greetings):
            return "Hello! I'm here to help you. While I'm currently operating without an external AI service, I can still assist with basic queries. Please configure an API key for full functionality."
        
        if any(question in message_lower for question in questions):
            return "I'm functioning properly, though I'm currently in fallback mode without full AI capabilities. To unlock my full potential, please configure an OpenAI API key."
        
        return ("I understand your message: '{}'. To provide more intelligent responses, "
                "please configure an AI API key (OpenAI or HuggingFace) in the backend .env file. "
                "I'm currently operating in local fallback mode.").format(message)

# Create singleton instance
ai_service = AIService()
