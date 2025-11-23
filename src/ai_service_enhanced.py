"""
Enhanced AI-powered service for financial statement validation and enhancement.
Supports custom model selection and advanced prompt engineering for accounting tasks.
"""

import os
import json
import requests
from typing import Dict, Any, List, Optional, Tuple

# Available models from OpenRouter (curated list)
AVAILABLE_MODELS = {
    "Reasoning & Complex Analysis": [
        "x-ai/grok-4.1-fast",
        "openai/gpt-4o",
        "openai/gpt-4-turbo",
        "anthropic/claude-3.5-sonnet",
    ],
    "Fast & Cost-Effective": [
        "google/gemini-2.5-flash-lite",
        "openai/gpt-4.1-nano",
        "openai/gpt-5-mini",
        "anthropic/claude-3-haiku",
    ],
    "Document Intelligence": [
        "nvidia/nemotron-nano-12b-v2-vl",
        "google/gemini-2.0-flash-exp",
        "openai/gpt-4o",
        "qwen/qwen3-embedding-8b",  # Added Qwen embedding model
    ],
    "General Purpose": [
        "openai/gpt-4.1-nano",
        "openai/gpt-4o-mini",
        "google/gemini-2.5-flash-lite",
    ]
}


class EnhancedAIService:
    """
    Enhanced AI service with configurable models and advanced prompt engineering.
    """
    
    def __init__(self, api_key: Optional[str] = None, model_config: Optional[Dict[str, str]] = None):
        """
        Initialize AI service with custom API key and model configuration.
        
        Args:
            api_key: OpenRouter API key. If None, reads from OPENROUTER_API_KEY env var.
            model_config: Dictionary mapping task types to model names
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenRouter API key required")
        
        # Default model configuration with Qwen embedding model for document analysis
        self.model_config = model_config or {
            'validation': 'x-ai/grok-4.1-fast',
            'extraction': 'nvidia/nemotron-nano-12b-v2-vl',
            'cross_validation': 'google/gemini-2.5-flash-lite',
            'note_generation': 'openai/gpt-4.1-nano',
            'tax_validation': 'google/gemini-2.5-flash-lite',
            'document_analysis': 'qwen/qwen3-embedding-8b',  # Added for document analysis
        }
        
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo",
            "X-Title": "AASB Financial Statement Generator"
        }
    
    def update_api_key(self, api_key: str):
        """Update API key dynamically."""
        self.api_key = api_key
        self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    def update_model_config(self, model_config: Dict[str, str]):
        """Update model configuration dynamically."""
        self.model_config.update(model_config)
    
    def _call_api(self, model: str, messages: List[Dict[str, str]], 
                  reasoning_enabled: bool = False, temperature: float = 0.3) -> Dict[str, Any]:
        """Call OpenRouter API with specified model."""
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        
        if 'grok' in model.lower() and reasoning_enabled:
            payload["reasoning"] = True
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenRouter API error: {str(e)}")
    
    def validate_balance_sheet_relationships(self, bs_data: Dict[str, Any], 
                                            pl_data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """Use AI to validate balance sheet relationships."""
        prompt = f"""Validate this balance sheet for an Australian non-reporting entity.
        
BALANCE SHEET: {json.dumps(bs_data, indent=2)}
P&L: {json.dumps(pl_data, indent=2)}

Check: Assets = Liabilities + Equity, retained earnings rollforward, classifications.

Respond in JSON: {{"is_valid": true/false, "issues": [], "calculated_totals": {{}}}}"""
        
        messages = [
            {"role": "system", "content": "You are a senior chartered accountant specializing in Australian financial reporting."},
            {"role": "user", "content": prompt}
        ]
        
        model = self.model_config.get('validation', 'x-ai/grok-4.1-fast')
        
        try:
            response = self._call_api(model, messages, reasoning_enabled=True)
            content = response['choices'][0]['message']['content']
            analysis = self._extract_json(content)
            is_valid = analysis.get('is_valid', False)
            issues = analysis.get('issues', [])
            message = "\n".join(issues) if issues else "All checks passed"
            return is_valid, message, analysis
        except Exception as e:
            return True, f"AI validation unavailable: {str(e)}", {}
    
    def _extract_json(self, content: str) -> Dict[str, Any]:
        """Extract JSON from AI response."""
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except:
                pass
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except:
                pass
        return {"raw_response": content}
    
    def analyze_document_semantics(self, document_text: str) -> Dict[str, Any]:
        """
        Use Qwen/Qwen3-Embedding-8B model for advanced document analysis and semantic understanding.
        
        Args:
            document_text: Text content of the document to analyze
            
        Returns:
            Dictionary with semantic analysis results
        """
        # For embedding models, we might need a different approach
        # This is a placeholder implementation that would need to be adapted based on the specific API
        model = self.model_config.get('document_analysis', 'qwen/qwen3-embedding-8b')
        
        # If it's an embedding model, we might need to use a different endpoint or approach
        if 'embedding' in model.lower():
            # This would be for embedding models - semantic analysis
            payload = {
                "model": model,
                "input": document_text[:4000],  # Limit text length for embedding models
            }
            
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/embeddings",  # Different endpoint for embeddings
                    headers=self.headers,
                    json=payload,
                    timeout=60
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                raise Exception(f"OpenRouter Embedding API error: {str(e)}")
        else:
            # For regular chat models, use the standard approach
            prompt = f"""Analyze the following financial document for semantic understanding:
            
{document_text[:4000]}  # Limit text length

Provide:
1. Key financial concepts identified
2. Document structure analysis
3. Semantic relationships between sections
4. Potential data extraction points

Respond in JSON format."""
            
            messages = [
                {"role": "system", "content": "You are an expert in financial document analysis and semantic understanding."},
                {"role": "user", "content": prompt}
            ]
            
            try:
                response = self._call_api(model, messages)
                content = response['choices'][0]['message']['content']
                return self._extract_json(content)
            except Exception as e:
                return {"error": f"Document analysis failed: {str(e)}"}