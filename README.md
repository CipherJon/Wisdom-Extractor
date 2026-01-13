# Wisdom Extractor

A Streamlit application that extracts wisdom and insights from YouTube videos using AI. The application uses the YouTube Transcript API to fetch video transcripts and processes them through OpenRouter's AI models (specifically `google/gemini-2.0-flash-exp:free`) to extract key insights and lessons.

## Features

- Extract transcripts from YouTube videos
- Process transcripts using AI to extract wisdom and insights
- Clean and user-friendly interface
- Support for various YouTube URL formats
- Comprehensive error handling and logging
- Utilities for file storage and database operations
- Extensive unit tests for reliability
- Docker support for easy deployment

## Setup

### Prerequisites

- Python 3.8+
- OpenRouter API key
- Internet connection

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/wisdom-extractor.git
cd wisdom-extractor
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenRouter API key:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Open the application in your web browser (usually at http://localhost:8501)
2. Enter a YouTube URL in the input field
3. Wait for the transcript to be fetched
4. Click "Extract Wisdom" to process the transcript with AI
5. View the extracted wisdom and insights

## Running Tests

To run the unit tests, use the following command:
```bash
pytest
```

## Deployment

The project includes Docker support for easy deployment. Use the following commands to build and run the application:

1. Build the Docker image:
```bash
docker build -t wisdom-extractor -f deployment/Dockerfile .
```

2. Run the application using Docker Compose:
```bash
docker-compose -f deployment/docker-compose.yml up -d
```

## Project Structure

- `app.py`: Main Streamlit application
- `config/`: Configuration files
- `data/`: Data models and schemas
- `logging_utils/`: Logging utilities
- `persistence/`: Database and storage utilities
- `tests/`: Unit tests
- `utils/`: Utility functions and classes
- `deployment/`: Deployment scripts and configurations

## Requirements

- Python 3.8+
- OpenRouter API key
- Internet connection

## Note

Make sure the YouTube video has captions/transcripts available. The application will not work with videos that don't have captions enabled.

## AI Model

This application uses the `google/gemini-2.0-flash-exp:free` model through OpenRouter. This model is specifically chosen for its ability to extract meaningful insights and wisdom from text content.

## License

This project is licensed under the MIT License.