<template>
  <v-card class="search-card">
    <v-card-title class="search-card__title">{{
      $t("search.search_condition")
    }}</v-card-title>

    <div
      class="search-card__search"
      v-for="(condition, index) in conditions"
      :key="index"
    >
      <select-list
        class="search-card__search--spacing"
        :placeHolder="$t('search.select_item')"
        :actions="getActions"
        @selectedAction="onSelected"
      />

      <v-text-field
        v-model="condition.input"
        clearable
        outlined
        :placeholder="$t('search.enter_condition')"
      ></v-text-field>
    </div>

    <div class="d-flex align-center justify-space-between search-card__btn">
      <div @click="addSearchField">
        <v-icon>mdi-plus</v-icon>

        <span class="ml-1 caption">{{
          $t("search.add_search_condition")
        }}</span>
      </div>

      <v-btn dark depressed color="#1B756A">
        Search
        <v-icon dark>mdi-magnify</v-icon>
      </v-btn>
    </div>
  </v-card>
</template>

<script>
import SelectList from "./SelectList";
import actions from "../assets/dump/table_actions.json";

export default {
  name: "search-card",

  components: {
    SelectList
  },

  data() {
    return {
      conditions: [
        {
          input: null
        }
      ]
    };
  },

  methods: {
    addSearchField() {
      this.conditions.push({ input: null });
    },

    onSelected(val) {
      console.log(val);
    }
  },

  computed: {
    getActions() {
      return actions;
    }
  }
};
</script>

<style lang="scss" scoped>
$action-color: #12c7a6;
$text-color: #999999;
$text-field--min-height: 0;

.search-card {
  padding: 18px;
  min-height: 628px;
  border-radius: 4px;

  &__title {
    font-size: 14px;
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
        color: $text-color !important;
      }
    }
  }

  &__btn {
    width: 100%;
    color: $action-color;
    cursor: pointer;

    & .v-btn i {
      color: white;
    }

    & .v-icon {
      color: $action-color;
    }
  }
}

.v-input ::v-deep {
  & .v-text-field__details {
    margin-bottom: 0 !important;
    min-height: $text-field--min-height;

    & .v-messages {
      min-height: $text-field--min-height;
    }
  }
}
</style>
