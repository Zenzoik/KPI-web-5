from django import forms

from .models import FuelItem, FuelType, IssueRecord


class FuelTypeForm(forms.ModelForm):
    class Meta:
        model = FuelType
        fields = ["name", "description"]
        labels = {
            "name": "Назва",
            "description": "Опис",
        }


class FuelItemForm(forms.ModelForm):
    class Meta:
        model = FuelItem
        fields = [
            "name",
            "supplier",
            "fuel_type",
            "quantity_liters",
            "unit_price",
            "description",
        ]
        labels = {
            "name": "Найменування",
            "supplier": "Постачальник",
            "fuel_type": "Тип ПММ",
            "quantity_liters": "Залишок, л",
            "unit_price": "Ціна за літр",
            "description": "Опис",
        }

    def clean_unit_price(self):
        price = self.cleaned_data["unit_price"]
        if price < 0:
            raise forms.ValidationError("Ціна не може бути від'ємною.")
        return price


class IssueRecordForm(forms.ModelForm):
    issued_at = forms.DateTimeField(
        label="Дата операції",
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    class Meta:
        model = IssueRecord
        fields = ["fuel_item", "amount_liters", "destination", "issued_at"]
        labels = {
            "fuel_item": "ПММ",
            "amount_liters": "Обсяг, л",
            "destination": "Куди видано",
            "issued_at": "Дата операції",
        }

    def clean_amount_liters(self):
        amount = self.cleaned_data["amount_liters"]
        if amount <= 0:
            raise forms.ValidationError("Обсяг має бути більшим за 0.")
        return amount
