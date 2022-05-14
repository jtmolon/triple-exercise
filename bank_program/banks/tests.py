import pytest

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from banks import models as bank_models
from general import models as general_models
from programs import models as program_models
from transactions import models as transaction_models

pytestmark = pytest.mark.django_db


@pytest.fixture
def rest_client() -> APIClient:
    client = APIClient()
    return client


def _create_countries_and_currencies():
    euro = general_models.Currency.objects.create(code="EUR", name="Euro")
    pound = general_models.Currency.objects.create(code="GBP", name="Pound Sterling")
    spain = general_models.Country.objects.create(code="ES", name="Spain", currency=euro)
    uk = general_models.Country.objects.create(code="GB", name="United Kingdom", currency=pound)


def test_bank_program_eligibility(rest_client):
    _create_countries_and_currencies()
    # Create bank
    bank_name = "bank 1"
    url = reverse("banks-list")
    data = {
        "name": bank_name,
        "countries": [general_models.Country.objects.get(code="ES").id],
    }

    assert not bank_models.Bank.objects.filter(name=bank_name).exists()
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["name"] == bank_name
    bank = bank_models.Bank.objects.get(name=bank_name)

    # Create program
    program_name = "program 1"
    url = reverse("programs-list")
    data = {
        "name": program_name,
        "currency": general_models.Currency.objects.get(code="EUR").id,
        "return_percentage": "10.50",
    }
    assert not program_models.Program.objects.filter(name=program_name).exists()
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["name"] == data["name"]
    program = program_models.Program.objects.get(name=program_name)

    # Create program eligibility
    url = reverse("programs-eligibility-list")
    data = dict(
        program=program.id,
        country=general_models.Country.objects.get(code="ES").id,
        bank=bank_name,
    )
    assert not program_models.ProgramEligibility.objects.filter(**data).exists()
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["program"] == program.id

    # Check eligibility
    url = reverse("transactions-list")
    data = {
        "country": general_models.Country.objects.get(code="ES").id,
        "currency": general_models.Currency.objects.get(code="EUR").id,
        "program": program.id,
        "bank": bank.id,
    }
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["is_eligible"] is True

    # Check eligibility - not applicable in country
    data = {
        "country": general_models.Country.objects.get(code="GB").id,
        "currency": general_models.Currency.objects.get(code="EUR").id,
        "program": program.id,
        "bank": bank.id,
    }
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["is_eligible"] is False

    # Check eligibility - not applicable in currency
    data = {
        "country": general_models.Country.objects.get(code="ES").id,
        "currency": general_models.Currency.objects.get(code="GBP").id,
        "program": program.id,
        "bank": bank.id,
    }
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["is_eligible"] is False

    # Check eligibility - not applicable in program
    program2 = program_models.Program.objects.create(
        name="program 2",
        currency=general_models.Currency.objects.get(code="EUR"),
        return_percentage=1.50,
    )
    data = {
        "country": general_models.Country.objects.get(code="ES").id,
        "currency": general_models.Currency.objects.get(code="EUR").id,
        "program": program2.id,
        "bank": bank.id,
    }
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["is_eligible"] is False

    # Check eligibility - not applicable in bank
    bank2 = bank_models.Bank.objects.create(
        name="bank 2",
    )
    bank2.countries.set([general_models.Country.objects.get(code="ES")])
    bank2.save()
    data = {
        "country": general_models.Country.objects.get(code="ES").id,
        "currency": general_models.Currency.objects.get(code="EUR").id,
        "program": program.id,
        "bank": bank2.id,
    }
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["is_eligible"] is False

    # Check eligibility - bank doesn't operate in country
    data = {
        "country": general_models.Country.objects.get(code="GB").id,
        "currency": general_models.Currency.objects.get(code="EUR").id,
        "program": program.id,
        "bank": bank.id,
    }
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["is_eligible"] is False

    # Check eligibility - not country currency
    bank3 = bank_models.Bank.objects.create(
        name="bank 3",
    )
    bank3.countries.set([
        general_models.Country.objects.get(code="ES"),
        general_models.Country.objects.get(code="GB"),
    ])
    bank3.save()
    data = {
        "country": general_models.Country.objects.get(code="ES").id,
        "currency": general_models.Currency.objects.get(code="GBP").id,
        "program": program.id,
        "bank": bank3.id,
    }
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["is_eligible"] is False


    # Check eligibility - correct country and currency
    program3 = program_models.Program.objects.create(
        name="program 3",
        currency=general_models.Currency.objects.get(code="GBP"),
        return_percentage=1.50,
    )
    program_models.ProgramEligibility.objects.create(
        program=program3,
        bank=bank3.name,
        country=general_models.Country.objects.get(code="GB"),
    )
    data = {
        "country": general_models.Country.objects.get(code="GB").id,
        "currency": general_models.Currency.objects.get(code="GBP").id,
        "program": program3.id,
        "bank": bank3.id,
    }
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["is_eligible"] is True

    # make sure it works internally without using the API
    transaction = transaction_models.Transaction.objects.create(
        country=general_models.Country.objects.get(code="GB"),
        currency=general_models.Currency.objects.get(code="GBP"),
        program=program3,
        bank=bank3,
    )
    assert transaction.is_eligible is True

    transaction2 = transaction_models.Transaction.objects.create(
        country=general_models.Country.objects.get(code="GB"),
        currency=general_models.Currency.objects.get(code="EUR"),
        program=program3,
        bank=bank3,
    )
    assert transaction2.is_eligible is False

    # updates work as well
    transaction2.currency = general_models.Currency.objects.get(code="GBP")
    transaction2.save()
    assert transaction2.is_eligible is True

    # test bank signal updating transactions
    bank3.countries.set([
        general_models.Country.objects.get(code="ES"),
    ])
    bank3.save()
    transaction.refresh_from_db()
    transaction2.refresh_from_db()
    assert transaction.is_eligible is False
    assert transaction2.is_eligible is False
