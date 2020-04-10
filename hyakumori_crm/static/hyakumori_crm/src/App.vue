<template>
  <v-app id="app" fullheight>
    <page-header />
    <router-view class="main-content d-flex px-7 pt-5"></router-view>
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
$background-color: #dddddd;

html {
  background-color: $background-color;
  overflow: auto !important;
}

#app {
  width: 1400px;
  height: 100%;
  background-color: $background-color;
  margin-left: auto;
  margin-right: auto;
}
</style>
