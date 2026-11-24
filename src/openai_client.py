from openai import OpenAI
from typing import Dict, Any


class OpenAIClient:
    def __init__(self, api_key: str, model_name: str = "gpt-4o-mini"):
        """
        Initialize OpenAI client.

        Args:
            api_key: OpenAI API key
            model_name: Model version to use
        """
        self.client = OpenAI(api_key=api_key)
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
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2, # 解説なので低めに設定して安定させる
                max_completion_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API for {repo_data.get('name')}: {e}")
            return "解説の生成に失敗しました。"
