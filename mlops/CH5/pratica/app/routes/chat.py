"""
Rota de chat — endpoint principal do serviço.
"""

from fastapi import APIRouter, Body, HTTPException, status

from client import get_client
from models import ChatMessage, ChatRequest, ChatResponse
from prompts import SYSTEM_PROMPT

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest = Body(
        ...,
        example={
            "messages": [{"role": "user", "content": "Olá! Quem é você?"}],
            "model": "gemini-2.5-flash",
        },
    ),
):
    """
    Envia mensagens para um LLM (Gemini) e retorna a resposta.

    O sistema injeta automaticamente o SYSTEM_PROMPT antes das mensagens
    do usuário para definir o comportamento do assistente.

    Exemplo de request:
        POST /chat
        {
          "messages": [{"role": "user", "content": "Olá! Quem é você?"}],
          "model": "gemini-2.0-flash"
        }
    """
    client = get_client()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += [{"role": m.role, "content": m.content} for m in request.messages]

    try:
        response = await client.chat.completions.create(
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erro ao chamar o modelo: {e}",
        ) from e

    return ChatResponse(
        message=ChatMessage(
            role="assistant",
            content=response.choices[0].message.content,
        ),
        model=response.model,
        usage=response.usage.model_dump() if response.usage else {},
    )
