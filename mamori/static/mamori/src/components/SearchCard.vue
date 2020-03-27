<template>
  <v-card class="search-section ml-xs-3 ml-sm-3 ml-md-4 ml-lg-9 ml-xl-9">
    <h5>検索条件</h5>
    <div class="mb-2 mt-2 d-flex align-center">
      <h5 class="font-weight-regular mb-0" style="color: #999999">
        項目を選択
      </h5>
      <v-icon>mdi-chevron-down</v-icon>
    </div>
    <v-text-field clearable placeholder="パスワード" outlined></v-text-field>
    <div class="d-block">
      <v-icon>mdi-plus</v-icon>
      <span class="ml-1 caption">検索条件を追加</span>
    </div>
  </v-card>
</template>

<script>
export default {
  name: "search-card"
};
</script>

<style lang="scss">
.search-section {
  padding: 18px;
  min-height: 628px;
  border-radius: 4px;
}

.v-input {
  & .v-text-field__details {
    margin-bottom: 0 !important;
    min-height: 0;

    & .v-messages {
      min-height: 0;
    }
  }
}

.d-block {
  color: #12c7a6 !important;

  & .v-icon {
    color: #12c7a6 !important;
  }
}
</style>
