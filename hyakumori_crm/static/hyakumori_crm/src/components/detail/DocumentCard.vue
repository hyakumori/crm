<template>
  <v-card class="document-card d-hover" outlined flat>
    <v-icon class="document-card__icon" size="16">mdi-paperclip</v-icon>
    <span class="document-card__file-name">{{ fileName }}</span>
    <v-spacer></v-spacer>
    <v-btn
      class="align-self-center ma-3"
      v-if="isUpdating"
      icon
      @click="onDelete"
    >
      <v-icon size="24">mdi-close</v-icon>
    </v-btn>
    <v-btn class="align-self-center ma-3" v-else icon @click="onDownload">
      <a class="download" :href="downloadUrl" download target="_blank"></a>
      <v-icon size="24">mdi-download</v-icon>
    </v-btn>
  </v-card>
</template>

<script>
export default {
  name: "document-card",

  props: {
    fileName: String,
    isUpdating: Boolean,
    deleteClick: Function,
    downloadClick: Function,
    downloadUrl: String,
  },

  methods: {
    onDelete() {
      this.deleteClick();
    },

    onDownload() {
      this.downloadClick();
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../../styles/variables";

.document-card {
  display: flex;
  height: 48px;

  &__icon {
    margin-left: 11px;
    align-self: center;
    @include round-icon(32px);
  }

  &__file-name {
    margin-left: 14px;
    color: #444444;
    font-size: 14px;
    align-self: center;
  }
}
</style>
