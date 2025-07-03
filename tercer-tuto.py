import os
from dotenv import load_dotenv

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY no está definida en el archivo .env")

os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING", "true")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "default")

from langchain_core.tools import Tool
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

def add_func(a: int, b: int) -> int:
    print(f"Ejecutando suma: {a} + {b} = {a + b}")
    return a + b

def multiply_func(a: int, b: int) -> int:
    print(f"Ejecutando multiplicación: {a} * {b} = {a * b}")
    return a * b

class AddInput(BaseModel):
    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")

class MultiplyInput(BaseModel):
    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")

tools = [
    Tool.from_function(
        name="add",
        description="Add two integers",
        func=lambda x: add_func(**x),
        args_schema=AddInput
    ),
    Tool.from_function(
        name="multiply",
        description="Multiply two integers",
        func=lambda x: multiply_func(**x),
        args_schema=MultiplyInput
    )
]

# 🤖 Modelo + herramientas
llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
llm_with_tools = llm.bind_tools(tools)

def handle_response(response):
    if getattr(response, "tool_calls", None):
        print("🛠 El modelo ha solicitado ejecutar herramienta(s):")
        for call in response.tool_calls:
            name = call["name"]
            args = call["args"]
            print(f"  🔧 {name}({args})")
            result = tool_map[name](**args)
            print(f"✅ Resultado de {name}: {result}")
    else:
        print("🧠 Respuesta directa del modelo:", response.content)

# 8. Mapeo de nombre → función real
tool_map = {
    "add": add_func,
    "multiply": multiply_func
}

# 9. Ejecutar consultas
query1 = "What is 3 * 12?"
response1 = llm_with_tools.invoke(query1)
print("\n📤 Respuesta 1:")
handle_response(response1)

query2 = "What is 3 * 12? Also, what is 11 + 49?"
response2 = llm_with_tools.invoke(query2)
print("\n📤 Respuesta 2:")
handle_response(response2)