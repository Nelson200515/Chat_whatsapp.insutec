from fastapi import FastAPI, Request
from agente.carregar_agente import carregar_agente

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()

    try:
        message_data = data["entry"][0]["changes"][0]["value"]["messages"][0"]
        remetente = message_data["from"]
        mensagem = message_data["text"]["body"]

        resposta = agent.invoke(
            {"question": mensagem},
            config={"configurable": {"session_id": remetente}}
        )

        return {"reply": resposta["answer"]}

    except Exception as e:
        return {"error": str(e)}

