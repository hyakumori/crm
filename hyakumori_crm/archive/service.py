
from hyakumori_crm.crm.models import Archive, ArchiveCustomer, ArchiveForest, ArchiveCustomerContact, Attachment, CustomerContact, Customer


class ArchiveService:

    def __init__(self, archive_detail=None):
        self.instance = archive_detail

    def create_archive(self,validated_data):

        archive_model = Archive()

        archive_model.consult_date = validated_data['consult_date']
        archive_model.location = validated_data['location']
        archive_model.attributes = validated_data['attributes']
        archive_model.discuss_content = validated_data['discuss_content']
        archive_model.future_action = validated_data['future_action']

        file_upload_list = validated_data['file_upload_list']
        for file_upload in file_upload_list:
            attachment_model = Attachment()
            attachment_model.content_object = archive_model
            attachment_model.attachment_file = file_upload_list[file_upload]
            attachment_model.creator = validated_data['creator']
            archive_model.attachment_list.add(attachment_model, bulk=False)

        archive_model.creator = validated_data['creator']
        archive_model.save()

        if validated_data['customer_id_set'] :
            for customer_id in validated_data['customer_id_set']:
                archivecustomer = ArchiveCustomer(archive=archive_model, customer_id=customer_id)
                archive_model.archivecustomer_set.add(archivecustomer, bulk=False)

        if validated_data['forest_id_set']:
            for forest_id in validated_data['forest_id_set']:
                    archiveforest = ArchiveForest(archive=archive_model, forest_id=forest_id)
                    archive_model.archiveforest_set.add(archiveforest, bulk=False)


        archive_model.save()

        return archive_model

    def update(self, validated_data):
        """ archive add customer list """
        customer_id_list = validated_data.get('customer_id_add_list')
        if customer_id_list:
            for customer_id in customer_id_list:
                if not ArchiveCustomer.objects.filter(archive_id=self.instance.id, customer_id=customer_id):
                    archivecustomer_new = ArchiveCustomer(archive_id=self.instance.id, customer_id=customer_id)
                    self.instance.archivecustomer_set.add(archivecustomer_new, bulk=False)

        """ archive delete customer """
        customers_delete = validated_data.get('customer_id_del_list')
        if customers_delete:
            for customer_id in customers_delete:
                ArchiveCustomer.objects.filter(archive_id=self.instance.id, customer_id=customer_id).delete()

        """ archive add forest list """
        forest_id_list = validated_data.get('forest_id_add_list')
        if forest_id_list:
            for forest_id in forest_id_list:
                if not ArchiveForest.objects.filter(archive_id=self.instance.id, forest_id=forest_id):
                    archiveforest_new = ArchiveForest(archive_id=self.instance.id, forest_id=forest_id)
                    self.instance.archiveforest_set.add(archiveforest_new, bulk=False)

        """ archive delete forest """
        forests_delete = validated_data.get('forest_id_del_list')
        if forests_delete:
            for forest_id in forests_delete:
                ArchiveForest.objects.filter(archive_id=self.instance.id, forest_id=forest_id).delete()

        self.instance.save()
        return self.instance

    def delete_archive(self):
        pass

    def get_contact_list_can_add(self, customer_id):

        archivecustomer_choiced = self.instance.archivecustomer_set.filter(customer_id=customer_id).get()
        customer_choiced = archivecustomer_choiced.customer
        contactcustomer_list = customer_choiced.customercontact_set.all()

        contact_can_add = []
        if contactcustomer_list:
            for contactcustomer in contactcustomer_list:
                archivecustomercontact = archivecustomer_choiced.archivecustomercontact_set.filter(customercontact_id=contactcustomer.id)
                if not archivecustomercontact:
                    contact_can_add.append(contactcustomer.contact)
            return contact_can_add
        else:
            return None

    def get_contacts_added_for_archive_customer(self, customer_id):
        archivecustomer_choiced = self.instance.archivecustomer_set.filter(customer_id = customer_id).get()
        customer_choiced = archivecustomer_choiced.customer
        contactcustomer_list = customer_choiced.customercontact_set.all()
        contacts_added = []
        if contactcustomer_list:
            for contactcustomer in contactcustomer_list:
                archivecustomercontact = archivecustomer_choiced.archivecustomercontact_set.filter(customercontact_id=contactcustomer.id)
                if archivecustomercontact:
                    contacts_added.append(contactcustomer.contact)
            return contacts_added
        else:
            return None

    def add_contact_to_archive_customer(self, customer_id, contact_id_list):
        archivecustomer_choiced = self.instance.archivecustomer_set.filter(customer_id=customer_id).get()
        customer_choiced = archivecustomer_choiced.customer
        for id in contact_id_list:

            contactcustomer_add = customer_choiced.customercontact_set.filter(customer_id=customer_id, contact_id=contact_id_list[id]).get()
            archivecustomercontact_add = ArchiveCustomerContact(archivecustomer=archivecustomer_choiced, customercontact=contactcustomer_add)
            archivecustomer_choiced.archivecustomercontact_set.add(archivecustomercontact_add, bulk=False)

        self.instance.save()
        return self.instance

    def delete_contact_for_archive_customer(self, customer_id, contact_id_list):
        archivecustomer_choiced = self.instance.archivecustomer_set.filter(customer_id=customer_id).get()
        customer_choiced = archivecustomer_choiced.customer

        for id in contact_id_list:
            contactcustomer_del = customer_choiced.customercontact_set.filter(customer_id=customer_id,contact_id=contact_id_list[id]).get()
            archivecustomer_choiced.archivecustomercontact_set.filter(customercontact_id=contactcustomer_del.id).delete()
        self.instance.save()
        return self.instance


