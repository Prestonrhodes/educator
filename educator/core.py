from openai import OpenAI

class LLM:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt, system_prompt="", stream=False):
        messages = [{"role": "system", "content": system_prompt}] if system_prompt else []
        messages.append({"role": "user", "content": prompt})
        if stream:
            return self._stream_generate(messages)
        else:
            response = self.client.chat.completions.create(
                model=self.model, messages=messages, stream=False
            )
            return response.choices[0].message.content if response.choices else "Error: No response"

    def _stream_generate(self, messages):
        response = self.client.chat.completions.create(
            model=self.model, messages=messages, stream=True
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
