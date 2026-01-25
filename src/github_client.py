import base64
from typing import List, Dict, Any, Optional
from github import Github, Auth
from github.Repository import Repository
from github.ContentFile import ContentFile


class GithubClient:
    def __init__(self, token: str):
        """
        Initialize Github client with access token.

        Args:
            token: GitHub Personal Access Token
        """
        self.client = Github(auth=Auth.Token(token))

    def search_repositories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for repositories based on query.

        Args:
            query: Search query string
            limit: Maximum number of repositories to return

        Returns:
            List of repository data dictionaries
        """
        print(f"Searching repositories using query: {query}")
        repositories = self.client.search_repositories(query=query, sort="stars", order="desc")

        results = []
        count = 0

        # search_repositories returns a paginated list, iterate carefully
        for repo in repositories:
            if count >= limit:
                break

            repo_data = self._extract_repo_info(repo)
            results.append(repo_data)
            count += 1

        return results

    def _extract_repo_info(self, repo: Repository) -> Dict[str, Any]:
        """
        Extract relevant information from Repository object.
        """
        readme_content = self.get_readme_content(repo)

        return {
            "name": repo.full_name,
            "url": repo.html_url,
            "description": repo.description or "No description",
            "stars": repo.stargazers_count,
            "language": repo.language,
            "topics": repo.get_topics(),
            "created_at": repo.created_at.strftime("%Y-%m-%d"),
            "readme": readme_content
        }

    def get_readme_content(self, repo: Repository, max_length: int = 5000) -> str:
        """
        Fetch and decode README content, truncated to max_length.
        """
        try:
            # 通常は 'README.md' や 'README.rst' などを自動で取得してくれる
            content_file: ContentFile = repo.get_readme()
            # Content is usually base64 encoded
            content = base64.b64decode(content_file.content).decode("utf-8", errors="ignore")

            if len(content) > max_length:
                return content[:max_length] + "...\n(truncated)"
            return content

        except Exception as e:
            print(f"Warning: Could not fetch README for {repo.full_name}: {e}")
            return "README not available"
