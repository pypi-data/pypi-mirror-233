from json import JSONDecodeError

from pypayz.abstract import PayzClient
from pypayz.utils import calculate_sign
from pypayz.schemas import (
    ExchangeCreationModel,
    ExchangeDealCreateModel,
    PaymentMethodEnum,
    ExchangeOffersResponseModel,
    ExchangeBuyRequestModel,
    ExchangeBuyFiatRequestModel,
    ExchangeAcquiringResponseModel,
    ExchangeGetResponse,
    ExchangeGetPaymentCredentialsResponse,
    ExchangeGetAddressResponse,
    ExchangeHistoryResponse,
)
from datetime import date


class Exchange:
    PaymentMethodEnum = PaymentMethodEnum
    ExchangeModel = ExchangeCreationModel
    DealModel = ExchangeDealCreateModel
    OffersModel = ExchangeOffersResponseModel
    BuyModel = ExchangeBuyRequestModel
    BuyFiatModel = ExchangeBuyFiatRequestModel
    AcquiringModel = ExchangeAcquiringResponseModel
    GetResponse = ExchangeGetResponse
    PaymentCredentials = ExchangeGetPaymentCredentialsResponse
    Address = ExchangeGetAddressResponse
    History = ExchangeHistoryResponse


    def __init__(
        self,
        secret_key: str,
        payz_client: PayzClient,
    ) -> None:
        self.payz_client = payz_client
        self.secret_key = secret_key

    def _calculate_sign(self, data: dict):
        return calculate_sign(self.secret_key, data)

    async def _post_request(self, path, data, calc_sign=True):
        if calc_sign:
            data['sign'] = self._calculate_sign(data)
        response = await self.payz_client.client.post(path, data=data)
        try:
            return response.json()
        except JSONDecodeError:
            return {}
    
    async def _get_request(self, path: str):
        response = await self.payz_client.client.get(path)
        return response.json()

    async def _exchange_get(self, endpoint: str) -> dict:
        return await self._get_request(f"/exchange{endpoint}")

    async def _exchange(self, endpoint: str, data: dict, calc_sign=True) -> dict:
        return await self._post_request(f'/exchange{endpoint}', data, calc_sign=calc_sign)

    async def create(self, merchant_id: str, data: ExchangeModel) -> dict:
        return await self._exchange(f'/create/{merchant_id}', data.dict())

    async def create_deal(self, merchant_id: str, data: DealModel) -> dict:
        return await self._exchange(f'/create_deal/{merchant_id}', data.dict())

    async def get_offers(self, payment_id: str) -> OffersModel:
        data = await self._exchange_get(f'/offers?id={payment_id}')
        return self.OffersModel(**data)

    async def buy(self, data: BuyModel) -> dict:
        return await self._exchange(f'/buy', data.dict(), calc_sign=False)

    async def buy_fiat(self, data: BuyFiatModel) -> dict:
        return await self._exchange('/buy_fiat', data.dict(), calc_sign=False)

    async def get_acquiring(self, payment_id: str) -> AcquiringModel:
        data = await self._exchange_get(f'/acquiring?id={payment_id}')
        return self.AcquiringModel(**data)

    async def get(self, payment_id: str) -> GetResponse:
        data = await self._exchange_get(f'/get?id={payment_id}')
        return self.GetResponse(**data)

    async def get_payment_credentials(self, payment_id: str) -> PaymentCredentials:
        data = await self._exchange_get(f'/get_payment_credentials?id={payment_id}')
        return self.PaymentCredentials(**data)

    async def get_address(self, payment_id: str) -> Address:
        data = await self._exchange_get(f'/address?id={payment_id}')
        return self.Address(**data)

    async def confirm(self, id: str, buy_id: str) -> dict:
        return await self._exchange(
            '/confirm',
            data={
                'id': id,
                'buyId': buy_id,
            },
            calc_sign=False,
        )

    async def cancel(self, id: str, buy_id: str) -> dict:
        return await self._exchange(
            '/cancel',
            data={
                'id': id,
                'buyId': buy_id,
            },
            calc_sign=False,
        )

    async def get_history(self, wallet: str, from_: date, to_: date) -> dict:
        parameters = f"wallet={wallet}&from={from_.strftime('%Y-%m-%d')}&to={to_.strftime('%Y-%m-%d')}"
        return await self._exchange_get(f'/history?{parameters}')

