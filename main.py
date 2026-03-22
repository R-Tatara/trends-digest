import os
import yaml
import datetime
from dotenv import load_dotenv
from src.github_client import GithubClient
from src.gemini_client import GeminiClient
from src.email_client import EmailClient

# Load environment variables
load_dotenv()

def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    # Load Configurations
    config = load_config()

    # 認証情報の取得（環境変数）
    github_token = os.getenv("GITHUB_TOKEN")
    gemini_key = os.getenv("GEMINI_API_KEY")
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    email_to = os.getenv("EMAIL_TO")

    if not all([github_token, gemini_key, email_user, email_pass, email_to]):
        print("Error: Missing environment variables. Please check .env file.")
        return

    # Initialize Clients
    gh_client = GithubClient(github_token)
    gemini_client = GeminiClient(gemini_key, model_name=config["gemini_settings"]["model"])
    email_client = EmailClient(email_user, email_pass)

    # Search GitHub Repositories
    print("--- Step 1: Searching GitHub ---")

    # 日付計算 (直近7日間)
    one_week_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    query = config["search_settings"]["query_template"].format(date=one_week_ago)
    limit = config["search_settings"]["limit"]

    repos = gh_client.search_repositories(query, limit)

    if not repos:
        print("No repositories found.")
        return

    # Analyze with Gemini
    print("--- Step 2: Analyzing with Gemini ---")
    reports = []
    prompt_template = config["gemini_settings"]["prompt_template"]

    for repo in repos:
        print(f"Processing: {repo['name']}")
        analysis = gemini_client.analyze_repository(repo, prompt_template)

        # レポート用データ作成
        reports.append({
            "name": repo["name"],
            "url": repo["url"],
            "stars": repo["stars"],
            "language": repo["language"],
            "digest": analysis
        })

    # Create and Send Email
    print("--- Step 3: Sending Email ---")
    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    subject = config["email_settings"]["subject_template"].format(date=today_str)

    html_body = email_client.create_html_body(
        intro_text=config["email_settings"]["intro_text"],
        reports=reports
    )

    success = email_client.send_email(email_to, subject, html_body)

    if success:
        print("Weekly digest sent successfully.")
    else:
        print("Failed to send email.")


if __name__ == "__main__":
    main()
