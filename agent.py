    # agent.py

from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from tools import get_call_outcome, get_sentiment_summary
import re
import os 
import warnings
warnings.filterwarnings("ignore")
# ---------------- LLM ----------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# ---------------- BUILD AGENT ----------------
def build_agent(rag):

    # -------- RETRIEVE NODE (USED ONLY FOR GENERAL QUERIES) --------
    def retrieve_node(state):
        query = state["query"]

        docs = rag.retrieve(query)

        context = "\n".join([
            d["text"] if isinstance(d, dict) else d.page_content
            for d in docs
        ])

        return {
            "query": query,
            "context": context
        }

    # -------- LLM NODE (ROUTER + GENERATOR) --------
    def llm_node(state):

        query = state["query"]
        context = state.get("context", "")
        q_lower = query.lower()

        # ---------------- CALL ID DETECTION ----------------
        match = re.search(r'call[_\s]?(\d+)', q_lower)

        if match:
            call_id = f"CALL_{match.group(1).zfill(3)}"

            # -------- TOOL CALLS --------
            if "outcome" in q_lower or "status" in q_lower:
                return {"response": get_call_outcome(call_id)}

            if "sentiment" in q_lower:
                return {"response": get_sentiment_summary(call_id)}

            # -------- DIRECT FETCH (NO RAG) --------
            docs = rag.get_by_call_id(call_id)

            if docs:
                context = docs[0].page_content   
            else:
                context = ""

        else:
            # -------- USE RAG FOR GENERAL QUERIES --------
            docs = rag.retrieve(query)

            context = "\n".join([
                d["text"] if isinstance(d, dict) else d.page_content
                for d in docs
            ])

        # -------- LLM RESPONSE --------
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a customer support AI.\n"
                    "Rules:\n"
                    "- Use ONLY the provided context\n"
                    "- Do NOT guess\n"
                    "- If no info → say 'No data found'\n"
                    "- Answer in 2-3 lines\n"
                )
            },
            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{query}
"""
            }
        ]

        response = llm.invoke(messages)

        return {"response": response.content}

    # -------- GRAPH --------
    graph = StateGraph(dict)

    graph.add_node("llm", llm_node)

    
    graph.set_entry_point("llm")

    return graph.compile()