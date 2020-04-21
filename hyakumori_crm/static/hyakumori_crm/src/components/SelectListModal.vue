<template>
  <v-dialog v-model="shown" scrollable max-width="720" :activator="activator">
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
        <v-btn color="primary" @click="submit"
          ><v-icon v-if="submitBtnIcon"></v-icon>{{ submitBtnText }}</v-btn
        >
        <v-btn text @click="shown = false">{{ $t("buttons.cancel") }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import TextInput from "./forms/TextInput";

export default {
  components: { TextInput },
  props: [
    "title",
    "submit",
    "submitBtnText",
    "submitBtnIcon",
    "itemComponent",
    "items",
    "activator",
  ],
  beforeMount() {
    if (this.itemComponent)
      this.$options.components.ItemComponent = this.itemComponent;
  },
  data() {
    return {
      shown: false,
    };
  },
};
</script>
