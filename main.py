import os
from dotenv import load_dotenv

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING", "true")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "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")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "default")

# LLM con modelo existente (evita el 404)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

llm = ChatGoogleGenerativeAI(
    model="-2.0- flashgemini-2.0-flash",           # ✅ Modelo válido de Gemini
    google_api_key=google_api_key,
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
