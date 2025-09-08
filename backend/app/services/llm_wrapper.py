from transformers import pipeline

class LLMWrapper:
    def __init__(self, model_name: str = "gpt2"):
        # Use a small generative model for local inference
        self.generator = pipeline('text-generation', model=model_name)

    def generate_answer(self, prompt: str) -> str:
        # Generate answer using the model
        result = self.generator(prompt, max_length=200, num_return_sequences=1)
        return result[0]['generated_text']
