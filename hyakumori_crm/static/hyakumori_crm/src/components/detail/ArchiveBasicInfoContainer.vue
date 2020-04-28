<template>
  <div>
    <content-header
      :content="headerContent"
      :editBtnContent="editBtnContent"
      :loading="isLoading"
      @toggleEdit="val => (isUpdate = val)"
      :display-addition-btn="isDetail"
    />
    <archive-basic-info
      class="mt-6"
      :isUpdate="isUpdate"
      :isDetail="isDetail"
      :info="info"
    />
    <slot name="create-btn"></slot>
    <update-button
      class="mb-12 mt-4"
      v-if="isUpdate"
      :cancel="cancel.bind(this)"
    />
  </div>
</template>

<script>
import ContentHeader from "./ContentHeader";
import ContainerMixin from "./ContainerMixin";
import ArchiveBasicInfo from "./ArchiveBasicInfo";
import UpdateButton from "./UpdateButton";

export default {
  name: "archive-basic-info-container",

  mixins: [ContainerMixin],

  components: {
    ContentHeader,
    ArchiveBasicInfo,
    UpdateButton,
  },

  props: {
    isDetail: {
      type: Boolean,
      default: true,
    },
    id: String,
  },

  data() {
    return {
      isUpdate: false,
      loading: true,
      info: {
        id: "",
        archive_date: "",
        location: "",
        future_response: "",
        author: "",
        content: "",
      },
    };
  },

  mounted() {
    if (this.isDetail) {
      this.fetchBasicInfo();
    }
  },

  methods: {
    async fetchBasicInfo() {
      const basicInfo = await this.$rest
        .get(`archives/${this.id}`)
        .then(res => res.data);
      if (basicInfo) {
        this.loading = false;
        this.info = {
          id: basicInfo.id,
          archive_date: basicInfo.archive_date,
          location: basicInfo.location,
          future_response: basicInfo.future_response,
          author: basicInfo.author.full_name,
          content: basicInfo.content,
        };
      }
    },
  },
};
</script>
