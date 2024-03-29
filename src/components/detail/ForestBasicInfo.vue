<template>
  <ValidationObserver ref="observer" v-slot="{ invalid }">
    <v-container class="forest-basic-info pa-0">
      <template v-if="!isUpdate">
        <v-row v-if="innerInfo" dense>
          <v-col cols="6">
            <text-info label="住所" :value="fullAddress" />
          </v-col>
          <v-col cols="6">
            <text-info
              label="字"
              name="字"
              rules="max:255"
              :value="address && address.subsector"
              :isUpdate="isUpdate"
              @input="val => (address.subsector = val)"
            />
          </v-col>
        </v-row>

        <v-row dense>
          <v-col cols="6">
            <text-info
              label="地番本番"
              :value="landAttributes && landAttributes['地番本番']"
            />
          </v-col>
          <v-col cols="6">
            <text-info
              label="地番支番"
              :value="landAttributes && landAttributes['地番支番']"
            />
          </v-col>
        </v-row>

        <v-row dense>
          <v-col cols="6">
            <text-info label="契約種類" :value="contractType">
              <template #readonly-extend v-if="contractStatus">
                <v-chip
                  small
                  class="contract-status"
                  outlined
                  :color="colorsMap[contractStatus]"
                  >{{ contractStatus }}</v-chip
                >
              </template>
            </text-info>
          </v-col>
          <v-col cols="6">
            <text-info label="契約期間" :value="formattedContractPeriod" />
          </v-col>
        </v-row>

        <v-row dense>
          <v-col cols="6">
            <text-info label="FSC認証" :value="fscStatus" />
          </v-col>
          <v-col cols="6">
            <text-info label="FSC開始日" :value="fscPeriod[0]" />
          </v-col>
        </v-row>
      </template>
      <template v-else>
        <v-row v-if="innerInfo">
          <v-col cols="4">
            <text-info
              label="都道府県"
              name="都道府県"
              rules="required|max:255"
              :value="innerInfo.cadastral.prefecture"
              :isUpdate="isUpdate"
              @input="val => (innerInfo.cadastral.prefecture = val)"
            />
          </v-col>
          <v-col cols="4">
            <text-info
              label="市町村"
              name="市町村"
              rules="required|max:255"
              :value="innerInfo.cadastral.municipality"
              :isUpdate="isUpdate"
              @input="val => (innerInfo.cadastral.municipality = val)"
            />
          </v-col>
          <v-col cols="4">
            <text-info
              label="大字"
              name="大字"
              rules="max:255"
              :value="innerInfo.cadastral.sector"
              :isUpdate="isUpdate"
              @input="val => (innerInfo.cadastral.sector = val)"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="4">
            <text-info
              label="字"
              name="字"
              rules="max:255"
              :value="innerInfo.cadastral.subsector"
              :isUpdate="isUpdate"
              @input="val => (innerInfo.cadastral.subsector = val)"
            />
          </v-col>
          <v-col cols="4">
            <text-info
              label="地番本番"
              name="地番本番"
              rules="required|min_value:1"
              :value="landAttributes['地番本番']"
              :isUpdate="isUpdate"
              @input="val => (landAttributes['地番本番'] = val)"
            />
          </v-col>

          <v-col cols="4">
            <text-info
              label="地番支番"
              name="地番支番"
              rules="min_value:1"
              :value="landAttributes['地番支番']"
              :isUpdate="isUpdate"
              @input="val => (landAttributes['地番支番'] = val)"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="4">
            <select-info
              :items="contractTypes"
              label="契約種類"
              :value="contractType"
              @change="updateContractType"
              :isUpdate="isUpdate"
              clearable
            />
          </v-col>
          <v-col cols="4">
            <select-info
              :items="contractStatusesSelectItems"
              label="契約ステータス"
              :value="contractStatus"
              @change="updateContractStatus"
              :isUpdate="isUpdate"
              clearable
            />
          </v-col>
          <v-col cols="4">
            <range-date-picker
              label="契約期間"
              :dates="contractPeriod"
              @newDates="updateContractDate"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="4">
            <select-info
              :items="[
                { text: '加入', value: '加入' },
                { text: '未加入', value: '未加入' }
              ]"
              label="FSC認証加入"
              :value="fscStatus"
              @change="updateFscStatus"
              :isUpdate="isUpdate"
              clearable
            />
          </v-col>
          <v-col cols="4">
            <single-date-picker
              name="contracts.fsc_start_date"
              label="FSC開始日"
              :readonly="false"
              :date="innerInfo.contracts.fsc_start_date"
              @newDate="val => (innerInfo.contracts.fsc_start_date = val)"
              @change="
                val => {
                  innerInfo.contracts.fsc_start_date = val;
                }
              "
            />
          </v-col>
          <v-col cols="4"> </v-col>
        </v-row>
      </template>
    </v-container>
    <update-button
      class="mb-12"
      v-if="isUpdate"
      :saving="isSave"
      :saveDisabled="invalid"
      :save="() => $emit('updateInfo', innerInfo)"
      :cancel="() => $emit('update:isUpdate', false)"
    />
  </ValidationObserver>
</template>

<script>
import TextInfo from "./TextInfo";
import SelectInfo from "./SelectInfo";
import RangeDatePicker from "../RangeDatePicker";
import SingleDatePicker from "../SingleDatePicker";
import UpdateButton from "./UpdateButton";
import { ValidationObserver } from "vee-validate";
import { get as _get, cloneDeep as _cloneDeep } from "lodash";

export default {
  name: "forest-basic-info",

  components: {
    TextInfo,
    SelectInfo,
    RangeDatePicker,
    SingleDatePicker,
    ValidationObserver,
    UpdateButton
  },

  props: {
    info: Object,
    isUpdate: Boolean,
    isSave: Boolean,
    formErrors: Object
  },

  data() {
    return {
      contractTypes: [],
      contractStatuses: {},
      innerInfo: null,
      colorsMap: {
        未契約: "grey--lighten",
        期限切: "orange lighten-2",
        契約済: "primary"
      }
    };
  },

  methods: {
    getRangeDate(val) {
      this.contract.start_date = val[0];
      this.contract.end_date = val[1];
    },
    formatDate(date) {
      return date; // && date.replace(new RegExp("-", "g"), "/");
    },
    async getContractTypes() {
      try {
        const response = await this.$rest.get("/contract_type/active");
        if (response) {
          this.contractTypes = response.map(item => ({
            text: item.name,
            value: item.name
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

    updateContractType(item) {
      this.innerInfo.contracts.contract_type = _get(item, "value");
    },
    updateContractDate(val) {
      this.innerInfo.contracts.contract_start_date = val[0];
      this.innerInfo.contracts.contract_end_date = val[1];
    },
    updateContractStatus(item) {
      this.innerInfo.contracts.contract_status = _get(item, "value");
    },
    updateFscStatus(item) {
      this.innerInfo.contracts.fsc_status = _get(item, "value");
      if (this.innerInfo.contracts.fsc_status !== "加入") {
        const errors = {
          ...this.$refs.observer.errors,
          "contracts.fsc_start_date": []
        };
        this.$refs.observer.setErrors(errors);
      }
    },
    updateFscDate(val) {
      this.innerInfo.contracts.fsc_start_date = val[0];
      this.innerInfo.contracts.fsc_end_date = val[1];
    }
  },

  async mounted() {
    await this.getContractTypes();
    await this.getContractStatuses();
  },

  computed: {
    fscStatus() {
      return _get(this.info, "contracts.fsc_status");
    },
    fscPeriod() {
      let start_date = _get(this.innerInfo, "contracts.fsc_start_date");
      let end_date = _get(this.innerInfo, "contracts.fsc_end_date");
      return [start_date || "", end_date || ""];
    },
    contractType() {
      return _get(this.info, "contracts.contract_type");
    },
    contractStatus() {
      return _get(this.info, "contracts.contract_status");
    },
    address() {
      return this.innerInfo && this.innerInfo.cadastral;
    },
    contract() {
      return _get(this.innerInfo, "contracts");
    },
    fullAddress() {
      let fullAddress = "";
      const address = this.address;
      if (address) {
        fullAddress =
          address.prefecture + address.municipality + (address.sector || "");
      }
      return fullAddress;
    },
    formattedContractPeriod() {
      let fullDate = "";
      const contract = this.contract;
      if (contract) {
        fullDate =
          `${this.formatDate(contract.contract_start_date) || ""}` +
          `${contract.contract_start_date ? " ～ " : ""}` +
          `${this.formatDate(contract.contract_end_date) || "未入力"}`;
      }
      return fullDate;
    },
    contractPeriod() {
      return [
        this.contract.contract_start_date || "",
        this.contract.contract_end_date || ""
      ];
    },
    contractStatusesSelectItems() {
      return Object.keys(this.contractStatuses).map(key => ({
        text: this.contractStatuses[key],
        value: this.contractStatuses[key]
      }));
    },
    landAttributes() {
      return this.innerInfo && this.innerInfo["land_attributes"];
    }
  },

  watch: {
    formErrors(val) {
      if (val) {
        this.$refs.observer.setErrors(val);
      }
    },
    info(val) {
      this.innerInfo = _cloneDeep(val);
    },
    isUpdate(val) {
      if (!val && this.$refs.observer.flags.dirty) {
        this.innerInfo = _cloneDeep(this.info);
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.forest-basic-info {
  .text-info {
    padding-bottom: 12px;
  }
}
</style>
