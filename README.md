
# 🏷️ Tag Extraction System (LangGraph + Groq)

## 🧠 Overview
This project is a **modular Tag Extraction System** built using **LangGraph**, **Groq LLMs**, and **spaCy**.
It demonstrates how to design and implement a *fan-out / fan-in* architecture that combines multiple extraction techniques:

1. **Rule-based Gazetteer Extractor**
2. **ML-based spaCy Named Entity Extractor**
3. **LLM-based Semantic Extractor (via Groq API)**

All three outputs are merged by an **LLM Aggregator Node** that selects the best final tags.

The system is inspired by the *"From Architecture to Implementation: Building the Tag Extraction System (AAIDC -- Week 6 Lesson 2b)"* tutorial from ReadyTensor.

---

## 🚀 Features
- Modular LangGraph pipeline with clear node boundaries.
- Three extraction strategies: rule-based, statistical, and reasoning-based.
- YAML-based prompt configuration for easy LLM customization.
- Uses Groq's latest Llama-3 models for ultra-fast inference.
- Clean separation of configuration, prompts, and logic layers.
- Easily extensible with reflection or verification nodes.

---

## 🧩 Architecture

```

Start\
├── Gazetteer Extractor → gazetteer_tags\
├── spaCy Extractor → spacy_tags\
└── LLM Extractor → llm_tags\
↓\
Aggregation Node (LLM)\
↓\
Final Tags Output

```

Each node processes text and updates the shared LangGraph state.
The Aggregation node combines the results and produces the final curated tag list.

---

## 📁 Folder Structure

```

tag_extractor/\
├── tag_extractor.py # LangGraph workflow\
├── llm_handler.py # Groq-based LLM utility\
├── config.yaml # Global configuration\
├── prompts/\
│ ├── llm_extraction.yaml\
│ └── llm_aggregation.yaml\
├── requirements.txt # Python dependencies\
└── README.md # This file

```

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Hemavathy040726/TagExtractor.git
   cd TagExtractor

```

1.  **Create and activate a virtual environment**

    ```
    python -m venv .venv
    .venv\Scripts\activate    # Windows
    source .venv/bin/activate # macOS/Linux

    ```

2.  **Install dependencies**

    ```
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm

    ```

* * * * *

🧰 Configuration
----------------

Edit `config.yaml` before running:

```
use_llm: true
model: llama-3.1-8b-instant
api_key: YOUR_GROQ_API_KEY_HERE
top_n: 8

```

* * * * *

▶️ Running the Project
----------------------

Run the main workflow from your terminal or PyCharm:

```
python tag_extractor.py

```

**Expected Output:**

```
✅ Gazetteer Extractor → ['LangGraph', 'ReadyTensor', 'LLM']
✅ spaCy Extractor → ['ReadyTensor', 'LangGraph']
✅ LLM Extractor → ['LangGraph', 'AI Systems', 'Agentic Design', 'ReadyTensor', 'LLM']
🏁 Aggregated Final Tags → ['LangGraph', 'ReadyTensor', 'AI Systems', 'Agentic Design', 'LLM']

```

* * * * *

⚙️ How It Works
---------------

1.  **Gazetteer Extractor** -- Uses regex to find known keywords.

2.  **spaCy Extractor** -- Uses `en_core_web_sm` model for Named Entity Recognition.

3.  **LLM Extractor** -- Sends a YAML-configured prompt to Groq LLM.

4.  **Aggregator Node** -- Combines, deduplicates, and ranks all tags using another LLM call.

* * * * *

✍️ Customizing Prompts
----------------------

Modify YAML prompt templates in the `prompts/` directory to change how the LLM behaves.\
Available variables: `{text}`, `{gazetteer_tags}`, `{spacy_tags}`, `{llm_tags}`, `{top_n}`

**Example (`llm_extraction.yaml`):**

```
template: |
  You are an expert tag extractor.
  Extract 5--10 relevant tags from the following text:
  {text}

```

* * * * *

🧩 Troubleshooting
------------------

| Issue | Cause | Solution |
| --- | --- | --- |
| `model_decommissioned` | Old Groq model name | Update `model:` to `llama-3.1-8b-instant` |
| `Can't find model 'en_core_web_sm'` | spaCy model missing | Run `python -m spacy download en_core_web_sm` |
| `InvalidUpdateError` | Multiple nodes writing to same key | Ensure nodes return only new keys (not rewriting `text`) |

* * * * *

🧱 Future Enhancements
----------------------

-   Add a **Reflection Node** to refine or filter tags.

-   Support batch document tagging.

-   Build a simple **web UI** for uploading and viewing tags.

-   Add **SQLite or JSON persistence** for saving tag results.

* * * * *

🪪 License
----------

This project is licensed under the **MIT License**.

* * * * *

💡 Acknowledgements
-------------------

-   [LangGraph](https://github.com/langchain-ai/langgraph) -- for graph-based orchestration.

-   [Groq](https://console.groq.com/) -- for ultra-fast LLM inference.

-   [spaCy](https://spacy.io/) -- for NLP and Named Entity Recognition.

-   [ReadyTensor AAIDC Program](https://app.readytensor.ai/publications/D3vJsJh1500g) -- inspiration for the architecture.

* * * * *

### ⭐ If this helped you learn LangGraph + Groq, consider starring the repo!

