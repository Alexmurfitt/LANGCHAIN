import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carga las variables definidas en .env (incluida GOOGLE_API_KEY)
load_dotenv()

# O, si prefieres, pásala explícitamente:
# genai.configure(api_key="AIzaSy...")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("\n📋 Modelos disponibles:")
for m in genai.list_models():
    print(" •", m.name, "→", m.supported_generation_methods)
