from forex_python.converter import CurrencyRates ,CurrencyCodes ,RatesNotAvailableError


rates = CurrencyRates()
codes = CurrencyCodes()

def check_code(code):
    return codes.get_currency_name(code) is not None



def convert_with_symbol(code_from , code_to , amount):
    try:
        amt = f"{rates.convert(code_from, code_to, amount):.2f}"
    except RatesNotAvailableError:
        return None

    symbol = codes.get_symbol(code_to)
    return f"{symbol} {amt}"

