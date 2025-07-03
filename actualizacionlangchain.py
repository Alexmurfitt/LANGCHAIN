# 🔁 Migración recomendada: RunnableWithMessageHistory
# Aquí tienes cómo actualizar tu código para estar alineado con las versiones modernas de LangChain (v0.2.7+):
 
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import ChatMessageHistory
from langchain_core.runnables import Runnable

# Tu modelo LLM sigue igual:
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=google_api_key,
    temperature=0.3
)

# Define la historia de mensajes
chat_history = ChatMessageHistory()

# Encadena el modelo con la historia de mensajes
chat_chain = RunnableWithMessageHistory(
    Runnable(lambda input: llm.invoke(input)),  # procesamiento
    lambda session_id: chat_history,           # backend de memoria
)

# Interfaz de usuario
print("\n🧠 Gemini ChatBox (v2) — escribe 'exit' para salir\n")

session_id = "usuario1"  # se puede usar por usuario
while True:
    user_input = input("Tú: ").strip()
    if user_input.lower() in {"exit", "quit"}:
        break
    try:
        response = chat_chain.invoke({"input": user_input}, config={"configurable": {"session_id": session_id}})
        print("🤖:", response, "\n")
    except Exception as e:
        print("⚠️ Error:", e, "\n")
