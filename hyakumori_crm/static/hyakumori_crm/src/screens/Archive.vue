<template>
  <main-section class="archives">
    <template #top>
      <page-header>
        <template #bottom-right>
          <outline-round-btn
            :content="$t('buttons.add_archive')"
            :icon="$t('icon.add')"
            @click="$router.push({ name: 'archive-new' })"
          />
        </template>
      </page-header>
    </template>
    <template #section class="archives">
      <search-card :onSearch="fetchArchives" :search-criteria="headers" />
      <data-list
        :auto-headers="false"
        :data="data"
        :headers="headers"
        :is-loading="isLoading"
        :showSelect="true"
        :tableRowIcon="pageIcon"
        @rowData="rowData"
        class="archives__data-section"
        iconRowValue="id"
      />
    </template>
  </main-section>
</template>

<script>
import SearchCard from "../components/SearchCard";
import MainSection from "../components/MainSection";
import DataList from "../components/DataList";
import ScreenMixin from "./ScreenMixin";
import archive_header from "../assets/dump/archive_header.json";
import PageHeader from "../components/PageHeader";
import OutlineRoundBtn from "../components/OutlineRoundBtn";
import { commonDatetimeFormat } from "../helpers/datetime";

export default {
  name: "archive",

  mixins: [ScreenMixin],

  components: {
    SearchCard,
    MainSection,
    DataList,
    PageHeader,
    OutlineRoundBtn,
  },

  mounted() {
    this.fetchArchives();
  },

  data() {
    return {
      pageIcon: this.$t("icon.archive_icon"),
      pageHeader: this.$t("page_header.archive_detail"),
      tableRowIcon: this.$t("icon.archive_icon"),
      data: [],
      isLoading: true,
    };
  },

  methods: {
    async fetchArchives() {
      const data = await this.$rest.get("/archives").then(res => res.results);
      this.data = data.map(data => {
        this.isLoading = false;
        return {
          id: data.id,
          archive_date: commonDatetimeFormat(data.archive_date),
          title: data.title,
          content: data.content,
          author: data.author.full_name,
          their_participants: "",
          our_participants: "",
          associated_forest: "",
        };
      });
    },

    rowData(val) {
      this.$router.push(`/archives/${val}`);
    },
  },

  computed: {
    headers() {
      return archive_header;
    },
  },
};
</script>

<style lang="scss" scoped>
.archives {
  &__data-section {
    margin-left: 29px;
  }
}
</style>
