<template>
  <main-section class="forest">
    <template #top>
      <page-header>
        <template #bottom-right>
          <div>
            <outline-round-btn
              :content="$t('buttons.csv_upload')"
              :icon="$t('icon.add')"
              @click="uploadCsv"
              class="mr-2"
              v-show="false"
            />
            <v-menu nudge-bottom="4" offset-y>
              <template v-slot:activator="{ on }">
                <outline-round-btn
                  :content="$t('buttons.csv_download')"
                  :loading="downloadCsvLoading"
                  class="mr-2"
                  icon="mdi-download"
                  v-on="on"
                />
              </template>
              <v-list class="pa-0" dense>
                <v-list-item
                  @click="downloadSelectedRows"
                  v-if="tableSelectedRow && tableSelectedRow.length > 0"
                >
                  <v-list-item-title
                    >{{ $t("buttons.download_selected") }}
                  </v-list-item-title>
                </v-list-item>
                <v-list-item @click="downloadAllCsv">
                  <v-list-item-title
                    >{{ $t("buttons.download_all") }}
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>
        </template>
      </page-header>
    </template>

    <template #section>
      <search-card
        :onSearch="onSearch"
        :searchCriteria="filterFields"
        ref="filter"
      />

      <div class="ml-7 forest__data-section">
        <table-action
          :actions="actions"
          :selectedCount="tableSelectedRow.length"
          @selected-action="selectedAction"
          class="forest__data-section__table-action mb-4"
          v-if="tableSelectedRow.length > 0"
        />

        <data-list
          :autoHeaders="false"
          :data="getData"
          :headers="getHeaders"
          :isLoading="$apollo.queries.forestsInfo.loading"
          :options.sync="options"
          :serverItemsLength="getTotalForests"
          :showSelect="true"
          :tableRowIcon="tableRowIcon"
          @rowData="rowData"
          @selectedRow="selectedRow"
          itemKey="id"
          mode="forest"
        ></data-list>
      </div>

      <snack-bar
        :isShow="isShowErr"
        :msg="errMsg"
        :timeout="sbTimeout"
        @dismiss="onDismissSb"
        color="error"
      />

      <v-dialog
        v-model="showChangeTagDialog"
        max-width="700"
        transition
        @click:outside="showChangeTagDialog = false"
      >
        <ValidationObserver v-slot="{ invalid }">
          <v-card>
            <v-card-title class="display-0">
              {{ $t("action.change_tag_value") }}
            </v-card-title>
            <v-card-text class="pb-0">
              <v-row>
                <v-col cols="6">
                  <h4>タグを選択</h4>
                  <v-select
                    ref="tagList"
                    outlined
                    dense
                    height="45"
                    no-data-text="データなし"
                    :items="tagKeys"
                    @change="onSelectedTagChange"
                  />
                </v-col>
                <v-col cols="6">
                  <h4>タグバリュー</h4>
                  <text-input
                    v-model="newTagValue"
                    label="タグバリュー"
                    rules="required|max:255"
                  />
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions class="px-4">
              <v-btn text color="primary" @click="setDefaultTagData"
                >Cancel</v-btn
              >
              <v-spacer></v-spacer>
              <v-btn
                text
                color="primary"
                @click="updateSelectedTags"
                :disabled="invalid || !selectedTagUpdate"
                >OK</v-btn
              >
            </v-card-actions>
          </v-card>
        </ValidationObserver>
      </v-dialog>
    </template>
  </main-section>
</template>

<script>
import gql from "graphql-tag";
import DataList from "../components/DataList";
import SearchCard from "../components/SearchCard";
import TableAction from "../components/TableAction";
import GetForestList from "../graphql/GetForestList.gql";
import SnackBar from "../components/SnackBar";
import ScreenMixin from "./ScreenMixin";
import MainSection from "../components/MainSection";
import PageHeader from "../components/PageHeader";
import OutlineRoundBtn from "../components/OutlineRoundBtn";
import TextInput from "../components/forms/TextInput";
import { saveAs } from "file-saver";
import { flatten, get as _get } from "lodash";
import { ValidationObserver } from "vee-validate";

export default {
  name: "forest",

  mixins: [ScreenMixin],

  components: {
    DataList,
    SearchCard,
    TableAction,
    SnackBar,
    MainSection,
    PageHeader,
    OutlineRoundBtn,
    TextInput,
    ValidationObserver,
  },

  data() {
    return {
      actions: [
        {
          text: this.$t("action.contract_status_to_contracted"),
          value: 0,
        },
        {
          text: this.$t("action.contract_status_to_unsigned"),
          value: 1,
        },
        {
          text: this.$t("action.contract_status_to_expired"),
          value: 2,
        },
        {
          text: this.$t("action.change_tag_value"),
          value: 3,
        },
      ],
      pageIcon: this.$t("icon.forest_icon"),
      pageHeader: this.$t("page_header.forest_mgmt"),
      tableRowIcon: this.$t("icon.forest_icon"),
      searchCriteria: [],
      isShowErr: false,
      errMsg: null,
      sbTimeout: 5000,
      filter: {},
      options: {},
      tableSelectedRow: [],
      headers: [],
      downloadCsvLoading: false,
      showChangeTagDialog: false,
      tagKeys: [],
      selectedTagUpdate: null,
      newTagValue: null,
    };
  },

  apollo: {
    headers: {
      query: gql`
        query ForestTableHeaders {
          foresttable_headers {
            headers
          }
        }
      `,
      update(data) {
        return data.foresttable_headers.headers;
      },
    },
    forestsInfo: {
      query: GetForestList,
      update: data => data.list_forests,
      variables() {
        return {
          filter: this.filter,
        };
      },
      skip() {
        return !this.filter || this.headers.length === 0;
      },
    },
  },

  methods: {
    rowData(val) {
      this.$router.push(`forests/${val}`);
    },

    onDismissSb(val) {
      this.isShowErr = val;
    },

    unableDelErr(err) {
      if (err) {
        this.isShowErr = true;
        this.errMsg = this.$t("search.unable_to_remove_search_msg");
      }
    },

    conditionOutOfBoundsErr(err) {
      if (err) {
        this.isShowErr = true;
        this.errMsg = this.$t("search.condition_is_maximum");
      }
    },

    selectedRow(val) {
      this.tableSelectedRow = val;
    },

    onSearch() {
      this.filter = { ...this.filter, filters: this.requestFilters };
      this.$apollo.queries.forestsInfo.refetch();
    },

    uploadCsv() {
      // TODO: handle upload forest as csv
    },

    async downloadAllCsv() {
      try {
        this.downloadCsvLoading = true;
        let csvData = await this.$rest.get("/forests/download-csv");
        const blob = new Blob([csvData], { type: "text/csv;charset=UTF-8" });
        saveAs(blob, "all-forests.csv");
      } catch (e) {
      } finally {
        this.downloadCsvLoading = false;
      }
    },

    async downloadSelectedRows() {
      try {
        this.downloadCsvLoading = true;
        let csvData = await this.$rest.post(
          "/forests/download-csv",
          this.selectedRowIds,
        );
        const blob = new Blob([csvData], { type: "text/csv;charset=UTF-8" });
        saveAs(blob, "selected_forests.csv");
      } catch (e) {
      } finally {
        this.downloadCsvLoading = false;
      }
    },

    renderCustomers(data, nameType) {
      const list = _get(data, "attributes.customer_cache.list", {});
      const itemCount = Object.keys(list).length;
      if (itemCount > 0) {
        const firstKeyAsId = Object.keys(list)[0];
        let results = _get(
          list[firstKeyAsId],
          `name_${nameType}.last_name`,
          "",
        );

        const firstName = _get(
          list[firstKeyAsId],
          `name_${nameType}.first_name`,
          "",
        );

        if (firstName && firstName.length > 0) {
          results += " " + firstName;
        }

        if (itemCount > 1) {
          results +=
            " " +
            this.$t(`tables.another_item_human_${nameType}`, {
              count: itemCount - 1,
            });
        }
        return results;
      }
      return "";
    },

    setDefaultTagData() {
      this.newTagValue = null;
      this.$refs.tagList.internalValue = "";
      this.showChangeTagDialog = false;
    },

    async fetchSelectedForests() {
      try {
        const forests = await this.$rest.put(
          "/forests/ids",
          this.selectedRowIds,
        );
        const tags = forests.map(forest => forest.tags);
        tags.forEach(tag => this.tagKeys.push(Object.keys(tag)));
        this.tagKeys = [...new Set(flatten(this.tagKeys))];
        this.showChangeTagDialog = true;
      } catch (e) {
        this.showChangeTagDialog = false;
      } finally {
      }
    },

    async updateSelectedTags() {
      const params = {
        ids: this.selectedRowIds,
        key: this.selectedTagUpdate,
        value: this.newTagValue,
      };
      try {
        await this.$rest.put("/forests/tags", params);
      } catch (e) {
      } finally {
        this.setDefaultTagData();
        await this.$apollo.queries.forestsInfo.refetch();
      }
    },

    onSelectedTagChange(val) {
      this.selectedTagUpdate = val;
    },

    selectedAction(index) {
      switch (index) {
        case 0:
          console.log("0");
          break;
        case 1:
          console.log("1");
          break;
        case 2:
          console.log("2");
          break;
        case 3:
          this.fetchSelectedForests();
          break;
        default:
          return;
      }
    },
  },

  watch: {
    options: {
      handler(val, old) {
        const { sortBy, sortDesc, page, itemsPerPage } = val;
        this.filter = {
          sortBy,
          sortDesc,
          page,
          itemsPerPage,
          preItemsPerPage: old.itemsPerPage || null,
          filters: this.requestFilters,
        };
      },
      deep: true,
    },
  },

  computed: {
    getHeaders() {
      return this.headers;
    },

    getData() {
      if (this.forestsInfo) {
        return this.forestsInfo.forests.map(element => {
          const fCadastral = element.cadastral;
          const contract = element.contracts;
          const tags = element.tags;

          return {
            id: element.id,
            internal_id: element.internal_id,
            cadastral__prefecture: fCadastral.prefecture,
            cadastral__municipality: fCadastral.municipality,
            cadastral__sector: fCadastral.sector,
            cadastral__subsector: fCadastral.subsector,
            owner__name_kanji: this.renderCustomers(element, "kanji"),
            owner__name_kana: this.renderCustomers(element, "kana"),
            contracts__0__status: contract[0].status,
            contracts__0__start_date: contract[0].start_date,
            contracts__0__end_date: contract[0].end_date,
            contracts__1__status: contract[1].status,
            contracts__1__start_date: contract[1].start_date,
            contracts__1__end_date: contract[1].end_date,
            contracts__2__status: contract[2].status,
            contracts__2__start_date: contract[2].start_date,
            contracts__2__end_date: contract[2].end_date,
            tags: tags,
          };
        });
      } else {
        return this.forestsInfo;
      }
    },

    getTotalForests() {
      if (this.forestsInfo) {
        return this.forestsInfo.total;
      } else {
        return 0;
      }
    },

    getSearchCriteria() {
      return Array.from(this.getHeaders).map(header => header.text);
    },

    filterFields() {
      return this.headers
        .map(h => ({ text: h.text, value: h.filter_name }))
        .filter(f => f.value !== undefined);
    },

    selectedRowIds() {
      return (
        this.tableSelectedRow.length > 0 &&
        this.tableSelectedRow.map(row => row.id)
      );
    },
  },
};
</script>

<style lang="scss" scoped>
.forest {
  &__data-section {
    flex: 1;
    overflow: hidden;
  }
}
</style>
