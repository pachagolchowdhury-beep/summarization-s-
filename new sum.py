from langchain_ollama import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
import requests


url = "drop your website here!"

r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

header = soup.find('h1')
print(header)

def extract_text_from_url(url: str) -> str: url =" drop your website here!"
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


def summarize_document_with(text: str, model: str = "llama3.2") -> str:
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    chunks = splitter.split_text(text)

    try:
        llm = OllamaLLM(model=model, temperature=0)
        summaries = [str(llm.invoke(f"Summarize:\n\n{chunk}")) for chunk in chunks[:3]]
        return str(llm.invoke("Combine these summaries:\n\n" + "\n\n".join(summaries)))
    except Exception as exc:
        raise RuntimeError(
            f"Summarization failed. Make sure Ollama is running and the model '{model}' is installed. Original error: {exc}"
        ) from exc


def main() -> None:
    url = "drop your website here!"
    try:
        text = extract_text_from_url(url)
        print("Extracted text length:", len(text))
        print(summarize_document_with(text))
    except Exception as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()