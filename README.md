# Reddit Story Generator

A Python-based application that transforms Reddit stories into engaging TikTok-ready content through a multi-stage AI processing pipeline.

## Overview

This project automates the process of:
1. Extracting stories from Reddit using the Reddit API
2. Storing them in a SQLite database
3. Enhancing the writing quality through AI
4. Restructuring stories following the Hero's Journey framework
5. Converting stories into TikTok-optimized scripts

## Features

- **Reddit Integration**: Fetches stories from specified subreddits using PRAW (Python Reddit API Wrapper)
- **Data Persistence**: Stores both raw and processed stories in SQLite database
- **AI-Powered Processing Pipeline**:
  - Story Enhancement: Improves writing clarity and flow
  - Hero's Journey Adaptation: Restructures stories following the classic 12-step hero's journey
  - TikTok Script Generation: Creates engaging scripts with hooks and timestamps

## Prerequisites

- Python 3.10+
- Reddit API credentials
- OpenAI API key

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the project root with the following variables:
```env
CLIENT_ID=your_reddit_client_id
CLIENT_SECRET=your_reddit_client_secret
USER_AGENT=your_reddit_user_agent
OPENAI_API_KEY=your_openai_api_key
```

## Usage

Run the main script:
```bash
python main.py
```

The script will:
1. Fetch recent stories from the configured subreddit
2. Store raw stories in the database
3. Process stories through the AI pipeline
4. Generate TikTok-ready scripts

## Project Structure

```
├── main.py           # Main execution script
├── utils.py          # Utility functions and AI processing
├── prompts.yaml      # AI system prompts configuration
├── managers/         # Component managers
│   ├── reddit_manager.py    # Reddit API integration
│   ├── database_manager.py  # Database operations
│   └── openai_manager.py    # OpenAI API integration
├── models/           # Database models
│   └── database.py   # SQLAlchemy models
└── requirements.txt  # Project dependencies
```

## Database Schema

- **reddit_stories**: Stores raw Reddit posts
- **processed_stories**: Stores enhanced and transformed stories
- **prompt_images_stories**: Stores image generation prompts
- **usage_tokens**: Tracks API token usage

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.