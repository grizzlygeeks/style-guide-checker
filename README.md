# Style Guide Checker GitHub Action

## Introduction
The Style Guide Checker GitHub Action is designed to automatically review your docs to ensure it adheres to specified style guidelines. It currently uses OpenAI's GPT-4 Preview model, and therefore requires a valid OpenAI API Key.

## Getting Started

### Prerequisites
- Requires setting a secret named `OPENAI_API_KEY` in the Org or Repo it will be run in.

### Example
```yaml
on:
  workflow_dispatch:
  push:
    branches:
      - main
  pull_request:

jobs:
  style-guide-checker-test:
    runs-on: ubuntu-latest
    name: A test job to run Style Guide Checker
    steps:
      - name: Run Style Guide Checker on changed files
        uses: grizzlygeeks/style-guide-checker
        id: style-guide-checker
        with:
          openai-token: ${{ secrets.OPENAI_API_KEY }}
          all_files: true
          ignore_path: '**/node_modules/**'
          file_extensions: |
            **/*.{md,MD,html,HTML}
```

## License
This project is distributed under the [MIT License](LICENSE).

## Support
For support, questions, or feedback, please [open an issue]()!
