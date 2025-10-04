# AI Documentation Generator Action

[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-AI--Docs--Action-blue?logo=github&style=flat-square)](https://github.com/marketplace/actions/ai-documentation-generator)
[![release](https://img.shields.io/github/v/release/jadenisaac2005/ai-docs-action?style=flat-square)](https://github.com/jadenisaac2005/ai-docs-action/releases)

A GitHub Action that automatically generates a documentation website for your project. It uses an AI model to scan your source code, create a Markdown file for each code file, and then builds and deploys a complete site to GitHub Pages. This keeps your project's documentation effortlessly in sync with every commit.

![Example of a generated documentation site](https://user-images.githubusercontent.com/your-image-url-here.png)
*(Recommended: Add a screenshot of your final working site here)*

---
## How It Works

This action performs the following steps:
1.  Scans a specified source directory in your repository.
2.  For each code file, it calls a specified AI endpoint to generate documentation.
3.  Saves the generated documentation as Markdown files.
4.  Uses MkDocs with the Material theme to build a beautiful static HTML site.
5.  Deploys the final website to GitHub Pages on the `gh-pages` branch.

---
## Usage

To use this action, create a new workflow file in your repository at `.github/workflows/docs.yml`.

### Prerequisites

1.  **Get an AI API Key:** You need access to an AI model that uses a chat-completion style API. You'll need the **API Endpoint URL** and an **API Key**.
2.  **Add Repository Secrets:** In your repository, go to **Settings > Secrets and variables > Actions** and add the following secrets:
    * `AI_API_KEY`: Your secret API key for the AI model.
    * `AI_API_ENDPOINT`: The full URL to the AI model's chat completions endpoint.

### Example Workflow
```yaml
# .github/workflows/docs.yml

name: Generate AI Documentation

on:
  push:
    branches:
      - main

jobs:
  build_and_deploy_docs:
    runs-on: ubuntu-latest
    permissions:
      contents: write # Required to push to the gh-pages branch

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Generate & Deploy Docs
        uses: jadenisaac2005/ai-docs-action@v1 # This calls the action
        with:
          api_key: ${{ secrets.AI_API_KEY }}
          api_endpoint: ${{ secrets.AI_API_ENDPOINT }}
          model_name: 'Salesforce/codet5-small' # Specify the model your endpoint uses
          source_dir: './src' # Optional: specify a subdirectory to document
