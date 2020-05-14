<template>
  <div class="ml-6 mb-6">
    <h4 class="mb-1">タグ情報</h4>
    <v-progress-linear
      height="2"
      indeterminate
      rounded
      v-if="isLoading"
    ></v-progress-linear>
    <div class="items">
      <v-card class="tag-card d-hover" flat @click="onClickCard">
        <div v-for="(key, index) in Object.keys(tags)" :key="index">
          <v-chip small class="ml-2" v-if="tags[key]">
            {{ key }}: {{ tags[key] }}
          </v-chip>
        </div>
      </v-card>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    tags: { type: Object },
    appName: { type: String, required: true },
    objectType: { type: String, required: true },
  },
  data() {
    return {
      settings: {},
      values: {},
      isLoading: false,
    };
  },
  async mounted() {
    this.isLoading = true;
    await Promise.all([this.getTagSettings(), this.getTagValues()]);
    this.isLoading = false;
  },
  methods: {
    async getTagSettings() {
      const tagSettings = await this.$rest.get(
        `/tags/settings/${this.appName}/${this.objectType}`,
      );
      if (tagSettings && tagSettings.results) {
        this.settings = tagSettings.results;
      }
    },
    async getTagValues() {
      const tags = await this.$rest.get(
        `/tags/${this.appName}/${this.objectType}`,
      );
      if (tags && tags.results) {
        this.values = tags.results;
      }
    },
    onClickCard() {
      //popup
    },
    async modifyTags() {},
  },
};
</script>
<style lang="scss">
.tag-card {
  margin-top: 12px;
  min-height: 60px;
  box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05);
  align-items: center;
  border-radius: 4px;
  padding: 8px;
  display: flex;
  width: 399px;
}
</style>
