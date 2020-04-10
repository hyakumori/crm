<template>
  <v-app id="app">
    <page-header />
    <router-view class="main-content d-flex pa-7"></router-view>
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

.main-content {
  width: $content-width;
  margin-left: auto;
  margin-right: auto;
}
</style>
