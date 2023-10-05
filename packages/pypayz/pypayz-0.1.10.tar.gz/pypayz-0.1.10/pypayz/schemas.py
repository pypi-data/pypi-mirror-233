from pydantic import BaseModel
from enum import Enum
from typing import Any, List, Dict


class PaymentMethodEnum(str, Enum):
    SBER = "335"
    TINKOFF = "338"
    PRIVATBANK = "378"
    ABANK24 = "435"
    MONOBANK = "394"
    PUMB = "352"
    VLASNIY_RAHUNOK = "438"
    IZIBANK = "439"
    BANK_CREDIT_DNIPRO = "440"
    BANK_PIVDENNYY = "441"
    KREDIT_AGRICOLE = "442"
    OTP_BANK = "443"
    RAIFFEISEN = "330"
    KREDO_BANK = "444"
    IDEA_BANK = "445"
    SPORTBANK = "446"
    TASKOMBANK = "447"
    UKRSIBBANK = "353"
    NEO = "437"
    CONCORD = "448"
    ANY_BANK = "449"
    FROM_CARD_TO_CARD = "450"


class PaymentStatusEnum(Enum):
    NEW = 0
    PROCESSING = 1
    TRANSITION_TO_3DS = 2
    ERROR_CANCEL = 3
    SUCCESS = 4


class ResponseWithStatusModel(BaseModel):
    success: bool


class ResponseWithItem(ResponseWithStatusModel):
    item: bool | None | Any = None


class FiatPayModel(BaseModel):
    amount: str
    currency: str
    bank: str
    number: str
    month: int
    year: int
    fiat: str
    cardholder: str
    date_of_birth: str
    type: str = 'fiat'


class CryptoPayModel(BaseModel):
    amount: str
    currency: str
    type: str = 'crypto'
    address: str


class BasePaymentModel(BaseModel):
    client: str
    product: str
    price: str
    quantity: int
    currency: str = 'USDT'
    fiat_currency: str = 'rub'
    message: str
    description: str
    language: str = 'ru'


class BasePaymentModel2(BaseModel):
    client: str
    product: str
    price: str
    quantity: int
    currency: str = 'USDT'
    fiat_currency: str = 'rub'
    uuid: str
    message: str
    description: str
    language: str = 'ru' 


class PaymentModel(BasePaymentModel):
    uuid: str | None = None


class ExchangeCreationModel(BasePaymentModel2):
    card_number: str = None  # Optional field


class ExchangeDealCreateModel(ExchangeCreationModel):
    payment_method_id: PaymentMethodEnum


class ExchangeOffersPaymentMethod(BaseModel):
    id: str
    name: str


class ExchangeAd(BaseModel):
    id: int
    payment_method: ExchangeOffersPaymentMethod
    paymentUrl: str
    escrow_time: int
    isOnline: bool
    service: str
    price: str
    payment_credentials: str
    userId: str
    fiatCurrency: str
    amount: int


class ExchangeOffersResponseModel(BaseModel):
    ads: List[ExchangeAd]
    success: bool


class ExchangeBuyRequestModel(BaseModel):
    id: str  # ID заявки на оплату
    buyId: str  # ID оффера
    service: str  # Поле service из оффера


class ExchangeBuyFiatRequestModel(ExchangeBuyRequestModel):
    cardNumber: str  # Номер карты (Visa/Mastercard)
    expires: str  # Срок действия карты (MM/YY)
    cvc: str  # CVC карты
    checkEmail: str  # Email для отправки чека
    cardTo: str  # Номер карты получателя платежа (только для эквайринга)


class ExchangeAcquiringItem(BaseModel):
    id: int  # Код оплаты полученный в методе buy_fiat
    currency: str  # Валюта оплаты
    amount: float  # Сумма оплаты
    uuid: str  # UUID оплаты (для H2H не требуется)
    card_to: str  # Карта с которой идет перевод
    created_at: str  # Дата создания заявки
    bank_error_code: str  # Код ошибки банка в случае отказа
    status: PaymentStatusEnum  # Статус оплаты (0 - Новая, 1 - Обработка, 2 - Переход на 3DS, 3 - Ошибка/отмена, 4 - Успех)


class ExchangeAcquiringResponseModel(ResponseWithItem):
    item: ExchangeAcquiringItem | bool | None = None


class DealInfo(BaseModel):
    id: str  # ID сделки
    status: int  # Статус сделки
    amount: str  # Сумма сделки
    cost: str  # Стоимость сделки


class ExchangeGetResponse(BaseModel):
    status: int | bool | None = None  # Статус платежа
    deal_info: DealInfo | None  # Информация о сделке
    payment_url: str | None  # URL для платежа
    payment_name: str | None  # Название платежа
    end_pay_time: str | None  # Время завершения платежа


class ExchangeGetPaymentCredentialsResponse(BaseModel):
    paymentCredentials: str | None  # Реквизиты
    cardholderName: str | None  # Имя держателя карты
    shortCode: str | None  # Короткий код (описание отсутствует)
    bicCode: str | None  # BIC для переводов евро
    paymentComment: str | None  # Комментарий к переводу
    success: bool  # Успешность операции


class ExchangeGetAddressResponse(BaseModel):
    success: bool  # Успешность операции
    address: str | None  # Адрес для оплаты
    currency: str | None  # Название криптовалюты


class ExchangeHistoryResponse(ResponseWithStatusModel):
    id: int | None  # ID транзакции
    wallet: str | None  # Валюта (rub. eur, usdt)
    address: str | None  # Криптоадрес для перевода
    amount: str | None  # Сумма
    hash: str | None  # Хеш тразакции в блокчейне
    created_at: str | None  # Дата создания
    status: int | None  # Статус операции 0 - неуспешна, 1 - успешна
    type: int | None  # Тип тразакции 0 - блокчейн, 1 - p2p, 3 - ОТС
    commission: str | None  # Комиссия
    demo: bool | None  # Флаг демо транзакций
    payment_id: int | None  # ID оплаты (если это вывод, то всегда значение 1600)
    withdrawal_id: int | None  # ID выплаты (для оплат null)
    uuid: str | None  # Внешний код либо короткое описание withdrawal, convert


class CryptoItem(BaseModel):
    name: str  # Name of the cryptocurrency
    balance: float  # Balance amount for the cryptocurrency


class PayoutBalanceInfo(BaseModel):
    success: bool  # Indicates if the operation was successful
    crypto: List[CryptoItem] | Dict[str, CryptoItem] | None  # List of cryptocurrency balances
    p2p: List[CryptoItem] | Dict[str, CryptoItem] | None  # List of P2P wallet balances
    acquiring: List[CryptoItem] | Dict[str, CryptoItem] | None  # List of acquiring balances
    payout: List[CryptoItem] | Dict[str, CryptoItem] | None  # List of payout balances

