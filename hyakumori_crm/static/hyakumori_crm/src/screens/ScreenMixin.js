import { flatten } from "lodash";

export default {
  data() {
    return {
      tableSelectedRows: [],
      tagKeys: [],
      showChangeTagDialog: false,
    };
  },
  mounted() {
    this.populateAppHeader();
  },
  methods: {
    populateAppHeader() {
      this.$store.dispatch("setPageHeader", this.pageHeader);
      this.$store.dispatch("setPageIcon", this.pageIcon);
      this.$store.dispatch("setHeaderTagColor", this.headerTagColor);
      this.$store.dispatch("setBackBtnContent", this.backBtnContent);
    },

    async getSelectedObject(apiUrl) {
      try {
        const objects = await this.$rest.put(apiUrl, this.selectedRowIds);
        this.tagKeys = [];
        const tags = objects.map(obj => obj.tags);
        tags.forEach(tag => this.tagKeys.push(Object.keys(tag)));
        this.tagKeys = [...new Set(flatten(this.tagKeys))];
        this.showChangeTagDialog = true;
      } catch (e) {
        this.showChangeTagDialog = false;
      } finally {
      }
    },

    selectedRows(val) {
      this.tableSelectedRows = val;
    },
  },
  computed: {
    requestFilters() {
      return this.$refs.filter
        ? this.$refs.filter.conditions.map(condition => {
            return {
              criteria: condition.criteria,
              keyword: condition.keyword,
            };
          })
        : [];
    },

    selectedRowIds() {
      return (
        this.tableSelectedRows.length > 0 &&
        this.tableSelectedRows.map(row => row.id)
      );
    },
  },
};
