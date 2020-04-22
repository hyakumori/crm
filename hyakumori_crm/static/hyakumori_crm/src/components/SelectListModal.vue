<template>
  <v-dialog v-model="shown_" scrollable width="480">
    <v-card>
      <v-card-title class="pa-0">
        <TextInput />
      </v-card-title>
      <v-divider></v-divider>

      <slot name="list"></slot>

      <v-divider></v-divider>
      <v-card-actions>
        <v-btn text @click="shown_ = false">{{ $t("buttons.cancel") }}</v-btn>
        <v-spacer />
        <v-btn color="primary"
          ><v-icon v-if="submitBtnIcon"></v-icon>{{ submitBtnText }}</v-btn
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
