<template>
  <main-section>
    <template #left>
      <search-card />
    </template>
    <template #content>
      <data-list class="ml-7" />
    </template>
  </main-section>
</template>

<script>
import SearchCard from "../components/SearchCard";
import DataList from "../components/DataList";
import MainSection from "../components/MainSection";

export default {
  name: "archive",

  components: {
    MainSection,
    SearchCard,
    DataList,
  },
};
</script>
