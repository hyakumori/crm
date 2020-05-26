<template>
  <ValidationObserver ref="observer">
    <v-container class="forest-basic-info pa-0">
      <template v-if="!isUpdate">
        <v-row v-if="info" dense>
          <v-col cols="6">
            <text-info label="住所" :value="fullAddress" />
          </v-col>
          <v-col cols="6">
            <text-info
              label="地番"
              name="地番"
              rules="max:255"
              :value="address && address.subsector"
              :isUpdate="isUpdate"
              @input="val => (address.subsector = val)"
            />
          </v-col>
        </v-row>

        <v-row dense>
          <v-col cols="6">
            <text-info label="契約種類" :value="contractType" />
          </v-col>
          <v-col cols="6">
            <text-info label="契約期間" :value="fullDate" />
          </v-col>
        </v-row>

        <v-row dense>
          <v-col cols="6">
            <text-info label="FSC認証加入" :value="fscStatus" />
          </v-col>
          <v-col cols="6">
            <text-info label="FSC認証期間" :value="fscPeriod" />
          </v-col>
        </v-row>
      </template>
      <template v-else>
        <v-row v-if="info">
          <v-col cols="4">
            <text-info
              label="都道府県"
              name="都道府県"
              rules="max:255"
              :value="address.prefecture"
              :isUpdate="isUpdate"
              @input="val => (address.prefecture = val)"
            />
          </v-col>
          <v-col cols="4">
            <text-info
              label="市町村"
              name="市町村"
              rules="max:255"
              :value="address.municipality"
              :isUpdate="isUpdate"
              @input="val => (address.municipality = val)"
            />
          </v-col>
          <v-col cols="4">
            <text-info
              label="大字"
              name="大字"
              rules="max:255"
              :value="address.sector"
              :isUpdate="isUpdate"
              @input="val => (address.sector = val)"
            />
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="4">
            <select-info
              :items="contractTypes"
              label="契約種類"
              :value="contractType"
              @input="updateContractType"
              :isUpdate="isUpdate"
            />
          </v-col>
          <v-col cols="4">
            <range-date-picker
              label="契約期間"
              :dates="dates"
              @newDates="updateContractDate"
            />
          </v-col>
          <v-col cols="4"> </v-col>
        </v-row>
        <v-row>
          <v-col cols="4">
            <select-info
              :items="contractStatusesSelectItems"
              label="FSC認証加入"
              :value="fscStatus"
              :isUpdate="isUpdate"
            />
          </v-col>
          <v-col cols="4">
            <range-date-picker
              label="FSC契約期間"
              :dates="dates"
              @newDates="updateFscDate"
            />
          </v-col>
          <v-col cols="4"> </v-col>
        </v-row>
      </template>
    </v-container>
  </ValidationObserver>
</template>

<script>
import TextInfo from "./TextInfo";
import SelectInfo from "./SelectInfo";
import RangeDatePicker from "../RangeDatePicker";
import { ValidationObserver } from "vee-validate";
import { get as _get } from "lodash";

export default {
  name: "forest-basic-info",

  components: {
    TextInfo,
    SelectInfo,
    RangeDatePicker,
    ValidationObserver,
  },

  props: {
    info: Object,
    isUpdate: Boolean,
    isSave: Boolean,
  },

  methods: {
    getRangeDate(val) {
      this.contract.start_date = val[0];
      this.contract.end_date = val[1];
    },

    formatDate(date) {
      return date && date.replace(new RegExp("-", "g"), "/");
    },

    async getContractTypes() {
      try {
        const response = await this.$rest.get("/contract_type");
        if (response) {
          this.contractTypes = response
            .filter(item => item.attributes && item.attributes.assignable)
            .map(item => ({
              text: item.name,
              value: item.name,
            }));
        }
      } catch {
        this.contractTypes = [];
      }
    },
    async getContractStatuses() {
      try {
        const response = await this.$rest.get("/contract_type/statuses");
        if (response) {
          this.contractStatuses = response;
        }
      } catch {
        this.contractStatuses = [];
      }
    },

    updateContractType(selected) {
      this.innerInfo.contracts.contact_type = selected.value;
    },
    updateContractDate(val) {
      this.innerInfo.contracts.contact_start_date = val[0];
      this.innerInfo.contracts.contact_end_date = val[1];
    },
    updateFscDate(val) {
      this.innerInfo.contracts.fsc_start_date = val[0];
      this.innerInfo.contracts.fsc_end_date = val[1];
    },
  },

  data() {
    return {
      contractTypes: [],
      contractStatuses: {},
    };
  },

  async mounted() {
    await this.getContractTypes();
    await this.getContractStatuses();
  },

  computed: {
    fscStatus() {
      return _get(this.innerInfo, "contracts.fsc_status");
    },
    fscPeriod() {
      let start_date = _get(this.innerInfo, "contracts.fsc_start_date");
      let end_date = _get(this.innerInfo, "contracts.fsc_end_date");
      return `${start_date || ""} - ${end_date || ""}`;
    },
    address() {
      return this.innerInfo && this.innerInfo.cadastral;
    },

    contractType() {
      return _get(this.innerInfo, "contracts.contract_type");
    },

    contract() {
      return _get(this.innerInfo, "contracts");
    },

    innerInfo() {
      return this.info;
    },

    fullAddress() {
      let fullAddress = "";
      const address = this.address;
      if (address) {
        fullAddress =
          address.prefecture + address.municipality + address.sector;
      }
      return fullAddress;
    },

    fullDate() {
      let fullDate = "";
      const contract = this.contract;
      if (contract) {
        fullDate = `${this.formatDate(contract.start_date) || ""} ${
          contract.start_date ? "-" : ""
        }
        ${this.formatDate(contract.end_date) || "未入力"}`;
      }
      return fullDate;
    },

    dates() {
      return [this.contract.start_date || "", this.contract.end_date || ""];
    },

    contractStatusesSelectItems() {
      const items = Object.keys(this.contractStatuses).map(key => ({
        text: this.contractStatuses[key],
        value: this.contractStatuses[key],
      }));
      return items;
    },
  },

  watch: {
    isSave(val) {
      if (val) {
        this.$emit("updateInfo", this.innerInfo);
      }
    },

    info: {
      deep: true,
      async handler() {
        const isValid = await this.$refs.observer.validate();
        this.$emit("forest:save-disable", !isValid);
      },
    },
  },
};
</script>

<style lang="scss" scoped>
.forest-basic-info {
  .text-info {
    padding-bottom: 12px;
  }
}
</style>
