import asyncio
import httpx

from .models import Oauth


def test(message):
    accs = list(Oauth.objects.all().values("id", "incoming_webhook"))

    async def send_messages(message):
        async with httpx.AsyncClient() as client:
            for webhook in accs:
                url = webhook["incoming_webhook"]["url"]
                print(url, message)
                await client.post(
                    url, json={"text": message},
                )

    asyncio.run(send_messages(message))
