<template>
  <div>
    <content-header
      :content="headerContent"
      :editBtnContent="editBtnContent"
      :update="isUpdate"
      :loading="isLoading"
      :displayAdditionBtn="displayAdditionBtn"
      @update="val => (isUpdate = val)"
    />
    <forest-info-list
      class="mt-4"
      :forests="tempForests"
      :isUpdate="isUpdate"
      @deleteForest="handleDelete"
      @undoDeleteForest="handleUndoDelete"
    />
    <addition-button
      ref="addBtn"
      class="my-2"
      v-if="isUpdate"
      :content="addBtnContent"
      :click="() => (showSelect = true)"
    />
    <SelectListModal
      :loading="loadForests"
      :shown.sync="showSelect"
      submitBtnText="Add"
      submitBtnIcon="mdi-plus"
      :handleSubmitClick="handleAdd"
      @needToLoad="handleLoadMore"
    >
      <template #list>
        <ForestInfoCard
          @selected="
            (fId, inx) => {
              selectingForestId = fId;
              selectingForestIndex = inx;
            }
          "
          v-for="(item, indx) in forestitems.results || []"
          :key="item.id"
          :card_id="item.id"
          :forestId="item.internal_id"
          :customerCount="item.customers_count"
          :address="
            `${item.cadastral.subsector} ${item.cadastral.sector} ${item.cadastral.municipality} ${item.cadastral.prefecture}`
          "
          :showAction="false"
          :index="indx"
          flat
        />
      </template>
    </SelectListModal>
    <update-button
      v-if="isUpdate"
      :cancel="cancel"
      :save="handleSave"
      :saving="saving"
      :saveDisabled="saveDisabled"
    />
  </div>
</template>

<script>
import ContainerMixin from "./ContainerMixin";
import ContentHeader from "./ContentHeader";
import ForestInfoList from "./ForestInfoList";
import UpdateButton from "./UpdateButton";
import AdditionButton from "../AdditionButton";
import SelectListModal from "../SelectListModal";
import ForestInfoCard from "../detail/ForestInfoCard";
import { reject } from "lodash";

export default {
  name: "forest-list-container",

  mixins: [ContainerMixin],

  components: {
    ContentHeader,
    ForestInfoList,
    UpdateButton,
    AdditionButton,
    SelectListModal,
    ForestInfoCard,
  },

  props: {
    id: String,
    forests: Array,
    displayAdditionBtn: Boolean,
  },
  data() {
    return {
      isUpdate: false,
      showSelect: false,
      loadForests: false,
      forestitems: {},
      selectingForestId: null,
      forestsToAdd: [],
      forestsToDelete: [],
      selectingForestIndex: null,
      saving: false,
    };
  },
  computed: {
    tempForests() {
      return [...this.forests, ...this.forestsToAdd];
    },
    forestIdsMap() {
      return Object.fromEntries(this.tempForests.map(f => [f.id, true]));
    },
    forestIdsToAdd() {
      return this.forestsToAdd.map(f => f.id);
    },
    forestIdsToDelete() {
      return this.forestsToDelete.map(f => f.id);
    },
    saveDisabled() {
      return (
        this.forestIdsToDelete.length === 0 && this.forestIdsToAdd.length === 0
      );
    },
  },
  methods: {
    handleAdd() {
      const forestItem = this.forestitems.results.splice(
        this.selectingForestIndex,
        1,
      )[0];
      forestItem.added = true;
      this.forestsToAdd.push(forestItem);
      this.selectingForestIndex = null;
      this.selectingForestId = null;
    },
    handleDelete(forest) {
      if (forest.added) {
        delete forest.added;
        this.forestsToAdd = reject(this.forestsToAdd, { id: forest.id });
      } else {
        this.$set(forest, "deleted", true);
        this.forestsToDelete.push(forest);
      }
    },
    handleUndoDelete(forest) {
      this.$set(forest, "deleted", undefined);
      this.forestsToDelete = reject(this.forestsToDelete, { id: forest.id });
    },
    async handleSave() {
      try {
        this.saving = true;
        await this.$rest.put(`/customers/${this.id}/forests`, {
          added: this.forestIdsToAdd,
          deleted: this.forestIdsToDelete,
        });
        this.$emit("saved");
        this.saving = false;
        this.forestsToDelete = [];
        this.forestsToAdd = [];
      } catch (error) {}
    },
    async handleLoadMore() {
      this.loadForests = true;
      const resp = await this.$rest.get(this.forestitems.next);
      this.forestitems = {
        next: resp.next,
        previous: resp.previous,
        results: [
          ...this.forestitems.results,
          ...reject(resp.results, f => !!this.forestIdsMap[f.id]),
        ],
      };
      this.loadForests = false;
    },
  },
  watch: {
    async showSelect(val) {
      if (val && !this.forestitems.next) {
        this.loadForests = true;
        const resp = await this.$rest.get("/forests");
        this.forestitems = {
          next: resp.next,
          previous: resp.previous,
          results: reject(resp.results, f => !!this.forestIdsMap[f.id]),
        };
        this.loadForests = false;
      }
    },
    isUpdate(val) {
      if (!val) {
        this.forestsToAdd.length > 0 && (this.forestsToAdd = []);
        for (let forestToDelete of this.forestsToDelete) {
          this.$set(forestToDelete, "deleted", undefined);
        }
        this.forestsToDelete && (this.forestsToDelete = []);
      }
    },
  },
};
</script>
