import os
from groq import Groq

cle = os.environ.get("GROQ_API_KEY")
if not cle:
    raise SystemExit("GROQ_API_KEY absente : exportez-la dans le terminal courant.")

client = Groq(api_key=cle)
reponse = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "Réponds : OK"}],
)
print(reponse.choices[0].message.content)
