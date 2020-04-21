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
    <SelectListModal activator="#forestAdd" title="Foo" submitBtnText="Add" />
    <addition-button
      ref="addBtn"
      class="my-2"
      id="forestAdd"
      v-if="isUpdate"
      :content="addBtnContent"
    />
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

export default {
  name: "forest-list-container",

  mixins: [ContainerMixin],

  components: {
    ContentHeader,
    ForestInfoList,
    UpdateButton,
    AdditionButton,
    SelectListModal,
  },

  props: {
    forests: Array,
    displayAdditionBtn: Boolean,
  },
  data() {
    return {
      isUpdate: false,
    };
  },
};
</script>
