import pytest
from fastapi import HTTPException, status
from app.utils.currency import convert_rates
from app.api.schemas import CurrencyConversion


class TestConvertRates:
    """Тесты для функции конвертации валют"""

    def test_convert_rates_single_currency(self):
        """Тест конвертации в одну конкретную валюту"""
        rates = {
            "EUR": {"value": 0.85},
            "GBP": {"value": 0.73},
            "JPY": {"value": 110.0}
        }
        
        result = convert_rates("USD", rates, amount=100, to_currency="EUR")
        
        assert len(result) == 1
        assert result[0].from_currency == "USD"
        assert result[0].to_currency == "EUR"
        assert result[0].rate == 0.85
        assert result[0].amount == 100
        assert result[0].converted_amount == 85.0

    def test_convert_rates_all_currencies(self):
        """Тест конвертации во все доступные валюты"""
        rates = {
            "EUR": {"value": 0.85},
            "GBP": {"value": 0.73},
            "JPY": {"value": 110.0}
        }
        
        result = convert_rates("USD", rates, amount=10)
        
        assert len(result) == 3
        
        # Проверяем EUR
        eur_result = next(r for r in result if r.to_currency == "EUR")
        assert eur_result.converted_amount == 8.5
        
        # Проверяем GBP
        gbp_result = next(r for r in result if r.to_currency == "GBP")
        assert gbp_result.converted_amount == 7.3
        
        # Проверяем JPY
        jpy_result = next(r for r in result if r.to_currency == "JPY")
        assert jpy_result.converted_amount == 1100.0

    def test_convert_rates_currency_not_found(self):
        """Тест ошибки при запросе несуществующей валюты"""
        rates = {
            "EUR": {"value": 0.85},
            "GBP": {"value": 0.73}
        }
        
        with pytest.raises(HTTPException) as exc_info:
            convert_rates("USD", rates, amount=100, to_currency="RUB")
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Валюта RUB не найдена" in str(exc_info.value.detail)

    def test_convert_rates_zero_amount(self):
        """Тест конвертации нулевой суммы"""
        rates = {"EUR": {"value": 0.85}}
        
        result = convert_rates("USD", rates, amount=0, to_currency="EUR")
        
        assert result[0].converted_amount == 0.0

    def test_convert_rates_negative_amount(self):
        """Тест конвертации отрицательной суммы"""
        rates = {"EUR": {"value": 0.85}}
        
        result = convert_rates("USD", rates, amount=-100, to_currency="EUR")
        
        assert result[0].converted_amount == -85.0

    def test_convert_rates_empty_rates(self):
        """Тест конвертации с пустым списком курсов"""
        rates = {}
        
        result = convert_rates("USD", rates, amount=100)
        
        assert len(result) == 0