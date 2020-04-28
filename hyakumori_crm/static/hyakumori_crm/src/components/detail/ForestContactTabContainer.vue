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
    :saveDisabled="saveDisabled"
    :save="handleSave"
    :saving="saving"
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
        @customerSelected="
          card_id =>
            selectingCustomerId == card_id
              ? (selectingCustomerId = null)
              : (selectingCustomerId = card_id)
        "
        :selectingCustomerId="selectingCustomerId"
        @toggleDefault="handleToggleDefault"
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
            @click="
              (cId, inx) => {
                modalSelectingCustomerId = cId;
                modalSelectingCustomerIndex = inx;
              }
            "
            v-for="(item, indx) in customersForAdding.results || []"
            :key="item.id"
            :card_id="item.id"
            :contact="item"
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
    customers: Array,
    customersContacts: Array,
    permissions: Array,
    isLoading: Boolean,
    id: String,
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
      saving: false,
      selectingCustomerId: null,
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
    customerIdsToAdd() {
      return this.customersToAdd.map(f => f.id);
    },
    customerIdsToDelete() {
      return this.customersToDelete.map(f => f.id);
    },
    saveDisabled() {
      return (
        this.customerIdsToDelete.length === 0 &&
        this.customerIdsToAdd.length === 0
      );
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
        const newCustomers = [...this.customers];
        const c = newCustomers[index];
        c.deleted = true;
        this.$store.commit("forest/setCustomers", newCustomers);
        this.customersToDelete.push(c);
      }
    },
    handleUndoDelete(customer, index) {
      const newCustomers = [...this.customers];
      const c = newCustomers[index];
      delete c.deleted;
      this.$store.commit("forest/setCustomers", newCustomers);
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
    handleToggleDefault(val, customer_id) {
      this.$store.dispatch("forest/toggleDefaultCustomer", {
        id: this.id,
        customer_id,
        val,
      });
    },
  },
  watch: {
    async showSelect(val) {
      if (val && !this.customersForAdding.next) {
        await this.loadInitCustomersForAdding();
      }
    },
    isEditing(val) {
      if (!val) {
        this.customersToAdd.length > 0 && (this.customersToAdd = []);
        const newCustomers = [...this.customers];
        for (let c of newCustomers) {
          delete c.deleted;
        }
        this.$store.commit("forest/setCustomers", newCustomers);
        this.customersToDelete.length > 0 && (this.customersToDelete = []);
      }
    },
  },
};
</script>
