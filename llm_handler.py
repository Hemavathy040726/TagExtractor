import yaml
from groq import Groq
from groq.types.chat import ChatCompletionUserMessageParam


class LLMHandler:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.client = Groq(api_key=self.config.get("api_key"))
        self.model = self.config.get("model", "llama-3.1-8b-instant")
        self.use_llm = self.config.get("use_llm", True)

    def load_prompt(self, path: str) -> str:
        import yaml
        with open(path, "r") as f:
            y = yaml.safe_load(f)
        return y["template"]

    def render_prompt(self, template: str, **kwargs) -> str:
        return template.format(**kwargs)

    def query(self, prompt: str) -> list:
        if not self.use_llm:
            return ["LangGraph", "AI Systems", "Agentic Design", "ReadyTensor", "LLM"]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                ChatCompletionUserMessageParam(role="user", content=prompt)
            ],
            temperature=0.3
        )
        content = response.choices[0].message.content.strip()
        return [t.strip() for t in content.split(",") if t.strip()]
