<template>
  <div>
    <slot name="top">
      <page-header></page-header>
    </slot>

    <v-container fluid class="app-width d-flex px-7 pt-5" v-if="!singleColumn">
      <slot name="section"></slot>
      <slot name="right"></slot>
    </v-container>

    <slot name="center"></slot>
  </div>
</template>

<script>
import PageHeader from "./PageHeader";

export default {
  name: "main-section",
  components: { PageHeader },
  props: {
    singleColumn: { type: Boolean, default: false },
  },
};
</script>

<style lang="scss" scoped>
@import "../styles/variables";

.app-width {
  width: $content-width;
  min-width: $content-width;
}
</style>
