<template>
  <div>
    <content-header
      class="mb-4"
      :content="headerContent"
      :editBtnContent="editBtnContent"
      :loading="loading"
      @toggleEdit="val => (isUpdate = val)"
    />

    <forest-info-list :forests="relatedForests" :isUpdate="isUpdate" />
    <template v-if="isUpdate">
      <addition-button
        class="my-2"
        :content="addBtnContent"
        :click="onAdditionClick.bind(this)"
      />
      <update-button :cancel="cancel.bind(this)" />
    </template>
    <select-list-modal
      :shown="shown"
      :loading="addRelatedForestLoading"
      :submitBtnText="$t('buttons.add')"
      submitBtnIcon="mdi-plus"
      @needToLoad="handleLoadMore"
      @update:shown="val => (shown = val)"
    >
      <template #list>
        <forest-info-card
          v-for="(item, index) in allForests"
          mode="search"
          :key="index"
          :index="index"
          :forest-id="item.internal_id"
          :card_id="item.id"
          :customerCount="item.customers_count"
          :address="getFullAddress(item)"
          :showAction="false"
          flat
        />
      </template>
    </select-list-modal>
  </div>
</template>

<script>
import ContentHeader from "./ContentHeader";
import ContainerMixin from "./ContainerMixin";
import ForestInfoList from "./ForestInfoList";
import UpdateButton from "./UpdateButton";
import AdditionButton from "../AdditionButton";
import SelectListModal from "../SelectListModal";
import ForestInfoCard from "./ForestInfoCard";

export default {
  name: "archive-related-forest-container",

  mixins: [ContainerMixin],

  components: {
    ForestInfoList,
    ContentHeader,
    UpdateButton,
    AdditionButton,
    SelectListModal,
    ForestInfoCard,
  },

  data() {
    return {
      id: this.$route.params.id,
      isUpdate: false,
      shown: false,
      relatedForests: [],
      loading: false,
      addRelatedForestLoading: false,
      allForests: [],
      next: null,
    };
  },

  mounted() {
    this.fetchRelatedForests();
  },

  methods: {
    onAdditionClick() {
      this.shown = true;
      if (this.allForests.length === 0) {
        this.fetchAllForests();
      }
    },

    getFullAddress(data) {
      if (!data.cadastral) {
        return "";
      } else {
        return `${data.cadastral.subsector} ${data.cadastral.sector} ${data.cadastral.municipality} ${data.cadastral.prefecture}`;
      }
    },

    async fetchRelatedForests() {
      this.loading = true;
      const response = await this.$rest
        .get(`/archives/${this.id}/forests`)
        .then(res => res)
        .catch();
      if (response) {
        this.relatedForests = response.data;
        this.loading = false;
      }
    },

    async fetchAllForests(next) {
      this.addRelatedForestLoading = true;
      const response = await this.$rest
        .get(next || "/forests/minimal")
        .then(res => res)
        .catch();
      if (response) {
        this.addRelatedForestLoading = false;
        this.allForests.push(...response.results);
        this.next = response.next;
      }
    },

    handleLoadMore() {
      console.log("load more");
      this.fetchAllForests(this.next);
    },
  },
};
</script>
