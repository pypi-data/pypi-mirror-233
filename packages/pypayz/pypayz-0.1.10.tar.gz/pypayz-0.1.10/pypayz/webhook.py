from pypayz.utils import calculate_sign


class Webhook:
    def __init__(self, data: dict):
        self.data = data

    def get_uuid(self):
        return self.data['uuid']

    def get_amount(self):
        return float(self.data['amount'])

    def get_currency(self):
        return self.data['currency']

    def get_status(self):
        return self.data['status']

    def get_commission(self):
        return float(self.data['commission'])

    def get_product(self):
        return self.data['product']

    def get_client(self):
        return self.data['client']

    def is_success(self):
        return self.data['status'] == 'success'

    def verify_payment(self, secret_key):
        data = self.data.copy()
        del data['sign']
        signature = calculate_sign(secret_key, data)
        return signature == self.data['sign']
