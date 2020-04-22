<template>
  <v-dialog v-model="shown_" scrollable width="400" height="480">
    <v-card>
      <v-card-title class="px-4 py-2">
        <TextInput @input="val => $emit('search', val)" />
      </v-card-title>
      <v-divider></v-divider>
      <v-progress-linear v-if="loading" height="2" indeterminate />
      <v-card-text style="height:228px" class="pa-0">
        <slot name="list"></slot>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-btn text @click="shown_ = false">{{ $t("buttons.cancel") }}</v-btn>
        <v-spacer />
        <v-btn height="36" outlined color="primary" @click="handleSubmitClick"
          ><v-icon v-if="submitBtnIcon">{{ submitBtnIcon }}</v-icon
          >{{ submitBtnText }}</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import TextInput from "./forms/TextInput";

export default {
  components: { TextInput },
  props: [
    "submitHandler",
    "submitBtnText",
    "submitBtnIcon",
    "itemComponent",
    "shown",
    "loading",
    "handleSubmitClick",
  ],
  data() {
    return {
      shown_: false,
    };
  },
  watch: {
    shown(val) {
      this.shown_ = val;
    },
    shown_(val) {
      if (val != this.shown) {
        this.$emit("update:shown", val);
      }
    },
  },
};
</script>
