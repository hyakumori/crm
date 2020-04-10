import os
import pickle
from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import TestCase
from dotenv import load_dotenv

from data_import.config import setup_django, setup_path
from data_import.services.customer import CustomerService

load_dotenv(Path(__file__).parent.joinpath(".env"))

EXCEL_FILE_PATH = Path(os.getenv("ORIGINAL_XLSX_PATH"))
MASTER_DATA_PATH = EXCEL_FILE_PATH.parent.joinpath("master-data.pickle")

data = pickle.load(open(MASTER_DATA_PATH, "rb"))

setup_path()
setup_django()


class SimpleLoadTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.dev", password="TeSt.PassWord!"
        )

    def test_print_data(self):
        # print(data["forest"]["1-005-99"].owner.json(ensure_ascii=False, indent=2))
        # print(data["customer"]["230"].json(ensure_ascii=False, indent=2))
        pass

    def test_insert_record(self):

        customer = CustomerService.create_customer(data["customer"]["230"], self.user)

        assert customer.id is not None
        assert customer.customercontact_set.count() == 6

        CustomerService.delete_customer_by_id(customer.id)
        customer.refresh_from_db()

        assert customer.is_deleted is True
