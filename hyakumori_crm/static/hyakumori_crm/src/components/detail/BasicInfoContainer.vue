<template>
  <div>
    <content-header
      :content="headerContent"
      :editBtnContent="editBtnContent"
      :loading="isLoading"
      :update="isUpdate"
      @update="val => (isUpdate = val)"
    />
    <div class="my-4">
      <basic-info
        :infos="info"
        :isUpdate="isUpdate"
        :isSave="isSave"
        @updateInfo="updateData"
      />
      <update-button
        class="mb-12"
        v-if="isUpdate"
        :cancel="cancel.bind(this)"
      />
    </div>
  </div>
</template>

<script>
import BasicInfo from "./BasicInfo";
import ContentHeader from "./ContentHeader";
import UpdateButton from "./UpdateButton";
import ContainerMixin from "./ContainerMixin";
import { updateBasicInfo } from "../../api/forest";
import { zipObjectDeep } from "lodash";

export default {
  name: "basic-info-container",

  mixins: [ContainerMixin],

  components: {
    ContentHeader,
    BasicInfo,
    UpdateButton,
  },

  props: {
    id: String,
    info: Array,
  },

  data() {
    return {
      isUpdate: false,
      isSave: false,
    };
  },

  methods: {
    save() {
      this.isSave = true;
    },

    updateData(updateInfo) {
      const key = updateInfo.map(info => info.attr);
      const val = updateInfo.map(info => info.value);
      const info = zipObjectDeep(key, val);
      updateBasicInfo(this.id, info);
    },
  },
};
</script>
