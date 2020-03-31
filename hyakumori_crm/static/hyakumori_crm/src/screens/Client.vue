<template>
  <v-row class="px-7 pt-2">
    <v-col cols="2">
      <search-card />
    </v-col>

    <v-col cols="10">
      <data-list />
    </v-col>
  </v-row>
</template>

<script>
import SearchCard from "../components/SearchCard";
import DataList from "../components/DataList";

export default {
  name: "client",

  components: {
    SearchCard,
    DataList
  }
};
</script>
