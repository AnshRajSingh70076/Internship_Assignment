# main.py
import warnings
warnings.filterwarnings("ignore")

from rag import load_data
from embed import RAG
from agent import build_agent
from tools import CALL_OUTCOMES
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

def main():

    docs = load_data("Call_Dataset.xlsx")

    
    for d in docs:
        CALL_OUTCOMES[d["id"]] = d["outcome"]

    rag = RAG()
    rag.ingest(docs)

    agent = build_agent(rag)

    while True:
        q = input("\nAsk: ")
        if q == "exit":
            break

        result = agent.invoke({"query": q})
        print("\nAnswer:", result["response"])


if __name__ == "__main__":
    main()
