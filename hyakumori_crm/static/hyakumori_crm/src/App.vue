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
$background-color: #F5F5F5;
$content-width: 1400px;

html {
  background-color: $background-color;
  overflow: auto !important;
}

#app {
  height: 100%;
  background-color: $background-color;
  margin-left: auto;
  margin-right: auto;
}

.main-content {
  width: $content-width;
  margin-left: auto;
  margin-right: auto;
}
</style>
