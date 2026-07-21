from langchain_ollama import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
import requests

# --- This is the missing function from your test ---
def get_soup(url):
    """Fetch a URL and return a BeautifulSoup object."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

# --- This is your correct, single extract function ---
def extract_text_from_url(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to fetch the page: {exc}") from exc

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    paragraphs = []
    for element in soup.find_all(["p", "h1", "h2", "h3", "li"]):
        text = " ".join(element.get_text(separator=" ", strip=True).split())
        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)

# --- Your summarization function (unchanged, it's good) ---
def summarize_document_with(text: str, model: str = "llama3.2") -> str:
    if not text.strip():
        return "No text available to summarize."

    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    chunks = splitter.split_text(text)

    llm = OllamaLLM(model=model, temperature=0)
    summaries = []
    for chunk in chunks[:3]:
        prompt = f"Summarize the following text in 2 to 3 concise bullet points:\n\n{chunk}"
        summaries.append(str(llm.invoke(prompt)).strip())

    combined_prompt = "Combine these summaries into one short paragraph:\n\n" + "\n\n".join(summaries)
    return str(llm.invoke(combined_prompt)).strip()

# --- Your test block, now working ---
if __name__ == "__main__":
    url = "enter your website here!"
    print("Loading and extracting text...")
    try:
        # This now works because get_soup is defined
        soup = get_soup(url)
        print("Title:", soup.title)
        text = extract_text_from_url(url)
        print("\nExtracted text preview:\n")
        print(text[:1000])
        # Optionally, call the summarizer
        # print("\n--- SUMMARY ---\n")
        # print(summarize_document_with(text))
    except Exception as exc:
        print(f"An error occurred: {exc}")