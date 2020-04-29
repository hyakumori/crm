<template>
  <div>
    <content-header
      :content="headerContent"
      :editBtnContent="editBtnContent"
      :loading="loading"
      @toggleEdit="val => (isUpdate = val)"
      :display-addition-btn="isDetail"
    />
    <archive-basic-info
      class="mt-6"
      :isUpdate="isUpdate"
      :isDetail="isDetail"
      :info="info"
    >
      <template v-if="!isDetail" v-slot:create-btn="props">
        <v-btn
          color="primary"
          :disabled="props.invalid"
          :loading="createLoading"
          @click="submit(props.info)"
        >
          {{ $t("buttons.continue") }}
        </v-btn>
      </template>
    </archive-basic-info>
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
import { archiveDatetimeFormat } from "../../helpers/datetime";

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
      loading: false,
      createLoading: false,
      info: {},
    };
  },

  mounted() {
    if (this.isDetail && !this.info.author) {
      this.fetchBasicInfo();
    }
  },

  methods: {
    dataMapping(basicInfo) {
      this.info = {
        id: basicInfo.id,
        archive_date: archiveDatetimeFormat(basicInfo.archive_date),
        location: basicInfo.location,
        future_action: basicInfo.future_action,
        author: basicInfo.author.full_name,
        content: basicInfo.content,
        title: basicInfo.title,
      };
    },

    async fetchBasicInfo() {
      this.loading = true;
      const basicInfo = await this.$rest
        .get(`archives/${this.id}`)
        .then(res => res.data)
        .catch(() => []);
      if (basicInfo) {
        this.loading = false;
        this.dataMapping(basicInfo);
      }
    },

    async submit(data) {
      this.createLoading = true;
      const newData = await this.$rest
        .post("/archives", data)
        .then(res => res)
        .catch();
      if (newData) {
        this.dataMapping(newData);
        this.createLoading = false;
        await this.$router.push(`/archives/${newData.id}`);
      }
    },
  },
};
</script>
