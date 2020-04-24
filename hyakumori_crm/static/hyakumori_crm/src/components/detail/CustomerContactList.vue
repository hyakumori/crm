<template>
  <v-row dense>
    <template v-for="(contact, index) in contacts">
      <v-col cols="6" :key="index">
        <customer-contact-card
          :card_id="contact.id"
          :fullname="getFullname(contact)"
          :address="contact.address.sector"
          :email="contact.email"
          :forestsCount="contact.forests_count"
          :phone="contact.telephone"
          :cellphone="contact.mobilephone"
          :isOwner="contact.is_basic"
          :isUpdate="isUpdate"
          :index="index"
          @deleteContact="$emit('deleteContact', contact)"
          @undoDeleteContact="$emit('undoDeleteContact', contact)"
          :added="contact.added"
          :deleted="contact.deleted"
        />
      </v-col>
    </template>
  </v-row>
</template>

<script>
import CustomerContactCard from "./CustomerContactCard";

export default {
  name: "customer-contact-list",

  components: {
    CustomerContactCard,
  },

  props: {
    contacts: Array,
    isUpdate: Boolean,
    isOwner: Boolean,
  },

  methods: {
    getFullname(contact) {
      if (contact.name_kanji) {
        return `${contact.name_kanji.last_name} ${contact.name_kanji.first_name}`;
      } else {
        return "";
      }
    },
  },
};
</script>
