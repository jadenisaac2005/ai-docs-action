import os
import requests
import sys

def get_ai_documentation(code_content: str, api_key: str, api_url: str, model_name: str) -> str:
    """
    Calls the specified AI model endpoint to generate documentation for a code snippet.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # This payload is structured for chat-completion style APIs (like OpenAI's or Gradient's)
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": f"Generate professional markdown documentation for this Python code snippet:\n\n{code_content}"
            }
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        response_data = response.json()
        # Navigate the JSON response to find the generated content
        return response_data['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        sys.exit(f"Error: API request failed. {e}")
    except (KeyError, IndexError):
        sys.exit(f"Error: Could not parse the AI response. Raw response: {response.text}")

def main():
    """
    Main function to orchestrate the documentation generation process for a repository.
    """
    # Read configuration from environment variables provided by the GitHub Action runner
    api_key = os.environ.get("INPUT_API_KEY")
    api_endpoint = os.environ.get("INPUT_API_ENDPOINT")
    model_name = os.environ.get("INPUT_MODEL_NAME")
    source_dir = os.environ.get("INPUT_SOURCE_DIR", ".") # Default to the root directory
    docs_dir = "./docs" # The action will always generate files into a local 'docs' folder

    # --- Input Validation ---
    if not api_key:
        sys.exit("Error: 'api_key' input is required.")
    if not api_endpoint:
        sys.exit("Error: 'api_endpoint' input is required.")
    if not model_name:
        sys.exit("Error: 'model_name' input is required.")

    print(f"Starting documentation generation for source directory: '{source_dir}'")

    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)

    # Walk through the source directory and process each Python file
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                print(f"Processing: {filepath}")

                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Get documentation from the AI model
                documentation = get_ai_documentation(content, api_key, api_endpoint, model_name)

                # Create a corresponding .md file in the docs folder
                relative_path = os.path.relpath(filepath, source_dir)
                md_filename = os.path.splitext(relative_path)[0] + ".md"
                md_filepath = os.path.join(docs_dir, md_filename)

                # Ensure the subdirectory structure is mirrored in the docs folder
                os.makedirs(os.path.dirname(md_filepath), exist_ok=True)

                with open(md_filepath, "w", encoding="utf-8") as f:
                    f.write(f"# {file}\n\n{documentation}")

    print("Documentation generation complete!")

if __name__ == "__main__":
    main()
