<template>
  <v-app id="app">
    <page-header />
    <router-view></router-view>
  </v-app>
</template>

<script>
import PageHeader from "./components/PageHeader";

export default {
  name: "App",

  components: {
    PageHeader,
  },
};
</script>

<style lang="scss">
@import "./styles/variables";

html {
  background-color: $background-color;
  overflow: auto !important;
}

#app {
  height: 100%;
  background-color: $background-color;
}
</style>
