<template>
  <div>
    <content-header
      class="mb-4"
      :content="headerContent"
      :editBtnContent="editBtnContent"
      :loading="loading"
      @toggleEdit="handleEdit"
    />

    <forest-info-list
      :forests="relatedForests"
      :isUpdate="isUpdate"
      @deleteForest="deleteForest"
      @undoDeleteForest="handleUndoDelete"
    />
    <template v-if="isUpdate">
      <addition-button
        class="my-2"
        :content="addBtnContent"
        :click="onAdditionClick.bind(this)"
      />
      <update-button
        :cancel="cancel.bind(this)"
        :save="save.bind(this)"
        :saveDisabled="addedForestIds.length === 0"
        :saving="addRelatedForestLoading"
      />
    </template>
    <select-list-modal
      :shown="shown"
      :loading="fetchAllForestLoading"
      :submitBtnText="$t('buttons.add')"
      :handleSubmitClick="submitRelatedForest.bind(this)"
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
          :selectedId="selectingForestId"
          @selected="
            (fId, fIndex) => {
              selectingForestId = fId;
              selectingForestIndex = fIndex;
            }
          "
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
import { cloneDeep, pullAllWith } from "lodash";

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
      immutableRelatedForest: [],
      loading: false,
      fetchAllForestLoading: false,
      allForests: [],
      immutableAllForest: [],
      next: null,
      selectingForestId: null,
      selectingForestIndex: null,
      addRelatedForestLoading: false,
      forestsToDelete: [],
    };
  },

  mounted() {
    this.fetchRelatedForests();
  },

  methods: {
    handleEdit(val) {
      this.isUpdate = val;
      this.immutableRelatedForest = cloneDeep(this.relatedForests);
    },

    cancel() {
      this.isUpdate = false;
      this.relatedForests = this.immutableRelatedForest;
      this.allForests = this.immutableAllForest;
    },

    save() {
      if (this.relatedForests.length === 0) {
        this.isUpdate = false;
      } else {
        this.addRelatedForestLoading = true;
        const relatedIds = this.addedForestIds;
        const addRequest = { ids: relatedIds };
        // const delRequest = { ids: this.forestsToDelete };
        // this.$rest.delete(`/archives/${this.id}/forests`, {delRequest}).then();
        console.log(this.addedForestIds)
        this.$rest
          .post(`/archives/${this.id}/forests`, addRequest)
          .then(res => {
            this.relatedForests = res.data;
            this.addRelatedForestLoading = false;
            this.isUpdate = false;
          });
      }
    },

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
      this.fetchAllForestLoading = true;
      const response = await this.$rest
        .get(next || "/forests/minimal")
        .then(res => res)
        .catch();
      if (response) {
        this.fetchAllForestLoading = false;
        const filteredForests = this.filterDuplicateForests(
          response.results,
          this.relatedForests,
        );
        this.allForests.push(...filteredForests);
        this.immutableAllForest.push(...filteredForests);
        this.next = response.next;
      }
    },

    filterDuplicateForests(forests1, forests2) {
      return pullAllWith(forests1, forests2, (f1, f2) => f1.id === f2.id);
    },

    handleLoadMore() {
      this.fetchAllForests(this.next);
    },

    submitRelatedForest() {
      if (this.selectingForestId && this.selectingForestIndex) {
        const selectedForest = this.allForests[this.selectingForestIndex];
        selectedForest.added = true;
        this.relatedForests.push(selectedForest);
        this.allForests.splice(this.selectingForestIndex, 1);
        this.selectingForestId = null;
        this.selectingForestIndex = null;
      } else {
        this.allForests[0].added = true;
        this.relatedForests.push(this.allForests[0]);
        this.allForests.splice(0, 1);
      }
    },

    deleteForest(forest, index) {
      if (forest.added) {
        this.relatedForests.splice(index, 1);
      } else {
        this.$set(forest, "deleted", true);
        this.forestsToDelete.push(forest.id);
      }
    },

    handleUndoDelete(forest, index) {
      this.$set(forest, "deleted", false);
      this.forestsToDelete.splice(index, 1);
    },
  },

  computed: {
    addedForestIds() {
      return this.relatedForests
          .filter(forest => forest.added)
          .map(forest => forest.id);
    },
  },
};
</script>
