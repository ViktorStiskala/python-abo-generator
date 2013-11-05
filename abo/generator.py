# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# ABO banking format generator (Currently supports only "CSOB" compatible format)
#
# Thanks to Lukas Hurych for providing generator code
# Additional docs: http://www.fio.cz/docs/cz/struktura-abo.pdf, http://www.equabank.cz/files/doc/13-format-abo.pdf


import re
from datetime import datetime

from .transaction import ABOTransaction


class ABO:
    """
    ABO format generator.

    Transaction type can be set either to payment or collection.
    """

    TYPE_PAYMENT = 1501
    TYPE_COLLECTION = 1502

    def __init__(self, client_account_number, due_date, client_name='', client_number=0, interval_start=1, interval_end=999,
                 code=0, secret_code=0, transaction_type=TYPE_PAYMENT):
        self._content = None
        self._transactions = []
        self._account_number = self._parse_account_number(client_account_number)
        self._due_date = due_date
        self._client_name = re.sub(r'[^A-Z0-9]', r'', client_name.upper())
        self._client_number = client_number
        self._interval_start = interval_start
        self._interval_end = interval_end
        self._code = code
        self._secret_code = secret_code
        self._transaction_type = transaction_type

        if len(str(client_number)) > 10:
            raise ValueError('Length of the client number cannot be higher than 10 characters')

        if interval_start > 999 or interval_start < 1 or interval_end > 999 or interval_end < 1 or interval_end < interval_start:
            raise ValueError('Wrong interval specified')

    def _parse_account_number(self, account_number):
        m = re.match(r'^((?P<prefix>\d+)-)?(?P<number>\d+)/(?P<bank>\d{4})$', account_number)
        if not m:
            raise ValueError('Invalid account number: {}'.format(account_number))

        return m.groupdict(default='')

    def _create_abo_header(self):
        return 'UHL1{date_generated}{client_name: <20}{client_number:010d}{int_start:03d}{int_end:03d}{code:06d}{secret_code:06d}\r\n'.format(
            date_generated=datetime.now().strftime('%d%m%y'),
            client_name=self._client_name[:20],
            client_number=int(self._client_number),
            int_start=self._interval_start,
            int_end=self._interval_end,
            code=int(self._code),
            secret_code=int(self._secret_code)
        )

    def _create_accounting_file_header(self):
        # SSS set to 001, PPB set to 000
        return '1 {trn_type} 001000 {bank_code}\r\n'.format(
            trn_type=self._transaction_type,
            bank_code=self._account_number['bank']
        )

    def _create_group_header(self):
        total_amount = int(sum(trn.get_amount() for trn in self._transactions))

        if len(str(total_amount)) > 15:
            raise ValueError('Total amount too high for use in ABO format')

        return '2 {prefix:0<6}-{account:0<10} {total_amount:015d} {due_date}\r\n'.format(
            prefix=self._account_number['prefix'],
            account=self._account_number['number'],
            total_amount=total_amount,
            due_date=self._due_date.strftime('%d%m%y')
        )

    def _create_footer(self):
        return '3 +\r\n5 +\r\n'

    def _generate(self):
        """Generate content of the ABO file"""
        self._content = self._create_abo_header()
        self._content += self._create_accounting_file_header()
        self._content += self._create_group_header()

        for transaction in self._transactions:
            self._content += transaction.render()

        self._content += self._create_footer()

    def add_transaction(self, account_number, amount, variable_symbol, constant_symbol=None, specific_symbol=None, message=None):
        account_number = self._parse_account_number(account_number)
        transaction = ABOTransaction(account_number, amount, variable_symbol, constant_symbol, specific_symbol, message)

        self._transactions.append(transaction)

    def get_content(self):
        if self._content is None:
            self._generate()
        return self._content

    def save(self, file_handle):
        file_handle.write(self.get_content())
