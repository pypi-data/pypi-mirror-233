import random
import base64
from urllib.parse import urlencode, quote
from pypayz.schemas import PaymentModel
from pypayz.utils import calculate_sign


class Widget:
    PaymentModel = PaymentModel

    def __init__(self, merchant_id, secret_key, base_url: str = 'https://payz.team/widget/%d?data=%s'):
        self.merchant_id = merchant_id
        self.secret_key = secret_key
        self.base_url = base_url

    def create_payment(self, data: PaymentModel):
        data = {
            **data.dict(),
            **{
                'price': int(data.price * 100),
                'uuid': random.randint(10000, 99999) if data.uuid is None else data.uuid
            }
        }

        data['sign'] = calculate_sign(self.secret_key, data)
        data = urlencode(data, quote_via=quote)
        
        message_bytes = str(data).encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')

        return self.base_url % (self.merchant_id, base64_message)
