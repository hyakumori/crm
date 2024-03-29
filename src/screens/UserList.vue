<template>
  <main-section class="forest">
    <template #top>
      <page-header>
        <template #bottom-right>
          <outline-round-btn
            :icon="$t('icon.add')"
            :content="$t('buttons.add_user')"
            @click="showCreationForm = !showCreationForm"
          />
          <v-dialog v-model="showCreationForm" scrollable max-width="420">
            <create-user-form
              @success="onUserCreated"
              :show="showCreationForm"
            />
          </v-dialog>
        </template>
      </page-header>
    </template>

    <template slot="section">
      <v-content>
        <v-container grid-list-xs class="main-container">
          <data-list
            itemKey="id"
            :dense="false"
            :headers="getHeaders"
            :data="results"
            :showSelect="false"
            :isLoading="isLoading"
            :serverItemsLength="count"
            :tableRowIcon="tableRowIcon"
            :options.sync="options"
            @rowData="rowData"
            @selectedRow="selectedRow"
            :autoHeaders="false"
            :disable-sort="false"
            sort-by="is_active"
            :sort-desc="true"
          ></data-list>
        </v-container>
      </v-content>
    </template>
  </main-section>
</template>

<script>
import MainSection from "../components/MainSection";
import PageHeader from "../components/PageHeader";
import ScreenMixin from "./ScreenMixin";
import DataList from "../components/DataList";
import CreateUserForm from "../components/forms/CreateUserForm";
import OutlineRoundBtn from "../components/OutlineRoundBtn";
import { fromNow } from "../helpers/datetime";

export default {
  mixins: [ScreenMixin],
  components: {
    DataList,
    PageHeader,
    MainSection,
    CreateUserForm,
    OutlineRoundBtn
  },
  data() {
    return {
      pageIcon: this.$t("icon.user_icon"),
      pageHeader: this.$t("page_header.user_mgmt"),
      tableRowIcon: this.$t("icon.user_icon"),
      headers: [],
      next: null,
      previous: null,
      count: 0,
      results: [],
      isLoading: false,
      options: {},
      showCreationForm: false
    };
  },
  methods: {
    rowData(val) {
      this.$router.push(`users/${val}`);
    },

    selectedRow(val) {
      this.tableSelectedRow = val;
    },

    mapResults(results) {
      return results.map(item => ({
        ...item,
        roles: item.groups && item.groups.join(","),
        last_login_text: fromNow(item.last_login) || undefined,
        is_active:
          item.is_active === true
            ? this.$t("enums.user_status.active")
            : this.$t("enums.user_status.inactive")
      }));
    },

    async getData(perPage, page, sortBy = [], sortDesc = []) {
      this.isLoading = true;
      let response;
      if (
        sortDesc.length > 0 &&
        sortBy.length > 0 &&
        sortDesc.length == sortBy.length
      ) {
        response = await this.$rest.get(
          `/users?page_size=${perPage}&page=${page}&sort_by=${sortBy.join(
            ","
          )}&sort_desc=${sortDesc.join(",")}`
        );
      } else {
        response = await this.$rest.get(
          `/users?page_size=${perPage}&page=${page}`
        );
      }

      if (response) {
        this.results = this.mapResults(response.results);
        this.next = response.next;
        this.count = response.count;
        this.previous = response.previous;
        this.isLoading = false;
      }
    },

    async onUserCreated() {
      await this.getData(this.filter.preItemsPerPage, this.filter.page);
    }
  },
  async mounted() {
    this.$store.dispatch("setHeaderInfo", {
      title: this.$t("page_header.user_mgmt"),
      subtitle: ""
    });
  },

  watch: {
    options: {
      async handler(val, old) {
        if (Object.keys(old).length == 0) return;
        const { sortBy, sortDesc, page, itemsPerPage } = val;
        this.filter = {
          sortBy,
          sortDesc,
          page,
          itemsPerPage,
          preItemsPerPage: old.itemsPerPage || null
        };
        await this.getData(itemsPerPage, page, sortBy, sortDesc);
      }
    }
  },

  computed: {
    getHeaders() {
      return [
        {
          text: "",
          align: "center",
          value: "internal_id",
          sortable: false
        },
        {
          text: this.$t("user_management.tables.headers.username"),
          align: "center",
          value: "username",
          sortable: false
        },
        {
          text: this.$t("user_management.tables.headers.full_name"),
          align: "center",
          value: "full_name",
          sortable: false
        },
        {
          text: this.$t("user_management.tables.headers.roles"),
          align: "center",
          value: "roles",
          sortable: false
        },
        {
          text: this.$t("user_management.tables.headers.email"),
          align: "center",
          value: "email",
          sortable: false
        },
        {
          text: this.$t("user_management.tables.headers.status"),
          align: "center",
          value: "is_active",
          sortable: true
        },
        {
          text: this.$t("user_management.tables.headers.last_login"),
          align: "center",
          value: "last_login_text",
          sortable: false
        }
      ];
    }
  }
};
</script>

<style lang="scss" scoped>
.main-container {
  max-width: 974px;
  padding: 0;
}
</style>
