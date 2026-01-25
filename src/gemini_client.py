from google import genai
from google.genai import types
from typing import Dict, Any


class GeminiClient:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        """
        Initialize Gemini client.

        Args:
            api_key: Gemini API Key
            model_name: Model version to use
        """
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def analyze_repository(self, repo_data: Dict[str, Any], prompt_template: str) -> str:
        """
        Analyze repository based on collected data.

        Args:
            repo_data: Dictionary containing repository info (name, readme, etc.)
            prompt_template: Format string for the prompt

        Returns:
            Generated text analysis
        """
        # コンテキストを作成
        prompt = prompt_template.format(
            name=repo_data.get("name"),
            url=repo_data.get("url"),
            description=repo_data.get("description"),
            topics=", ".join(repo_data.get("topics", [])),
            readme_content=repo_data.get("readme", "")
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2, # 解説なので低めに設定して安定させる
                    max_output_tokens=1000
                )
            )
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API for {repo_data.get('name')}: {e}")
            return "解説の生成に失敗しました。"
