<template>
  <v-row class="px-7 pt-2">
    <v-col cols="3">
      <search-card
        :searchCriteria="getSearchCriteria"
        @onSearch="onSearch"
        @unableDelete="unableDelErr"
        @conditionOutOfBounds="conditionOutOfBoundsErr"
      />
    </v-col>

    <v-col cols="9">
      <table-action />

      <data-list
        class="mt-4"
        mode="forest"
        v-on:rowData="rowData"
        :headers="getHeaders"
        :data="getData"
        :showSelect="true"
        :negotiationCols="['status']"
        :isLoading="isLoading"
        :serverItemsLength="getTotalForests"
      ></data-list>
    </v-col>

    <snack-bar
      color="error"
      :isShow="isShowErr"
      :msg="errMsg"
      :timeout="sbTimeout"
      @dismiss="onDismissSb"
    />
  </v-row>
</template>

<script>
import DataList from "../components/DataList";
import SearchCard from "../components/SearchCard";
import TableAction from "../components/TableAction";
import headers from "../assets/dump/table_header_forest.json";
import GetForestList from "../graphql/GetForestList.gql";
import SnackBar from "../components/SnackBar";
import ScreenMixin from "./ScreenMixin";

export default {
  name: "forest",

  mixins: [ScreenMixin],

  components: {
    DataList,
    SearchCard,
    TableAction,
    SnackBar,
  },

  data() {
    return {
      pageIcon: this.$t("icon.forest_icon"),
      pageHeader: this.$t("page_header.forest_list"),
      searchCriteria: [],
      isShowErr: false,
      errMsg: null,
      sbTimeout: 5000,
    };
  },

  apollo: {
    forestsInfo: {
      query: GetForestList,
      update: data => data.list_forests,
    },
  },

  methods: {
    rowData() {
      // console.log(val);
    },

    onSearch(err, data) {
      if (err) {
        this.isShowErr = true;
        this.errMsg = this.$t("search.duplicate_criteria_msg");
      } else {
        // Handling search data
      }
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
  },

  computed: {
    getHeaders() {
      return headers;
    },

    isLoading() {
      return this.$apollo.queries.forestsInfo.loading;
    },

    getData() {
      if (this.forestsInfo) {
        return this.forestsInfo.forests.map(element => {
          return {
            id: element.id,
            address: element.geo_data.address,
            ground: "",
            acreage: element.basic_info.acreage,
            status: element.basic_info.status,
            ownerName: `${element.owner.profile.first_name} ${element.owner.profile.last_name}`,
            customerId: element.customer.id,
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
  },
};
</script>
