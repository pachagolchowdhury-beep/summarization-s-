# summarization-s-

A collection of scripts for quickly getting the gist of long content — web articles/news, and YouTube videos — without reading or watching the whole thing. PDF and image-based summarization are planned but not implemented yet.

> **Status: work in progress.** This repo currently has a few overlapping/experimental scripts rather than one clean entry point. See [Repo structure](#repo-structure) below for what each file actually does before you run anything.

## Features

- **Web/article summarization** — pulls the readable text out of a webpage and summarizes it locally using [Ollama](https://ollama.com) + [LangChain](https://python.langchain.com/).
- **YouTube video summarization** — pulls the transcript of a YouTube video and produces two summaries side by side: a quick extractive summary (NLTK, no API calls) and an AI-generated abstractive summary (via [OpenRouter](https://openrouter.ai/)).
- **PDF / image support** — planned, not yet in the repo.

## Repo structure

This repo has a few scripts that do similar things at different stages of "working." Worth knowing before you dive in:

| File | What it does | Status |
|---|---|---|
| `attempt.py` | Fetches a URL, strips it down to text, and summarizes it with a local Ollama model. Has a working `__main__` test block. | Most complete web summarizer |
| `new sum.py` | An earlier/alternate version of the same idea. Has some leftover debug code (a stray `soup.find('h1')` print) and a bug — `extract_text_from_url` redefines the `url` parameter with a placeholder string inside the function. | Superseded by `attempt.py` — kept for reference |
| `youtube-summ pt 1` | Full YouTube summarizer: extracts the video ID, pulls the transcript, and runs both an NLTK extractive summary and an OpenRouter AI summary. Nicely formatted terminal output. | Working, but has a hardcoded API key placeholder (see [Security note](#security-note)) |
| `youtube-summ pt 2` | Continuation/variant of the YouTube summarizer. | Check before running — likely overlaps with pt 1 |

**Heads up:** the YouTube scripts have no `.py` extension in the repo — rename them locally (e.g. `youtube_summ_pt1.py`) before running.

## Requirements

Install into a fresh virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows

pip install langchain langchain-ollama langchain-text-splitters
pip install requests beautifulsoup4 requests-html
pip install pypdf                      # for planned PDF support
pip install nltk pytube youtube-transcript-api colorama openai urllib3
```

You'll also need:

- **[Ollama](https://docs.ollama.com)** installed and running locally, with a model pulled (the scripts default to `llama3.2`):
  ```bash
  ollama pull llama3.2
  ```
- **An OpenRouter API key** ([get one here](https://platform.openai.com/api-keys)) for the AI-generated YouTube summary. The `openai` Python package is used with OpenRouter's base URL, not OpenAI directly.

## Usage

### Summarize a web article

Open `attempt.py` and replace the placeholder in the `__main__` block:

```python
url = "enter your website here!"  # <-- put your URL here
```

Then run:

```bash
python attempt.py
```

It prints the page title and a preview of the extracted text. Uncomment the `summarize_document_with(text)` call at the bottom to also get a local LLM summary.

### Summarize a YouTube video

Open `youtube-summ pt 1` and replace the hardcoded API key with your own (see [Security note](#security-note)), then run it:

```bash
python "youtube-summ pt 1"
```

You'll be prompted for a YouTube URL and how many sentences you want in the summary. It prints:
- an NLTK-based extractive summary (fast, free, works offline once the transcript is fetched)
- an AI-generated summary via OpenRouter

## Security note

`youtube-summ pt 1` currently has an API key placeholder hardcoded directly in the source:

```python
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="drop your api key here!",
)
```

**Don't commit a real key here.** Before running it locally, either paste your key in temporarily (and don't push that change), or better, load it from an environment variable:

```python
import os
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
```

## Roadmap

- [ ] Merge `attempt.py` and `new sum.py` into a single, working web summarizer
- [ ] Consolidate `youtube-summ pt 1` / `pt 2` into one script
- [ ] Add PDF summarization
- [ ] Add image-based (OCR) summarization
- [ ] Move API keys and model names to environment variables / a config file
- [ ] Add a `requirements.txt`
- [ ] Rename the YouTube scripts with a `.py` extension

## License

Not yet specified.
