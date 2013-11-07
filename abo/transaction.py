class ABOTransaction:
    def __init__(self, account_number, amount, variable_symbol=None, constant_symbol=None, specific_symbol=None, message=None):
        self._account_number = account_number
        self._amount = int(round(amount * 100))
        self._variable_symbol = int(variable_symbol) if variable_symbol is not None else 0
        self._constant_symbol = int(constant_symbol) if constant_symbol is not None else 0
        self._specific_symbol = int(specific_symbol) if specific_symbol is not None else 0
        self._message = message[:35] if message is not None else ""

    def get_amount(self):
        return self._amount

    def render(self):
        return '{prefix:0>6}-{account:0>10} {amount:015d} {variable_symbol:010d} {bank:0>4}{constant_symbol:04d} {specific_symbol:010d} AV:{message}\r\n'.format(
            prefix=self._account_number['prefix'],
            account=self._account_number['number'],
            amount=self._amount,
            variable_symbol=self._variable_symbol,
            bank=self._account_number['bank'],
            constant_symbol=self._constant_symbol,
            specific_symbol=self._specific_symbol,
            message=self._message
        )