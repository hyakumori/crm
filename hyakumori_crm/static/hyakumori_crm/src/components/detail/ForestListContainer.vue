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
    <forest-info-list class="mt-4" :forests="forests" :isUpdate="isUpdate" />
    <addition-button
      ref="addBtn"
      class="my-2"
      v-if="isUpdate"
      :content="addBtnContent"
      :click="() => (showSelect = true)"
    />
    <SelectListModal :shown.sync="showSelect" submitBtnText="Add">
      <template #list>
        <ForestInfoCard v-for="item in forests" :key="item.id" />
      </template>
    </SelectListModal>
    <update-button v-if="isUpdate" :cancel="cancel.bind(this)" />
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
    // forests: Array,
    displayAdditionBtn: Boolean,
  },
  data() {
    return {
      isUpdate: false,
      showSelect: false,
      forests: [
        {
          id: "1uqyewuqw",
          address: "foo",
          cadastral: {
            subsector: "ha",
            sector: "ha",
            municipality: "ha",
            prefecture: "ha",
          },
        },
        {
          id: "1uqyewuqw-1",
          address: "foo",
          cadastral: {
            subsector: "ha",
            sector: "ha",
            municipality: "ha",
            prefecture: "ha",
          },
        },
        {
          id: "1uqyewuqw-2",
          address: "foo",
          cadastral: {
            subsector: "ha",
            sector: "ha",
            municipality: "ha",
            prefecture: "ha",
          },
        },
      ],
    };
  },
};
</script>
