<template>
  <div class="update-btn">
    <v-btn
      color="primary"
      :disabled="saveDisabled"
      elevation="0"
      class="mr-2"
      @click.stop="save"
      >{{ $t("buttons.save") }}</v-btn
    >
    <v-btn class="update-btn__cancel" text @click="onCancel">{{
      $t("buttons.cancel")
    }}</v-btn>
  </div>
</template>

<script>
export default {
  name: "update-button",

  props: {
    save: Function,
    cancel: Function,
    saveDisabled: Boolean,
  },

  methods: {
    onCancel() {
      if (this.cancel) {
        this.cancel();
      }
    },

    onSave() {
      if (this.save) {
        this.save();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.update-btn {
  display: flex;
  font-weight: bold;

  &__cancel {
    color: #999999;
  }
}
</style>
