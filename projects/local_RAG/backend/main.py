from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import invoke as retriever  # searches all files in /data

app = FastAPI(title="Universal RAG Chatbot API")

origins = ["http://localhost:3001"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM
llm_model = OllamaLLM(model="llama3.2")

# Generic prompt for all file types
prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant that answers questions strictly based on the provided files.
The files may contain CSV, TXT, PDF, DOCX, MD, HTML, or EML content.
Each paragraph or row is prefixed with the filename in square brackets.

Use only the information in the data above. Include the filename in your answer if relevant.
Do not invent any information. If the information is missing, say you don't have enough information.

Relevant data:
{file_rows}

Question:
{query}

Answer:
""")

chain = prompt | llm_model

# Request / Response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Search all files in /data dynamically
        rows = retriever(request.message)

        # Invoke LLM with retrieved data
        result = chain.invoke({
            "query": request.message,
            "file_rows": rows  # matches {file_rows} in prompt
        })

        return ChatResponse(reply=str(result))

    except Exception as e:
        return ChatResponse(reply=f"⚠️ Error: {e}")
