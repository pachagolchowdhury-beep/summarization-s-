import os
import re
import nltk
import pytube
from youtube_transcript_api import YouTubeTranscriptApi
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from heapq import nlargest
from urllib.parse import parse_qs, urlparse
import textwrap
from colorama import Fore, Style, init
from openai import OpenAI

init(autoreset=True)


nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

client=OpenAI(
    base_url="https://api.openai.com/v1",
    api_key="Drop your api key here 2!",
)


def extract_video_id(url: str) -> str:
    parsed_url = urlparse(url)

   
    if parsed_url.netloc == 'youtu.be':
        return parsed_url.path.lstrip('/')

    
    if parsed_url.netloc in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            video_id = parse_qs(parsed_url.query).get('v', [None])[0]
            if video_id is None:
                raise ValueError(f"Unable to extract video ID from URL: {url}")
            return video_id
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
        elif parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]

   
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if match:
        return match.group(1)

    raise ValueError(f"Unsupported YouTube URL: {url}")


def get_transcript(video_id: str) -> str:
    try:
       
        ytt_api = YouTubeTranscriptApi()
        fetched = ytt_api.fetch(video_id)
        texts = []
        for entry in fetched:
            if isinstance(entry, dict) and 'text' in entry:
                texts.append(entry['text'])
            elif hasattr(entry, 'text'):
                texts.append(entry.text)
            else:
              
                texts.append(str(entry))
        return ' '.join(texts)
    except Exception as e:
        return f"Error retrieving transcript: {str(e)}"


def summarize_text_nltk(text: str, num_sentences: int = 5) -> str:
    """Simple extractive summarization using frequency scoring (NLTK)."""
    if not text or text.startswith("Error"):
        return text

    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text

    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    words = [w for w in words if w.isalnum() and w not in stop_words]

    freq = FreqDist(words)

    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in freq:
                sentence_scores[i] = sentence_scores.get(i, 0) + freq[word]

    top_indices = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    top_indices.sort()
    summary = ' '.join([sentences[i] for i in top_indices])
    return summary


def summarize_text_ai(text: str, video_title: str, num_sentences: int = 5) -> str:
    """Placeholder for AI summarization. Returns a short heuristic summary if no AI client is configured."""
    
    return text

    sentences = sent_tokenize(text)
    return ' '.join(sentences[:num_sentences])


def summarize_youtube_video(youtube_url: str, num_sentences: int = 5) -> dict:
    """Main function: fetch transcript, title, and produce summaries."""
    try:
        video_id = extract_video_id(youtube_url)
    except Exception as e:
        return {"error": str(e)}

    transcript = get_transcript(video_id)
    if transcript.startswith("Error"):
        return {"error": transcript}

    try:
        yt = pytube.YouTube(youtube_url)
        video_title = yt.title
    except Exception:
        video_title = "Unknown Title"

    nltk_summary = summarize_text_nltk(transcript, num_sentences)
    ai_summary = summarize_text_ai(transcript, video_title, num_sentences)

    full_len = len(transcript.split())
    return {
        "video_title": video_title,
        "video_id": video_id,
        "ai_summary": ai_summary,
        "nltk_summary": nltk_summary,
        "full_transcript_length": full_len,
        "nltk_summary_length": len(nltk_summary.split()),
        "ai_summary_length": len(ai_summary.split()),
    }


def format_time(seconds: int) -> str:
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    if minutes > 0:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"


def print_boxed_text(text: str, width: int = 80, title: str | None = None, color: str = Fore.RED):
    wrapper = textwrap.TextWrapper(width=width - 4)
    lines = wrapper.wrap(text)
    horiz = '─' * (width - 2)
    print(color + '┌' + horiz + '┐')
    if title:
        title_line = title.center(width - 2)
        print(color + '│' + title_line + '│')
        print(color + '├' + horiz + '┤')
    for line in lines:
        print(color + '│ ' + line.ljust(width - 4) + ' │')
    print(color + '└' + horiz + '┘')


def print_summary_result(result: dict, width: int = 100):
    if 'error' in result:
        print_boxed_text(f"Error: {result['error']}", width=width, title="ERROR", color=Fore.MAGENTA)
        return

    terminal_width = width
    print(Fore.YELLOW + "=" * terminal_width)
    title = (result.get('video_title') or 'YouTube Summary').center(terminal_width)
    print(Fore.YELLOW + Style.BRIGHT + title)
    print(Fore.YELLOW + "=" * terminal_width + "\n")

    print(Fore.BLUE + "VIDEO INFORMATION".center(terminal_width))
    print(f"Video ID: {result['video_id']}")
    print(f"Transcript words: {result['full_transcript_length']}")
    print(Fore.BLUE + "─" * terminal_width)

    print(Fore.RED + Style.BRIGHT + "AI SUMMARY".center(terminal_width))
    print(result['ai_summary'])
    print(Fore.BLUE + "─" * terminal_width)

    print(Fore.GREEN + Style.DIM + "NLTK SUMMARY".center(terminal_width))
    print(result['nltk_summary'])
    print(Fore.BLUE + "─" * terminal_width)


if __name__ == '__main__':
    try:
        terminal_width = os.get_terminal_size().columns
        terminal_width = max(60, min(terminal_width, 140))
    except Exception:
        terminal_width = 80

    print(Fore.RED + Style.BRIGHT + "\n" + "=" * terminal_width)
    print(Fore.RED + Style.BRIGHT + "YOUTUBE VIDEO SUMMARIZER".center(terminal_width))
    print(Fore.RED + Style.BRIGHT + "=" * terminal_width + "\n")

    youtube_url = input(Fore.MAGENTA + "Enter YouTube video URL: " + Fore.WHITE)
    num_sentences_input = input(Fore.YELLOW + "Enter number of sentences for summaries (default 5): " + Fore.WHITE)
    num_sentences = int(num_sentences_input) if num_sentences_input.strip() else 5

    print(Fore.YELLOW + "\nFetching and analyzing video transcript... Please wait...\n")
    result = summarize_youtube_video(youtube_url, num_sentences)
    print_summary_result(result, width=terminal_width)
