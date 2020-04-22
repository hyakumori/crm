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
    };
  },
  computed: {
    tempForests() {
      return [
        ...this.forests.filter(f => !this.forestIdsToDelete.includes(f.id)),
        ...this.forestsToAdd,
      ];
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
      this.forestsToAdd.push(forestItem);
      this.selectingForestIndex = null;
      this.selectingForestId = null;
    },
    handleDelete(forest) {
      this.forestsToDelete.push(forest);
    },
    async handleSave() {
      console.log("hey");
      try {
        await this.$rest.put(`/customers/${this.id}/forests`, {
          added: this.forestIdsToAdd,
          deleted: this.forestIdsToDelete,
        });
      } catch (error) {
        console.log(error);
      }
    },
  },
  watch: {
    async showSelect(val) {
      if (val) {
        this.loadForests = true;
        this.forestitems = await this.$rest.get("/forests");
        this.loadForests = false;
      }
    },
    isUpdate(val) {
      if (!val) {
        this.forestsToAdd = [];
        this.forestsToDelete = [];
      }
    },
  },
};
</script>
