<template>
  <v-row dense>
    <v-col v-for="(contact, index) in contacts" cols="6" :key="index">
      <customer-contact-card
        :card_id="contact.customer_id || contact.id"
        :contact="contact"
        :isOwner="isOwner"
        :isUpdate="isUpdate"
        :index="index"
        @deleteContact="$emit('deleteContact', contact, index)"
        @undoDeleteContact="$emit('undoDeleteContact', contact, index)"
        :added="contact.added"
        :deleted="contact.deleted"
        :showRelationshipSelect="showRelationshipSelect"
        @click="(card_id, indx) => isUpdate && $emit('selected', card_id, indx)"
        :selectedId="selectingId"
      />
    </v-col>
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
    showRelationshipSelect: { type: Boolean, default: true },
    selectingId: String,
  },
};
</script>
