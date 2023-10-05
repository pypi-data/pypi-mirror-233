from pypayz.abstract import PayzClient
from pypayz.utils.calculus import calculate_sign
from pypayz.schemas import PayoutBalanceInfo
from typing import Any


class PayoutHost2Host:
    BalanceInfo = PayoutBalanceInfo


    def __init__(self, secret_key: str, wallex_client: WallexClient) -> None:
        self.secret_key = secret_key
        self.wallex_client = wallex_client

    def _calculate_sign(self, data: dict):
        return calculate_sign(self.secret_key, data)

    async def _post_request(self, path, data, calc_sign=True):
        if calc_sign:
            data['sign'] = self._calculate_sign(data)
        response = await self.wallex_client.client.post(path, json=data)
        return response.json()

    async def _payout(self, endpoint: str, data: dict, calc_sign=True) -> dict:
        return await self._post_request(f'/payout{endpoint}', data, calc_sign=calc_sign)

    async def get_balance(self, merchant_id: int) -> BalanceInfo:
        data = await self._payout(
            endpoint='/balance',
            data={
                'merchant': merchant_id
            }
        )
        return self.BalanceInfo(**data)

    async def to_pay_balance(self, merchant_id: int, amount: float) -> Any:
        return await self._payout(
            endpoint='/to_pay_balance',
            data={
                'merchant': merchant_id,
                'amount': amount,
            }
        )
