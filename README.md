# trends-digest

Automated trend discovery tool that fetches popular GitHub repositories and generates AI-powered summaries using Google Gemini. Insights are delivered directly to your inbox as a detailed email digest.

## Prerequisites

- Python 3.10+
- uv

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/R-Tatara/trends-digest.git
   cd trends-digest
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure environment**
   ```bash
   GITHUB_TOKEN=your_github_token
   GEMINI_API_KEY=your_gemini_api_key
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_app_password
   EMAIL_TO=recipient@example.com
   ```

## Usage

Generate and send the digest:

```bash
uv run python main.py
```

## License
MIT