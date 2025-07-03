````markdown
# 🚀 LangChain + Gemini ChatBot — README ultra-eficiente

Aprende, instala y escala en **minutos** un chatbot con cálculo aritmético usando  
LangChain (🧰 tools + memoria), Gemini 2.0 Flash (Google), y observabilidad LangSmith.

---

## 1. Qué es cada cosa — en 1 línea

| Herramienta | Idea en una frase | Úsala cuando… |
|-------------|------------------|----------------|
| **LangChain** | Framework que conecta LLM ↔ prompts ↔ tools ↔ memoria. | Necesitas un MVP con IA. |
| **LangGraph** | Orquesta flujos complejos como grafos con estado. | Multi-agente / loops. |
| **LangSmith** | Dashboard de trazas, latencia y A/B. | Tu app llega a producción. |

---

## 2. Instalación rápida

```bash
python -m venv myenv && source myenv/bin/activate   # Win: myenv\Scripts\activate
pip install -U langchain langchain-google-genai google-generativeai python-dotenv pydantic
````

`.env` mínimo:

```env
GOOGLE_API_KEY=TU_CLAVE_GOOGLE
LANGSMITH_TRACING=true           # opcional
LANGSMITH_PROJECT=default
```

---

## 3. Código completo (chat + suma/multiplica)

```python
import os, sys
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.tools import Tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage

# ── load keys ──
load_dotenv(); key = os.getenv("GOOGLE_API_KEY") or sys.exit("Falta GOOGLE_API_KEY")

# ── math tools ──
def add(a: float, b: float):  return a + b
def mul(a: float, b: float):  return a * b

class AB(BaseModel): a: float = Field(...); b: float = Field(...)

tools = [ Tool.from_function("add", "Suma",  lambda x: add(**x), AB),
          Tool.from_function("multiply", "Multiplica", lambda x: mul(**x), AB) ]

# ── LLM + binding ──
llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
bot = llm.bind_tools(tools)
tool_map = {"add": add, "multiply": mul}
chat = []

print("\n🤖 Escribe 'salir' para terminar\n")
while True:
    msg = input("Tú: ").strip()
    if msg.lower() in {"salir","exit","quit"}: break
    chat.append(HumanMessage(content=msg))
    res = bot.invoke(chat)
    if getattr(res,"tool_calls",None):
        for call in res.tool_calls:
            r = tool_map[call['name']](**call['args'])
            print(f"🔧 {call['name']} → {r}")
            chat.append(AIMessage(content=str(r)))
    else:
        print("🤖", res.content)
        chat.append(AIMessage(content=res.content))
```

**Cómo funciona?**

1. El usuario pregunta → Gemini detecta que es cálculo.
2. Invoca `add` / `multiply` vía `tool_calls`.
3. Python ejecuta y responde con resultado.

---

## 4. Solución de errores típicos

| Error                               | Causa                        | Fix inmediato                        |
| ----------------------------------- | ---------------------------- | ------------------------------------ |
| `NameError: ChatGoogleGenerativeAI` | Falta import/paquete         | `pip install langchain-google-genai` |
| 404 / 429 modelo                    | ID inválido/cuota            | Usa `gemini-2.0-flash`               |
| Deprecations ≥0.2.7                 | `ConversationChain` obsoleta | Usa `RunnableWithMessageHistory`     |

---

## 5. Escala siguiente (1 frase cada uno)

* **Divide / Subtract** → añade nuevas tools + esquemas.
* **Router Chain** → rutea preguntas a experto física/history.
* **Agente ReAct** → pensamiento paso a paso con múltiples actions.
* **RAG** → Pinecone / Chroma para contexto externo.
* **LangSmith** → mide coste €, latencia y calidad en dashboard.
* **FastAPI / Streamlit** → conviértelo en API o web demo.

---

## 6. Roadmap experto (orden recomendado)

1. Domina prompts + tools + memoria.
2. Agents (ReAct → MRKL → Plan\&Execute).
3. LangGraph para loops & multi-agente.
4. Retrieval-Augmented Generation.
5. Observabilidad continua (LangSmith).
6. Despliegue Docker + CI/CD.

---

### Recursos clave

* Docs LangChain → [https://python.langchain.com/](https://python.langchain.com/)
* Gemini API → [https://ai.google.dev/docs](https://ai.google.dev/docs)
* Curso Agents & RAG → LangChain U
* LangSmith Blog → ejemplos de observabilidad

---

**Con \~120 líneas de código** tienes un chatbot con herramientas matemáticas, extensible y trazable.
¡Practica, itera y escala! 🚀

```
```



