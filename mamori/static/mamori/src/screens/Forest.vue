<template>
  <v-row class="pt-4 main-section">
    <v-col cols="3">
      <search-card />
    </v-col>
    <v-col cols="9">
      <div
        class="list-header d-flex align-center mr-xs-3 mr-sm-3 mr-md-4 mr-lg-9 mr-xl-9"
      >
        <p class="ml-4 mb-0 font-weight-bold caption">４件を選択済み</p>
        <p class="ml-12 mb-0 caption">アクションを選択</p>
        <v-icon>mdi-chevron-down</v-icon>
      </div>
      <data-list
        class="mt-4 mr-xs-3 mr-sm-3 mr-md-4 mr-lg-9 mr-xl-9"
        :showSelect="false"
        v-on:rowData="rowData"
      ></data-list>
    </v-col>
  </v-row>
</template>

<script>
import DataList from "../components/DataList";
import SearchCard from "../components/SearchCard";

export default {
  name: "forest",
  components: {
    DataList,
    SearchCard
  },
  data() {
    return {
      headers: [
        {
          text: "id"
        },
        {
          text: "name"
        },
        {
          text: "age"
        },
        {
          text: "options"
        }
      ],
      datas: [
        {
          id: 1,
          name: "bao",
          age: 22,
          options: "hello"
        }
      ]
    };
  },
  methods: {
    rowData(val) {
      console.log(val);
    }
  }
};
</script>

<style lang="scss">
.main-section {
  background-color: #dddddd;
}

.list-header {
  background: #f7eaa5;
  border-radius: 4px;
  height: 56px;

  & p {
    color: #825929;
  }

  & .v-icon {
    cursor: pointer;
  }
}
</style>
