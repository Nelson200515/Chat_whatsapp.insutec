from fastapi import FastAPI, Request
from agente.carregar_agente import carregar_agente

app = FastAPI()

# Carrega o agente uma única vez
agent = carregar_agente()

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()

    try:
        mensagem = (
            data["entry"][0]
                ["changes"][0]
                ["value"]["messages"][0]
                ["text"]["body"]
        )

        resposta = agent.invoke(
            {"question": mensagem},
            config={"configurable": {"session_id": "whatsapp"}}
        )

        return {
            "reply": resposta["answer"]
        }

    except Exception as e:
        return {"error": str(e)}
