from __future__ import annotations
from langchain_text_splitters import RecursiveCharacterTextSplitter


class EmbeddingAgent:
    def chunk_documents(self, documents: list[str]) -> list[dict[str, str]]:
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
        chunks = []
        for document in documents:
            for chunk in splitter.split_text(document):
                chunks.append({"text": chunk})
        return chunks

    def store_chunks(self, chunks: list[dict[str, str]], topic: str) -> None:
        for index, chunk in enumerate(chunks):
            chunk["id"] = f"{topic}-{index}"
