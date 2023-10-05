import httpx


class PayzClient:
    def __init__(
        self,
        api_key=None,
        *,
        client: httpx.AsyncClient = None,
        base_url = 'https://payz.team'
    ):
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        if api_key:
            self.headers['X-Api-Key'] = api_key

        if not client:
            client = httpx.AsyncClient()
        
        client.base_url = base_url
        client.headers = self.headers

        self.client = client


    async def close(self):
        await self.client.aclose()
