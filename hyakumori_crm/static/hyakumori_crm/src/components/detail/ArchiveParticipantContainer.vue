<template>
  <div>
    <content-header
      class="mb-4"
      :content="headerContent"
      :editBtnContent="editBtnContent"
      :loading="isLoading"
      @toggleEdit="val => (isUpdate = val)"
    />
    <customer-contact-list :contacts="participants" :isUpdate="isUpdate" />
    <addition-button
      ref="addBtn"
      class="my-2"
      v-if="isUpdate"
      :content="addBtnContent"
      :click="() => (showSelect = true)"
    />
    <select-list-modal
      :loading="loadContacts"
      :shown.sync="showSelect"
      :submitBtnText="$t('buttons.add')"
      submitBtnIcon="mdi-plus"
      :handleSubmitClick="handleAdd"
      @needToLoad="handleLoadMore"
      @search="debounceLoadInitContactsForAdding"
    >
      <template #list>
        <customer-contact-card
          @click="
            (cId, inx) => {
              modalSelectingContactId = cId;
              modalSelectingContactIndex = inx;
            }
          "
          v-for="(item, indx) in participantsForAdding"
          :key="item.id"
          :card_id="item.id"
          :contact="item"
          :showAction="false"
          :index="indx"
          :selectedId="modalSelectingContactId"
          flat
          mode="search"
          :showRelationshipSelect="false"
        />
      </template>
    </select-list-modal>
    <update-button
      v-if="isUpdate"
      :cancel="() => (isUpdate = !isUpdate)"
      :save="handleSave"
      :saving="saving"
      :saveDisabled="saveDisabled"
    />
  </div>
</template>

<script>
import ContentHeader from "./ContentHeader";
import ContainerMixin from "./ContainerMixin";
import UpdateButton from "./UpdateButton";
import CustomerContactList from "./CustomerContactList";
import CustomerContactCard from "./CustomerContactCard";
import AdditionButton from "../AdditionButton";
import SelectListModal from "../SelectListModal";
import { debounce } from "lodash";

export default {
  name: "archive-participant-container",

  mixins: [ContainerMixin],

  components: {
    ContentHeader,
    UpdateButton,
    AdditionButton,
    SelectListModal,
    CustomerContactList,
    CustomerContactCard,
  },
  props: {
    participants: { type: Array, default: () => [] },
  },
  created() {
    this.debounceLoadInitContactsForAdding = debounce(
      this.loadInitContacts,
      500,
    );
  },
  data() {
    return {
      isUpdate: false,
      loadContacts: false,
      contactsForAdding: {},
      saving: false,
      modalSelectingContactId: null,
      modalSelectingContactInde: null,
      showSelect: false,
    };
  },
  computed: {
    saveDisabled() {
      return true;
    },
    participantsForAdding() {
      return this.contactsForAdding.results || [];
    },
  },
  methods: {
    handleSave() {},
    handleAdd() {},
    async handleLoadMore() {
      if (!this.contactsForAdding.next && this.loadContacts) return;
      this.loadContacts = true;
      const resp = await this.$rest.get(this.contactsForAdding.next);
      this.contactsForAdding = {
        next: resp.next,
        previous: resp.previous,
        results: [...this.contactsForAdding.results, ...resp.results],
      };
      this.loadContacts = false;
    },
    async loadInitContacts(keyword) {
      this.loadContacts = true;
      this.contactsForAdding = await this.$rest.get("/contacts", {
        params: {
          search: keyword || "",
        },
      });
      this.loadContacts = false;
    },
  },
  watch: {
    async showSelect(val) {
      if (val && !this.contactsForAdding.next) {
        await this.loadInitContacts();
      }
    },
  },
};
</script>
