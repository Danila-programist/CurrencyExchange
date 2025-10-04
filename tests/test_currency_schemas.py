import pytest
from pydantic import ValidationError

from app.api.schemas import Currency, CurrencyConversion


class TestCurrencySchema:
    def test_currency_valid_data(self):
        currency_data = {
            "symbol": "$",
            "name": "US Dollar",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "USD",
            "name_plural": "US dollars",
            "type": "fiat",
            "countries": ["US", "EC", "SV", "MH", "FM", "PW", "TL", "ZW"],
        }

        currency = Currency(**currency_data)

        assert currency.symbol == "$"
        assert currency.name == "US Dollar"
        assert currency.code == "USD"
        assert len(currency.countries) == 8

    def test_currency_missing_required_field(self):
        currency_data = {
            "symbol": "$",
            "name": "US Dollar",
            # Отсутствует symbol_native
            "decimal_digits": 2,
            "rounding": 0,
            "code": "USD",
            "name_plural": "US dollars",
            "type": "fiat",
            "countries": ["US"],
        }

        with pytest.raises(ValidationError):
            Currency(**currency_data)

    def test_currency_invalid_type(self):
        currency_data = {
            "symbol": "$",
            "name": "US Dollar",
            "symbol_native": "$",
            "decimal_digits": "invalid",  # Должно быть int
            "rounding": 0,
            "code": "USD",
            "name_plural": "US dollars",
            "type": "fiat",
            "countries": ["US"],
        }

        with pytest.raises(ValidationError):
            Currency(**currency_data)

    def test_currency_empty_countries(self):
        currency_data = {
            "symbol": "₿",
            "name": "Bitcoin",
            "symbol_native": "₿",
            "decimal_digits": 8,
            "rounding": 0,
            "code": "BTC",
            "name_plural": "Bitcoins",
            "type": "crypto",
            "countries": [],
        }

        currency = Currency(**currency_data)
        assert currency.countries == []


class TestCurrencyConversionSchema:
    def test_currency_conversion_valid_data(self):
        conversion_data = {
            "from_currency": "USD",
            "to_currency": "EUR",
            "rate": 0.85,
            "amount": 100.0,
            "converted_amount": 85.0,
        }

        conversion = CurrencyConversion(**conversion_data)

        assert conversion.from_currency == "USD"
        assert conversion.to_currency == "EUR"
        assert conversion.rate == 0.85
        assert conversion.amount == 100.0
        assert conversion.converted_amount == 85.0

    def test_currency_conversion_missing_field(self):
        conversion_data = {
            "from_currency": "USD",
            "to_currency": "EUR",
            "rate": 0.85,
            "amount": 100.0,
            # Отсутствует converted_amount
        }

        with pytest.raises(ValidationError):
            CurrencyConversion(**conversion_data)

    def test_currency_conversion_negative_values(self):
        conversion_data = {
            "from_currency": "USD",
            "to_currency": "EUR",
            "rate": -0.85,  # Отрицательный курс
            "amount": -100.0,  # Отрицательная сумма
            "converted_amount": 85.0,
        }

        conversion = CurrencyConversion(**conversion_data)
        assert conversion.rate == -0.85
        assert conversion.amount == -100.0

    def test_currency_conversion_zero_values(self):
        conversion_data = {
            "from_currency": "USD",
            "to_currency": "EUR",
            "rate": 0.0,
            "amount": 0.0,
            "converted_amount": 0.0,
        }

        conversion = CurrencyConversion(**conversion_data)
        assert conversion.rate == 0.0
        assert conversion.amount == 0.0
        assert conversion.converted_amount == 0.0

    def test_currency_conversion_large_numbers(self):
        conversion_data = {
            "from_currency": "USD",
            "to_currency": "JPY",
            "rate": 110.0,
            "amount": 1000000.0,
            "converted_amount": 110000000.0,
        }

        conversion = CurrencyConversion(**conversion_data)
        assert conversion.amount == 1000000.0
        assert conversion.converted_amount == 110000000.0

    def test_currency_conversion_serialization(self):
        conversion = CurrencyConversion(
            from_currency="USD",
            to_currency="EUR",
            rate=0.85,
            amount=100.0,
            converted_amount=85.0,
        )

        data = conversion.model_dump()

        assert data["from_currency"] == "USD"
        assert data["to_currency"] == "EUR"
        assert data["rate"] == 0.85
        assert data["amount"] == 100.0
        assert data["converted_amount"] == 85.0
