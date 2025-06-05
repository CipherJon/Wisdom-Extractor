# Wisdom Extractor

A Streamlit application that extracts wisdom and insights from YouTube videos using AI. The application uses the YouTube Transcript API to fetch video transcripts and processes them through OpenRouter's AI models (specifically deepseek-r1-0528-qwen3-8b) to extract key insights and lessons.

## Features

- Extract transcripts from YouTube videos
- Process transcripts using AI to extract wisdom and insights
- Clean and user-friendly interface
- Support for various YouTube URL formats
- Uses deepseek-r1-0528-qwen3-8b model for consistent, high-quality insights

## Setup

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

## Requirements

- Python 3.7+
- OpenRouter API key
- Internet connection

## Note

Make sure the YouTube video has captions/transcripts available. The application will not work with videos that don't have captions enabled.

## AI Model

This application uses the `deepseek/deepseek-r1-0528-qwen3-8b:free` model through OpenRouter. This model is specifically chosen for its ability to extract meaningful insights and wisdom from text content.