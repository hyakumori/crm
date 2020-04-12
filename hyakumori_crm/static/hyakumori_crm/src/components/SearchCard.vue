<template>
  <v-card class="search-card">
    <v-card-title class="search-card__title">{{
      $t("search.search_condition")
    }}</v-card-title>

    <v-form ref="form">
      <div
        class="search-card__search"
        v-for="(condition, index) in conditions"
        :key="index"
      >
        <div class="pb-2">
          <v-select
            ref="selectList"
            append-icon="mdi-chevron-down"
            append-outer-icon="mdi-delete-circle"
            loading="false"
            dense
            clearable
            hide-details
            :name="condition.criteria"
            v-model="condition.criteria"
            :items="fields"
            :placeholder="$t('search.select_item')"
            @click:append-outer="() => deleteSearchField(index)"
          ></v-select>
          <TextInput
            v-model="condition.data"
            :hideDetails="true"
            :placeholder="$t('search.enter_condition')"
            :name="condition.criteria"
          />
        </div>
      </div>

      <div class="d-flex search-card__btn">
        <div class="d-flex align-center" @click="addSearchField">
          <v-icon>mdi-plus</v-icon>
          <span class="ml-1 caption">{{
            $t("search.add_search_condition")
          }}</span>
        </div>
        <v-btn color="primary" depressed @click="onSearch">
          {{ $t("raw_text.search") }}
          <v-icon>mdi-magnify</v-icon>
        </v-btn>
      </div>
    </v-form>
  </v-card>
</template>

<script>
import TextInput from "./forms/TextInput";

export default {
  name: "search-card",

  components: {
    TextInput,
  },

  props: {
    fields: Array,
    onSearch: Function,
  },

  data() {
    return {
      conditions: [
        {
          data: null,
          criteria: null,
        },
      ],
    };
  },

  methods: {
    addSearchField() {
      if (this.conditions.length == this.fields.length) {
        this.$emit("conditionOutOfBounds", true);
      } else {
        this.conditions.push({ data: null, criteria: null });
      }
    },

    deleteSearchField(index) {
      if (this.conditions.length > 1) {
        this.conditions.splice(index, 1);
      } else {
        this.$emit("unableDelete", true);
      }
    },

    isUniqueArr(arr) {
      return arr.length === new Set(arr).size;
    },
  },
};
</script>

<style lang="scss" scoped>
$action-color: #12c7a6;
$text-color: #999999;
$text-field--min-height: 0;
$text-font-size: 14px;

.search-card {
  padding: 18px;
  max-height: 625px;
  overflow: auto;
  min-width: 295px;
  box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05);

  &__title {
    font-size: $text-font-size;
    font-weight: bold;
    color: #444444;
    padding: 0;
  }

  &__search {
    &--color {
      color: $text-color;
    }

    &--spacing ::v-deep {
      padding-top: 0;

      input::placeholder {
        color: $text-color;
      }

      .v-input__icon > i {
        color: $text-color !important;
      }
    }
  }

  &__btn {
    width: 100%;
    color: $action-color;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    margin-top: 5px !important;

    & i {
      color: $action-color;
    }
  }
}
</style>
