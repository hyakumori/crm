<template>
  <ValidationProvider
    :vid="vid"
    :rules="rules"
    :name="name || label"
    mode="aggressive"
    v-slot="{ errors }"
    slim
  >
    <v-select
      v-model="innerValue"
      return-object
      single-line
      dense
      outlined
      height="45"
      :items="items"
      :hide-details="hideDetails"
      :placeholder="placeholder"
      :error-messages="errors[0]"
      :clearable="clearable"
      @input="$emit('input', $event)"
      @change="$emit('change', $event)"
    ></v-select>
  </ValidationProvider>
</template>

<script>
import { ValidationProvider } from "vee-validate";

export default {
  components: {
    ValidationProvider
  },
  props: {
    vid: {
      type: String,
      default: undefined
    },
    items: {
      type: Array
    },
    name: {
      type: String,
      default: ""
    },
    label: {
      type: String,
      default: ""
    },
    rules: {
      type: [Object, String],
      default: ""
    },
    placeholder: {
      type: String,
      default: ""
    },
    hideDetails: {
      type: [String, Boolean],
      default: "auto"
    },
    value: {
      type: null,
      default: ""
    },
    clearable: { type: Boolean, default: false }
  },
  data: () => ({
    innerValue: ""
  }),
  computed: {
    hasValue() {
      return !!this.innerValue;
    }
  },
  watch: {
    value(val) {
      if (val !== this.innerValue) {
        this.innerValue = val;
      }
    }
  },
  created() {
    if (this.value) {
      this.innerValue = this.value;
    }
  }
};
</script>
