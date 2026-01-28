import asyncio
from openai import AsyncOpenAI
import config

client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

async def get_legal_answer(thread_id: str, user_question: str):
    # Добавляем сообщение в поток
    await client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_question
    )
    
    # Запускаем ассистента
    run = await client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=config.ASSISTANT_ID
    )
    
    # Ожидание ответа
    while True:
        run_status = await client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        await asyncio.sleep(1)
    
    # Получаем последнее сообщение
    messages = await client.beta.threads.messages.list(thread_id=thread_id)
    return messages.data[0].content[0].text.value

async def create_thread():
    thread = await client.beta.threads.create()
    return thread.id