<template>
  <v-container fluid class="app-width">
    <v-row class="app-width px-4">
      <v-col cols="3">
        <slot name="left"></slot>
      </v-col>
      <v-col cols="9">
        <slot name="content"></slot>
      </v-col>
      <v-col cols="3">
        <slot name="right"></slot>
      </v-col>
    </v-row>
    <slot name="addons"></slot>
  </v-container>
</template>

<style lang="scss" scoped>
@import "../styles/variables";

.app-width {
  width: $content-width;
}
</style>
