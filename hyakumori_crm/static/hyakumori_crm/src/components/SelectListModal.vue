<template>
  <v-dialog v-model="shown_" scrollable max-width="720">
    <v-card>
      <v-card-title class="pa-0">
        <TextInput />
      </v-card-title>
      <v-divider></v-divider>

      <v-card-text style="min-height: 300px;" class="px-6 py-5">
        <!-- <ItemComponent v-for="item in items" :key="item.id" /> -->
      </v-card-text>

      <v-divider></v-divider>
      <v-card-actions>
        <v-btn text @click="cancelClick">{{ $t("buttons.cancel") }}</v-btn>
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
    "items",
    "shown",
  ],
  beforeMount() {
    if (this.itemComponent)
      this.$options.components.ItemComponent = this.itemComponent;
  },
  data() {
    return {
      shown_: false,
    };
  },
  methods: {
    cancelClick() {
      this.shown_ = false;
      this.$emit("update:shown", false);
    },
  },
  watch: {
    shown(val) {
      this.shown_ = val;
    },
  },
};
</script>
