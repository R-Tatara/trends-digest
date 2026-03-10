# trends-digest

[![Scheduled Trends Digest](https://github.com/R-Tatara/trends-digest/actions/workflows/scheduled_digest.yml/badge.svg)](https://github.com/R-Tatara/trends-digest/actions/workflows/scheduled_digest.yml)
[![MIT](https://custom-icon-badges.herokuapp.com/badge/license-MIT-8BB80A.svg?logo=law&logoColor=white)](LICENSE)
[![Python](https://custom-icon-badges.herokuapp.com/badge/Python-3572A5.svg?logo=Python&logoColor=white)]()
[![Google Gemini](https://custom-icon-badges.herokuapp.com/badge/Google%20Gemini-8E75B2.svg?logo=google-gemini&logoColor=white)]()

Automated trend discovery tool that fetches popular GitHub repositories and generates AI-powered summaries using Google Gemini. Insights are delivered directly to your inbox as a detailed email digest.

## Features

- Fetches popular repositories from the past week using the GitHub API
- Generates explanations in Japanese with Google Gemini
- Sends the digest as an HTML email

## Prerequisites

- A GitHub account
- A Google Gemini API key
- A Gmail account

## Setup

### 1. Fork the Repository

Open https://github.com/R-Tatara/trends-digest on GitHub and click the **Fork** button in the upper right. The repository will be copied to your account.

### 2. Configure GitHub Secrets

In your forked repository, go to **Settings > Secrets and variables > Actions** and add the following Repository secrets.

| Secret Name | Description | How to Obtain |
|---|---|---|
| `GEMINI_API_KEY` | Google Gemini API key | Issue at [Google AI Studio](https://aistudio.google.com/) |
| `EMAIL_USER` | Sender Gmail address | Your Gmail address |
| `EMAIL_PASS` | Gmail app password | Your app password (refer to the [Google Account Help](https://support.google.com/accounts/answer/185833?hl=ja)) |
| `EMAIL_TO` | Recipient email address | The address where you want to receive the digest |


### 3. Enable GitHub Actions

By default, Actions are disabled in forked repositories. Go to the **Actions** tab and click **"I understand my workflows, go ahead and enable them"** to enable them.

### 4. Test Run (Manual Execution)

The workflow supports `workflow_dispatch`, so you can trigger it manually.

1. Go to the **Actions** tab > select **"Scheduled Trends Digest"** from the left menu
2. Click the **"Run workflow"** button
3. Select the `main` branch and click the **"Run workflow"** button

If successful, a digest email will be sent to the `EMAIL_TO` address.

### 5. Scheduled Execution

Default cron setting:

```yaml
cron: '0 22 * * 0'
```

This runs automatically every Monday 7:00 JST. To change the schedule, edit this line in `.github/workflows/scheduled_digest.yml`.

## Customization

You can customize the following by editing `config.yaml`:

- **Search criteria**: Conditions and limits for fetching repositories
- **Gemini model & prompt**: The model and prompt used for generating summaries
- **Email settings**: Subject template and introductory text

## License
MIT