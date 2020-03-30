<template>
  <div class="d-flex align-center table-action">
    <p class="ml-4 mb-0 table-action__text">
      {{ selectedAction }} {{ $t("search.selected_action") }}
    </p>
    <select-list
      class="ml-12 table-action__select"
      :actions="getActions"
      :placeHolder="$t('search.select_action')"
      @selectedAction="onSelected"
    />
  </div>
</template>

<script>
import actions from "../assets/dump/table_actions.json";
import SelectList from "./SelectList";

export default {
  name: "table-action",

  components: {
    SelectList
  },

  data() {
    return {
      selectedAction: null
    };
  },

  methods: {
    onSelected(val) {
      this.selectedAction = val.text;
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
$action-list-color: #825929 !important;

.table-action {
  background: #f7eaa5;
  border-radius: 4px;
  height: 56px;

  &__text {
    font-size: 14px;
    font-weight: bold;
  }

  &__select ::v-deep {
    margin-top: 2px;

    .v-select__slot {
      color: $action-list-color;
    }

    .v-select__selections {
      color: $action-list-color;
    }

    .v-select__selection {
      color: $action-list-color;
    }

    .mdi-chevron-down {
      color: $action-list-color;
    }
  }
}
</style>
