from pypayz.abstract import PayzClient
from pypayz.schemas import FiatPayModel, CryptoPayModel
from pypayz.utils import calculate_sign


class Payout:
    CRYPTO = 'crypto'
    FIAT = 'fiat'
    FiatPayModel = FiatPayModel
    CryptoPayModel = CryptoPayModel

    def __init__(self, merchant_id, secret_key, payz_client=None):
        self.merchant_id = merchant_id
        self.secret_key = secret_key
        self.client = payz_client or PayzClient()

    async def _post_request(self, path, data):
        data['sign'] = self._calculate_sign(data)
        response = await self.client.client.post(path, json=data)
        return response.json()

    def _calculate_sign(self, data: dict):
        return calculate_sign(self.secret_key, data)

    async def _payout(self, endpoint: str, data: dict = None):
        if data is None:
            data = {}
        data = {
            **data,
            'merchant': self.merchant_id,
        } 
        return await self._post_request(endpoint, data)

    async def get_all(self):
        return await self._payout('/payout/list')

    async def crypto_pay(self, data: CryptoPayModel):
        return await self._payout('/payout/new', data.dict())

    async def fiat_pay(self, data: FiatPayModel):
        return await self._payout('/payout/new', data.dict())

    async def pay_to_balance(self, amount: float):
        return await self._payout('/payout/to_pay_balance', {'amount': amount})

    async def convert(self, amount: float, currency: str):
        return await self._payout(
            '/payout/to_pay_balance',
            data = {
                'amount': amount,
                'currency': currency,
            }
        )
