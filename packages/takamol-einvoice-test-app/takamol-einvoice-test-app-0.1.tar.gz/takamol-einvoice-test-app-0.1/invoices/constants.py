SELLER_INFO = {
    "registration_name": "شركة تكامل لخدمات الأعمال",
    "CRN": "1010341361",
    "company_ID": "300892771510003",

}

SELLER_ADDRESS = {
    "street_name": "street",
    "building_number": "2654",
    "postal_zone": "13241",
    "city": ["Riyadh", "الرياض"],
    "additional_number": "7343"
}

INVOICE_TYPE_CODES_NAMES = {
    'STANDARD': '0100000',
    'SIMPLIFIED': '0200000'
}

INVOICE_TYPE_CODES = {
    'TAX': '388',
    'DEBIT': '383',
    'CREDIT': '381'
}
INVOICE_TITLE = {
    'STANDARD': {
        'TAX': {'en': 'Tax Invoice',
                'ar': 'فاتورة ضريبية'},
        'DEBIT': {'en': 'Debit Notice for Tax Invoice', 'ar': 'إشعار مدين للفاتورة الضريبية'},
        'CREDIT': {'en': 'Credit Notice for Tax Invoice',
                   'ar': 'إشعار دائن للفاتورة الضريبية'}
    },

    'SIMPLIFIED': {'TAX': {'en': 'Simplified Tax Invoice',
                           'ar': 'فاتورة ضريبية مبسطة'},
                   'DEBIT': {'en': 'Debit Notice for Simplified Tax Invoice',
                             'ar': 'إشعار مدين للفاتورة الضريبية المبسطة'},
                   'CREDIT': {'en': 'Credit Notice for Simplified Tax Invoice',
                              'ar': 'إشعار دائن للفاتورة الضريبية المبسطة'}
                   }
}
