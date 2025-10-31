from langgraph.graph import StateGraph, END
from typing import List, TypedDict
import re
import spacy
from llm_handler import LLMHandler



class TagState(TypedDict, total=False):
    text: str
    gazetteer_tags: List[str]
    spacy_tags: List[str]
    llm_tags: List[str]
    final_tags: List[str]



# ========== Helper Extractors ==========
def gazetteer_extractor(state):
    text = state["text"]
    keywords = ["AI", "LLM", "LangGraph", "ReadyTensor", "agents"]
    found = [kw for kw in keywords if re.search(rf"\b{kw}\b", text, re.IGNORECASE)]
    print("✅ Gazetteer Extractor →", found)
    new_state = {"gazetteer_tags": found}
    return new_state


def spacy_extractor(state):
    text = state["text"]
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    tags = list(set(ent.text for ent in doc.ents))
    print("✅ spaCy Extractor →", tags)
    new_state = {"spacy_tags": tags}
    return new_state


def llm_extractor(state):
    text = state["text"]
    llm = LLMHandler("config.yaml")
    prompt = llm.load_prompt("prompts/llm_extraction.yaml")
    rendered = llm.render_prompt(prompt, text=text)
    tags = llm.query(rendered)
    print("✅ LLM Extractor →", tags)
    new_state = {"llm_tags": tags}
    return new_state


def aggregator(state):
    llm = LLMHandler("config.yaml")
    prompt = llm.load_prompt("prompts/llm_aggregation.yaml")
    rendered = llm.render_prompt(
        prompt,
        gazetteer_tags=state["gazetteer_tags"],
        spacy_tags=state["spacy_tags"],
        llm_tags=state["llm_tags"],
        top_n=llm.config["top_n"]
    )
    tags = llm.query(rendered)
    print("\n🏁 Aggregated Final Tags →", tags)
    state["final_tags"] = tags
    return state


# ========== LangGraph Wiring ==========
graph = StateGraph(TagState)

# Start node → three parallel extractors
graph.add_node("gazetteer", gazetteer_extractor)
graph.add_node("spacy", spacy_extractor)
graph.add_node("llm", llm_extractor)
graph.add_node("aggregate", aggregator)

graph.add_edge("gazetteer", "aggregate")
graph.add_edge("spacy", "aggregate")
graph.add_edge("llm", "aggregate")
graph.add_edge("aggregate", END)

graph.set_entry_point("gazetteer")  # first branch
graph.set_entry_point("spacy")      # second branch
graph.set_entry_point("llm")        # third branch

# Compile the graph
app = graph.compile()

# ========== Run the Workflow ==========
if __name__ == "__main__":
    text = """
    LangGraph is an open-source framework for building modular AI systems.
    It helps orchestrate agents, LLMs, and tools efficiently.
    The ReadyTensor AAIDC course teaches how to design agentic architectures.
    """

    state = {"text": text}
    app.invoke(state)
