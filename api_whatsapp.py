from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import os
from agente.carregar_agente import carregar_agente

app = FastAPI()

# ✅ Token que você define e coloca também no painel do WhatsApp
VERIFY_TOKEN = "meu_token_secreto123"

# Carrega o agente uma vez
agent = carregar_agente()

# Endpoint GET → usado pelo WhatsApp para validar o webhook
@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        # WhatsApp exige que o challenge seja retornado exatamente
        return PlainTextResponse(content=challenge)
    return PlainTextResponse(content="Token inválido", status_code=403)

# Endpoint POST → usado para receber mensagens
@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    try:
        message_data = data["entry"][0]["changes"][0]["value"]["messages"][0]
        remetente = message_data["from"]
        mensagem = message_data["text"]["body"]

        resposta = agent.invoke(
            {"question": mensagem},
            config={"configurable": {"session_id": remetente}}
        )

        return {"reply": resposta["answer"]}

    except Exception as e:
        return {"error": str(e)}
