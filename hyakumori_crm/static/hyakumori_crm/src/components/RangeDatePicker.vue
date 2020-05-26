<template>
  <div class="range-date-picker">
    <h5>{{ label }}</h5>
    <v-menu
      ref="menu"
      v-model="menu"
      transition="scale-transition"
      min-width="290px"
      offset-y
      nudge-top="20"
      :close-on-content-click="false"
      :return-value.sync="innerDates"
    >
      <template v-slot:activator="{ on }">
        <v-text-field
          v-model="innerDateRange"
          height="45"
          dense
          placeholder="例：2020-12-24 ～ 2025-12-24"
          single-line
          v-mask="'####-##-## ～ ####-##-##'"
          outlined
          v-on="on"
          :error="!isDefaultDateEmpty && hasInvalidDate"
        ></v-text-field>
      </template>
      <v-date-picker
        v-model="innerDates"
        range
        no-title
        scrollable
        reactive
        @change="() => save(false)"
      >
        <v-spacer></v-spacer>
        <v-btn text color="primary" @click="menu = false">キャンセル</v-btn>
        <v-btn text color="primary" @click="save">OK</v-btn>
      </v-date-picker>
    </v-menu>
  </div>
</template>

<script>
import { parse, isValid, format } from "date-fns";

const dateSeparator = " ～ ";

export default {
  name: "range-date-picker",

  props: {
    label: String,
    dates: Array,
  },

  data() {
    return {
      menu: false,
      innerDates: this.dates,
      innerDateRange: this.dates.join(dateSeparator),
    };
  },

  methods: {
    save(closeMenu = true) {
      if (closeMenu) {
        this.$refs.menu.save(this.innerDates);
      }
      this.$emit("newDates", this.innerDates);
      this.innerDateRange = this.innerDates.join(dateSeparator);
    },
    rangeToInnerDate() {
      if (this.hasInvalidDate) {
        return;
      }
      this.innerDates = this.innerDateRange
        .split(dateSeparator)
        .map(d => d.trim())
        .map(d => parse(d, "yyyy-MM-dd", new Date()))
        .map(d => format(d, "yyyy-MM-dd"));
    },
  },

  computed: {
    isDefaultDateEmpty() {
      return this.innerDates.every(d => d.length === 0);
    },
    hasInvalidDate() {
      const parts = this.innerDateRange
        .split(dateSeparator)
        .map(part => part.trim())
        .map(d => parse(d, "yyyy-MM-dd", new Date()));
      const check =
        parts.length < 2 ||
        !parts.every(part => isValid(part)) ||
        parts[0] > parts[1];
      return check;
    },
  },
  watch: {
    innerDateRange() {
      this.rangeToInnerDate();
    },
    innerDates: {
      deep: true,
      handler(val) {
        this.$emit("newDates", val);
      },
    },
    menu() {
      if (this.menu === false) {
        this.rangeToInnerDate();
        this.$refs.menu.save(this.innerDates);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "src/styles/variables";

.range-date-picker ::v-deep {
  @extend %picker-shared;
}
</style>
