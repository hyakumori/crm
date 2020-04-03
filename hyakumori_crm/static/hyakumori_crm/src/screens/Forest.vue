<template>
  <v-row class="px-7 pt-2">
    <v-col cols="3">
      <search-card />
    </v-col>

    <v-col cols="9">
      <table-action />

      <data-list
        class="mt-4"
        mode="client"
        v-on:rowData="rowData"
        :headers="getHeaders"
        :data="getData"
        :showSelect="true"
        :negotiationCols="['status']"
      ></data-list>
    </v-col>
  </v-row>
</template>

<script>
import DataList from "../components/DataList";
import SearchCard from "../components/SearchCard";
import TableAction from "../components/TableAction";
import headers from "../assets/dump/table_header_forest.json";
import GetForestList from "../graphql/GetForestList.gql";
import gql from "graphql-tag";

export default {
  name: "forest",

  components: {
    DataList,
    SearchCard,
    TableAction
  },

  apollo: {
    forestsInfo: {
      query: gql`
        ${GetForestList}
      `,
      update: data => data.list_forests.forests
    }
  },

  methods: {
    rowData() {
      // console.log(val);
    }
  },

  computed: {
    getHeaders() {
      return headers;
    },

    getData() {
      if (this.forestsInfo) {
        return this.forestsInfo.map(e => {
          return {
            id: e.id,
            address: e.geo_data.address,
            ground: "",
            acreage: e.basic_info.acreage,
            status: e.basic_info.status,
            ownerName: `${e.owner.profile.first_name} ${e.owner.profile.last_name}`,
            customerId: e.customer.id
          };
        });
      } else {
        return this.forestsInfo;
      }
    }
  }
};
</script>
