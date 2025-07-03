import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Carga la API key desde .env
load_dotenv()

# LLM con modelo existente (evita el 404)
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-pro-latest",  # ✅ modelo disponible
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    google_api_version="v1",               # ✅ versión correcta
    temperature=0.3
)

memory = ConversationBufferMemory(return_messages=True)
chat_chain = ConversationChain(llm=llm, memory=memory)

# UI simple
print("\n🧠 Gemini ChatBox — escribe 'exit' para salir\n")

while True:
    user_input = input("Tú: ").strip()
    if user_input.lower() in {"exit", "quit"}:
        break
    try:
        response = chat_chain.predict(input=user_input)
        print("🤖:", response, "\n")
    except Exception as e:
        print("⚠️ Error:", e, "\n")
