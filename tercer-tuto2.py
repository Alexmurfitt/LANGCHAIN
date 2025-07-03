import os
from dotenv import load_dotenv
from langchain_core.tools import Tool
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage

# Cargar variables de entorno
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY no está definida")

# Configuración de LangSmith (opcional)
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING", "true")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "default")

# Definir funciones matemáticas
def add_func(a: float, b: float) -> float:
    print(f"➕ Ejecutando suma: {a} + {b} = {a + b}")
    return a + b

def multiply_func(a: float, b: float) -> float:
    print(f"✖️ Ejecutando multiplicación: {a} * {b} = {a * b}")
    return a * b

# Esquemas de entrada
class AddInput(BaseModel):
    a: float = Field(..., description="Primer número")
    b: float = Field(..., description="Segundo número")

class MultiplyInput(BaseModel):
    a: float = Field(..., description="Primer número")
    b: float = Field(..., description="Segundo número")

# Herramientas disponibles
tools = [
    Tool.from_function(name="add", description="Suma dos números", func=lambda x: add_func(**x), args_schema=AddInput),
    Tool.from_function(name="multiply", description="Multiplica dos números", func=lambda x: multiply_func(**x), args_schema=MultiplyInput)
]

# Modelo + herramientas
llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
llm_with_tools = llm.bind_tools(tools)

# Mapeo de nombres a funciones reales
tool_map = {"add": add_func, "multiply": multiply_func}

# Historial de conversación
chat_history = []

print("\n🤖 Gemini ChatBot activo — Escribe 'salir' para terminar\n")

while True:
    user_input = input("🧑 Tú: ").strip()
    if user_input.lower() in {"salir", "exit", "quit"}:
        break

    chat_history.append(HumanMessage(content=user_input))
    response = llm_with_tools.invoke(chat_history)

    if getattr(response, "tool_calls", None):
        print("🛠 El modelo ha solicitado ejecutar herramienta(s):")
        for call in response.tool_calls:
            name = call["name"]
            args = call["args"]
            print(f"  🔧 {name}({args})")
            result = tool_map[name](**args)
            print(f"✅ Resultado de {name}: {result}")
            chat_history.append(AIMessage(content=f"Resultado de {name}: {result}"))
    else:
        print("🤖:", response.content)
        chat_history.append(AIMessage(content=response.content))
