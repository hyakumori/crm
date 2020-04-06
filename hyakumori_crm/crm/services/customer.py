from uuid import UUID, uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from ..models.customer import Contact, Customer
from ..models.relations import CustomerContact
from ..schemas.customer import CustomerSchema


class CustomerService:
    @staticmethod
    def create_customer(customer: CustomerSchema, author: AbstractUser) -> Customer:
        _customer = Customer()
        _customer.internal_id = customer.internal_id
        _customer.name_kanji = customer.name_kanji.dict()
        _customer.name_kana = customer.name_kana.dict()
        _customer.address = customer.address.dict()
        _customer.banking = customer.banking.dict()
        _customer.basic_contact = customer.basic_contact.dict()
        _customer.tags = customer.tags
        _customer.editor = author
        _customer.author = author
        _customer.save()

        for contact in customer.contacts:
            _contact = Contact()
            _contact.internal_id = uuid4().hex
            _contact.contact_info = contact.dict()
            _contact.author = author
            _contact.editor = author
            _contact.save()

            _customer_contact = CustomerContact()
            _customer_contact.customer = _customer
            _customer_contact.contact = _contact
            _customer_contact.author = author
            _customer_contact.editor = author
            _customer_contact.save()

        return _customer

    @staticmethod
    def delete_customer_by_id(customer_id: UUID):
        customer = Customer.objects.get(pk=customer_id)
        customer.delete()

        for contact_link in customer.customercontact_set.all().iterator():
            contact_link.delete()
            contact_link.contact.delete()
