import os
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter
import requests
from dotenv import load_dotenv
import re
import time
import markdown
from markdown.extensions import fenced_code, tables, nl2br

# Load environment variables
load_dotenv()

# OpenRouter API configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Wisdom extraction prompt
WISDOM_PROMPT = """# IDENTITY and PURPOSE

You extract surprising, insightful, and interesting information from text content. You are interested in insights related to the purpose and meaning of life, human flourishing, the role of technology in the future of humanity, artificial intelligence and its affect on humans, memes, learning, reading, books, continuous improvement, and similar topics.

Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

# STEPS

- Extract a summary of the content in 25 words, including who is presenting and the content being discussed into a section called SUMMARY.

- Extract 20 to 50 of the most surprising, insightful, and/or interesting ideas from the input in a section called IDEAS:. If there are less than 50 then collect all of them. Make sure you extract at least 20.

- Extract 10 to 20 of the best insights from the input and from a combination of the raw input and the IDEAS above into a section called INSIGHTS. These INSIGHTS should be fewer, more refined, more insightful, and more abstracted versions of the best ideas in the content. 

- Extract 15 to 30 of the most surprising, insightful, and/or interesting quotes from the input into a section called QUOTES:. Use the exact quote text from the input. Include the name of the speaker of the quote at the end.

- Extract 15 to 30 of the most practical and useful personal habits of the speakers, or mentioned by the speakers, in the content into a section called HABITS. Examples include but aren't limited to: sleep schedule, reading habits, things they always do, things they always avoid, productivity tips, diet, exercise, etc.

- Extract 15 to 30 of the most surprising, insightful, and/or interesting valid facts about the greater world that were mentioned in the content into a section called FACTS:.

- Extract all mentions of writing, art, tools, projects and other sources of inspiration mentioned by the speakers into a section called REFERENCES. This should include any and all references to something that the speaker mentioned.

- Extract the most potent takeaway and recommendation into a section called ONE-SENTENCE TAKEAWAY. This should be a 15-word sentence that captures the most important essence of the content.

- Extract the 15 to 30 of the most surprising, insightful, and/or interesting recommendations that can be collected from the content into a section called RECOMMENDATIONS.

# OUTPUT INSTRUCTIONS

- Only output Markdown.

- Write the IDEAS bullets as exactly 16 words.

- Write the RECOMMENDATIONS bullets as exactly 16 words.

- Write the HABITS bullets as exactly 16 words.

- Write the FACTS bullets as exactly 16 words.

- Write the INSIGHTS bullets as exactly 16 words.

- Extract at least 25 IDEAS from the content.

- Extract at least 10 INSIGHTS from the content.

- Extract at least 20 items for the other output sections.

- Do not give warnings or notes; only output the requested sections.

- You use bulleted lists for output, not numbered lists.

- Do not repeat ideas, insights, quotes, habits, facts, or references.

- Do not start items with the same opening words.

- Ensure you follow ALL these instructions when creating your output.

# INPUT

INPUT:
"""

def is_valid_youtube_url(url):
    """Validate YouTube URL format."""
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    youtube_regex_match = re.match(youtube_regex, url)
    return bool(youtube_regex_match)

def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    if not is_valid_youtube_url(url):
        print(f"[DEBUG] Invalid YouTube URL: {url}")
        return None
    
    # Handle youtu.be URLs
    if "youtu.be" in url:
        video_id = url.split("/")[-1].split("?")[0]
        print(f"[DEBUG] Extracted video_id from youtu.be: {video_id}")
        return video_id
    
    # Handle youtube.com URLs
    if "youtube.com" in url:
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
            print(f"[DEBUG] Extracted video_id from youtube.com (v=): {video_id}")
            return video_id
        elif "embed/" in url:
            video_id = url.split("embed/")[1].split("?")[0]
            print(f"[DEBUG] Extracted video_id from youtube.com (embed/): {video_id}")
            return video_id
        elif "/v/" in url:
            video_id = url.split("/v/")[1].split("?")[0]
            print(f"[DEBUG] Extracted video_id from youtube.com (/v/): {video_id}")
            return video_id
    print(f"[DEBUG] Could not extract video_id from URL: {url}")
    return None

def get_transcript(video_id, retries=3, delay=2):
    """Get transcript from YouTube video with retry mechanism."""
    print(f"[DEBUG] Attempting to fetch transcript for video_id: {video_id}")
    attempt = 0
    while attempt < retries:
        try:
            # Try to get transcript with auto-generated captions
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=['en', 'en-US', 'en-GB'],  # Try different English variants
                preserve_formatting=True
            )
            formatter = TextFormatter()
            formatted = formatter.format_transcript(transcript)
            print(f"[DEBUG] Successfully fetched transcript for video_id: {video_id}, length: {len(formatted)} characters")
            return formatted
        except TranscriptsDisabled:
            print(f"[DEBUG] Transcripts are disabled for video_id: {video_id}")
            return "Error: This video has transcripts disabled."
        except NoTranscriptFound:
            print(f"[DEBUG] No transcript found for video_id: {video_id}")
            return "Error: No transcript found for this video. The video might not have captions available."
        except Exception as e:
            print(f"[DEBUG] Exception while fetching transcript for video_id: {video_id} (attempt {attempt+1}): {e}")
            attempt += 1
            if attempt < retries:
                print(f"[DEBUG] Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                return f"Error getting transcript after {retries} attempts: {str(e)}"

def process_with_ai(text):
    """Process text with OpenRouter AI."""
    if text.startswith("Error"):
        return text
        
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [
            {
                "role": "system",
                "content": WISDOM_PROMPT
            },
            {
                "role": "user",
                "content": text
            }
        ]
    }
    
    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error processing with AI: {str(e)}"

def format_wisdom_output(markdown_text):
    """Convert markdown to HTML with proper styling."""
    # Configure markdown extensions
    extensions = [
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        'markdown.extensions.nl2br',
        'markdown.extensions.sane_lists'
    ]
    
    # Convert markdown to HTML
    html = markdown.markdown(markdown_text, extensions=extensions)
    
    # Split into sections and wrap each in a styled div
    sections = html.split('<h3>')
    formatted_html = sections[0]  # Keep any content before the first h3
    
    for section in sections[1:]:
        if section.strip():
            # Find the next h3 tag or end of content
            next_section_start = section.find('<h3>')
            if next_section_start != -1:
                # Split at the next h3
                current_section = section[:next_section_start]
                formatted_html += f'<div class="wisdom-section"><h3>{current_section}</div>'
            else:
                # This is the last section
                formatted_html += f'<div class="wisdom-section"><h3>{section}</div>'
    
    return formatted_html

def main():
    st.title("Wisdom Extractor")
    st.write("Extract wisdom and insights from YouTube videos using AI")
    
    # Add custom CSS for consistent formatting
    st.markdown("""
        <style>
        .wisdom-section {
            margin: 1.5em 0;
            padding: 1em;
            border-left: 4px solid #4CAF50;
            background-color: #f8f9fa;
        }
        .wisdom-section h3 {
            color: #2c3e50;
            margin-bottom: 0.5em;
            font-size: 1.4em;
        }
        .wisdom-section ul {
            margin: 0;
            padding-left: 1.5em;
        }
        .wisdom-section li {
            margin: 0.5em 0;
            line-height: 1.4;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state for transcript if not exists
    if 'transcript' not in st.session_state:
        st.session_state.transcript = None
    
    # Initialize session state for processing status
    if 'is_processing' not in st.session_state:
        st.session_state.is_processing = False
    
    # Input for YouTube URL
    youtube_url = st.text_input("Enter YouTube URL:")
    
    # Process new URL if provided and not currently processing
    if youtube_url and not st.session_state.is_processing:
        if not is_valid_youtube_url(youtube_url):
            st.error("Please enter a valid YouTube URL")
            return
            
        video_id = extract_video_id(youtube_url)
        if video_id:
            with st.spinner("Fetching transcript..."):
                transcript = get_transcript(video_id)
                if transcript.startswith("Error"):
                    st.error(transcript)
                    st.session_state.transcript = None
                else:
                    st.session_state.transcript = transcript
    
    # Display transcript if available
    if st.session_state.transcript:
        st.text_area("Transcript:", st.session_state.transcript, height=200)
        
        # Extract Wisdom button
        if st.button("Extract Wisdom", disabled=st.session_state.is_processing):
            try:
                st.session_state.is_processing = True
                with st.spinner("Processing with AI..."):
                    # Use the stored transcript directly
                    stored_transcript = st.session_state.transcript
                    wisdom = process_with_ai(stored_transcript)
                    if wisdom.startswith("Error"):
                        st.error(wisdom)
                        st.info("The transcript is still available above. You can try extracting wisdom again.")
                    else:
                        # Format the wisdom output using proper markdown parsing
                        formatted_wisdom = format_wisdom_output(wisdom)
                        st.markdown(formatted_wisdom, unsafe_allow_html=True)
            finally:
                st.session_state.is_processing = False

if __name__ == "__main__":
    main() 