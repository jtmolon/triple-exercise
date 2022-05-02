import pytest

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from banks import models as bank_models
from programs import models as program_models

pytestmark = pytest.mark.django_db


@pytest.fixture
def rest_client() -> APIClient:
    client = APIClient()
    return client


def test_bank_program_eligibility(rest_client):
    # Create bank
    bank_name = "bank 1"
    url = reverse("banks-list")
    data = {
        "name": bank_name,
        "countries": ["ES"],
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
        "currency": "EUR",
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
        country="ES",
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
        "country": "ES",
        "currency": "EUR",
        "program": program_name,
        "bank": bank_name,
    }
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["is_eligible"] is True

    # Check eligibility - not applicable in country
    url = reverse("transactions-list")
    data = {
        "country": "PT",
        "currency": "EUR",
        "program": program_name,
        "bank": bank_name,
    }
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["is_eligible"] is False

    # Check eligibility - not applicable in currency
    url = reverse("transactions-list")
    data = {
        "country": "ES",
        "currency": "USD",
        "program": program_name,
        "bank": bank_name,
    }
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["is_eligible"] is False

    # Check eligibility - not applicable in program
    url = reverse("transactions-list")
    data = {
        "country": "ES",
        "currency": "EUR",
        "program": "program 2",
        "bank": bank_name,
    }
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["is_eligible"] is False

    # Check eligibility - not applicable in bank
    url = reverse("transactions-list")
    data = {
        "country": "ES",
        "currency": "EUR",
        "program": program_name,
        "bank": "bank 2",
    }
    response = rest_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    result = response.data
    assert result["is_eligible"] is False
