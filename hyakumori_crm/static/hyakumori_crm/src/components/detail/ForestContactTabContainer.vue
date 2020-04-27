<template>
  <SectionContainerWrapper
    :headerContent="headerContent"
    :toggleEditBtnContent="toggleEditBtnContent"
    :addBtnContent="addBtnContent"
    :isLoading="isLoading"
    :permissions="permissions"
    :isEditing="isEditing"
    @toggleEdit="val => (isEditing = val)"
    :cancelEdit="
      () => {
        isEditing = false;
      }
    "
    :addBtnClickHandler="
      () => {
        showSelect = true;
      }
    "
  >
    <template>
      <contact-tab
        class="mt-5"
        :class="{ 'mb-10': !isEditing }"
        :customers="tempCustomers"
        :customersContacts="customersContacts"
        :isEditing="isEditing"
        @deleteCustomer="handleDelete"
        @undoDeleteCustomer="handleUndoDelete"
      />
      <SelectListModal
        :loading="customersForAddingLoading"
        :shown.sync="showSelect"
        :submitBtnText="$t('buttons.add')"
        submitBtnIcon="mdi-plus"
        :handleSubmitClick="handleAdd"
        @needToLoad="handleLoadMore"
        @search="debounceLoadInitCustomersForAdding"
      >
        <template #list>
          <CustomerContactCard
            @selected="
              (cId, inx) => {
                modalSelectingCustomerId = cId;
                modalSelectingCustomerIndex = inx;
              }
            "
            v-for="(item, indx) in customersForAdding.results || []"
            :key="item.id"
            :card_id="item.id"
            :fullname="
              `${item.self_contact.name_kanji.last_name} ${item.self_contact.name_kanji.first_name}`
            "
            :address="item.self_contact.address.sector"
            :email="item.self_contact.email"
            :forestsCount="item.forests_count"
            :phone="item.self_contact.telephone"
            :cellphone="item.self_contact.mobilephone"
            :showAction="false"
            :index="indx"
            :selectedId="modalSelectingCustomerId"
            flat
            mode="search"
            :showRelationshipSelect="false"
          />
        </template>
      </SelectListModal>
    </template>
  </SectionContainerWrapper>
</template>

<script>
import SectionContainerWrapper from "../SectionContainerWrapper";
import ContactTab from "./ContactTab";
import ContainerMixin from "./ContainerMixin";
import SelectListModal from "../SelectListModal";
import CustomerContactCard from "./CustomerContactCard";

import { debounce, reject } from "lodash";

export default {
  name: "forest-contact-tab-container",

  mixins: [ContainerMixin],

  components: {
    SectionContainerWrapper,
    ContactTab,
    SelectListModal,
    CustomerContactCard,
  },

  props: {
    headerContent: String,
    toggleEditBtnContent: String,
    addBtnContent: String,
    editBtnContent: String,
    customers: Array,
    customersContacts: Array,
    permissions: Array,
    isLoading: Boolean,
  },
  data() {
    return {
      isEditing: false,
      customersForAddingLoading: false,
      showSelect: false,
      customersForAdding: {},
      customersToAdd: [],
      customersToDelete: [],
      modalSelectingCustomerId: null,
      modalSelectingCustomerIndex: null,
    };
  },
  created() {
    this.debounceLoadInitCustomersForAdding = debounce(
      this.loadInitCustomersForAdding,
      500,
    );
  },
  computed: {
    tempCustomers() {
      return [...this.customers, ...this.customersToAdd];
    },
    customerIdsMap() {
      return Object.fromEntries(this.tempCustomers.map(c => [c.id, true]));
    },
  },
  methods: {
    handleAdd() {
      const c = this.customersForAdding.results.splice(
        this.modalSelectingCustomerIndex,
        1,
      )[0];
      c.added = true;
      this.customersToAdd.push(c);
      this.modalSelectingCustomerIndex = null;
      this.modalSelectingCustomerId = null;
    },
    handleDelete(customer, index) {
      if (customer.added) {
        delete customer.added;
        this.customersToAdd = reject(this.customersToAdd, { id: customer.id });
      } else {
        this.$set(customer, "deleted", true);
        this.customersToDelete.push(customer);
      }
    },
    handleUndoDelete(customer, index) {
      this.$set(customer, "deleted", undefined);
      this.customersToDelete = reject(this.customersToDelete, {
        id: customer.id,
      });
    },
    async handleSave() {
      try {
        this.saving = true;
        await this.$rest.put(`/forests/${this.id}/customers/update`, {
          added: this.customerIdsToAdd,
          deleted: this.customerIdsToDelete,
        });
        this.$emit("saved");
        this.saving = false;
        this.customersToDelete = [];
        this.customersToAdd = [];
      } catch (error) {
        this.saving = false;
      }
    },
    async handleLoadMore() {
      if (!this.customersForAdding.next) return;
      this.customersForAddingLoading = true;
      const resp = await this.$rest.get(this.customersForAdding.next);
      this.customersForAdding = {
        next: resp.next,
        previous: resp.previous,
        results: [
          ...this.customersForAdding.results,
          ...reject(resp.results, c => this.customerIdsMap[c.id]),
        ],
      };
      this.customersForAddingLoading = false;
    },
    async loadInitCustomersForAdding(keyword) {
      this.customersForAddingLoading = true;
      const resp = await this.$rest.get("/customers", {
        params: {
          search: keyword || "",
        },
      });
      this.customersForAdding = {
        next: resp.next,
        previous: resp.previous,
        results: reject(resp.results, c => this.customerIdsMap[c.id]),
      };
      this.customersForAddingLoading = false;
    },
  },
  watch: {
    async showSelect(val) {
      if (val && !this.customersForAdding.next) {
        await this.loadInitCustomersForAdding();
      }
    },
  },
};
</script>
