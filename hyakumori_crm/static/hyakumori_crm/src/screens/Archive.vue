<template>
  <main-section #section>
    <search-card :onSearch="() => {}" />
  </main-section>
</template>

<script>
import SearchCard from "../components/SearchCard";
import MainSection from "../components/MainSection";

export default {
  name: "archive",

  components: {
    SearchCard,
    MainSection,
  },
};
</script>
