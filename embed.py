from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
import os
import re
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")
load_dotenv()

class RAG:
    def __init__(self):
        api_key = os.getenv("PINECONE_API_KEY")

        if not api_key:
            raise ValueError("PINECONE_API_KEY not found")

        # ---------------- EMBEDDINGS ----------------
        self.embed = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # ---------------- PINECONE ----------------
        self.pc = Pinecone(api_key=api_key)

        self.index_name = "call-agent"

        index_list = [i.name for i in self.pc.list_indexes()]

        if self.index_name not in index_list:
            self.pc.create_index(
                name=self.index_name,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

        self.index = self.pc.Index(self.index_name)

        self.vectorstore = PineconeVectorStore(
            index=self.index,
            embedding=self.embed
        )

    # ---------------- CALL NORMALIZER ----------------
    def normalize_call_id(self, text):
        match = re.search(r'(\d+)', str(text))
        if match:
            return f"CALL_{match.group(1).zfill(3)}"
        return None

    # ---------------- INGEST ----------------
    def ingest(self, docs):
        new_texts = []
        new_metadata = []

        for d in docs:
            raw_id = d["id"]
            text = d["text"]

            # normalize CALL ID
            call_id = self.normalize_call_id(raw_id)

            if not call_id:
                continue

            # check existing
            existing = self.vectorstore.similarity_search(
                query="",
                k=1,
                filter={"call_id": call_id}
            )

            if existing:
                continue

            # IMPORTANT: enrich text improves retrieval
            enriched_text = f"{call_id} | {text}"

            new_texts.append(enriched_text)

            # KEEP EXACTLY SAME (as you said)
            new_metadata.append({"call_id": call_id})

        if not new_texts:
            return

        self.vectorstore.add_texts(
            texts=new_texts,
            metadatas=new_metadata
        )

    # ---------------- RETRIEVE (FIXED) ----------------
    def retrieve(self, query):
        call_id = self.normalize_call_id(query)

        # ---------------- LEVEL 1: EXACT CALL MATCH ----------------
        if call_id:
            results = self.vectorstore.similarity_search(
                query="",
                k=2,
                filter={"call_id": call_id}
            )

            if results:
                return results

        # ---------------- LEVEL 2: FUZZY CALL SEARCH ----------------
        # (important fix for "call 001" edge cases)
        results = self.vectorstore.similarity_search(
            query=f"CALL {query}",
            k=2
        )

        if results:
            return results

        # ---------------- LEVEL 3: GENERAL FALLBACK ----------------
        return self.vectorstore.similarity_search(query, k=2)
    # ---------------- GET BY CALL ID (FIXED) ----------------
    def get_by_call_id(self, call_id):
        call_id = self.normalize_call_id(call_id)

        results = self.vectorstore.similarity_search(
            query="",
            k=1,
            filter={"call_id": call_id}
        )

        return results if results else []