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
        :customers="customers"
        :customerContacts="customerContacts"
        :isEditing="isEditing"
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
              `${item.name_kanji.last_name} ${item.name_kanji.first_name}`
            "
            :address="item.address.sector"
            :email="item.email"
            :forestCount="item.forest_count"
            :phone="item.telephone"
            :cellphone="item.mobilephone"
            :isOwner="true"
            :showAction="false"
            :index="indx"
            :selectedId="modalSelectingCustomertId"
            flat
            mode="search"
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

export default {
  name: "forest-contact-tab-container",

  mixins: [ContainerMixin],

  components: {
    SectionContainerWrapper,
    ContactTab,
    SelectListModal,
  },

  props: {
    headerContent: String,
    toggleEditBtnContent: String,
    addBtnContent: String,
    editBtnContent: String,
    customers: Array,
    customerContacts: Array,
    permissions: Array,
    isLoading: Boolean,
  },
  data() {
    return {
      isEditing: false,
      customersForAddingLoading: false,
      showSelect: false,
      customersForAdding: {},
    };
  },
  created() {
    this.debounceLoadInitCustomersForAdding = () => {};
  },
  methods: {
    handleAdd() {},
    handleLoadMore() {},
  },
};
</script>
