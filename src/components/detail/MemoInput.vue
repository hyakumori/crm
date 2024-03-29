<template>
  <div
    class="memo-input ml-6 mb-6"
    @click.stop="hasPermission && (isUpdate = true)"
    :class="{ pointer: !isUpdate && hasPermission }"
  >
    <h4 class="mb-1">備考</h4>
    <v-progress-linear
      height="2"
      indeterminate
      rounded
      v-if="isLoading"
    ></v-progress-linear>

    <v-card
      class="memo-input__card d-flex"
      flat
      :ripple="false"
      :class="{ 'd-hover': !isUpdate }"
    >
      <div class="d-flex pa-4">
        <div v-if="!isUpdate">
          <p class="ma-0" v-if="isEmpty" :class="{ 'grey--text': isEmpty }">
            {{
              (hasPermission && $t("memo.empty")) || $t("memo.empty_view_only")
            }}
          </p>
          <p
            v-else
            class="ma-0"
            v-html="formattedMemo"
            :class="{ 'grey--text': isEmpty }"
          ></p>
        </div>

        <div class="memo-input__value" v-else>
          <ValidationProvider
            name="備考"
            v-slot="{ errors, invalid }"
            slim
            rules="max:255"
            mode="aggressive"
          >
            <v-textarea
              outlined
              name="input-7-4"
              v-model="memo"
              placeholder="テキストを入力してください"
              :error-messages="errors[0]"
            ></v-textarea>

            <update-button
              class="mb-2"
              :saveDisabled="!hasChanged || invalid"
              :cancel="onCancel"
              :save="onSave"
              :saving="isLoading"
            />
          </ValidationProvider>
        </div>
      </div>
    </v-card>
  </div>
</template>

<script>
import { ValidationProvider } from "vee-validate";
import UpdateButton from "./UpdateButton";
import { hasScope } from "../../helpers/security";
import { get as _get } from "lodash";

export default {
  props: {
    apiUrl: { type: String, required: true },
    value: { type: Object },
    objectType: { type: String, required: true }
  },
  components: {
    ValidationProvider,
    UpdateButton
  },
  data() {
    return {
      isLoading: false,
      isUpdate: false,
      memo: _get(this.value, "attributes.memo") || "",
      originalMemo: ""
    };
  },
  methods: {
    async onSave() {
      try {
        this.isLoading = true;
        const response = await this.$rest.post(this.apiUrl, {
          memo: this.memo
        });
        if (response) {
          this.memo = response.memo;
          this.value.attributes["memo"] = response.memo;
          this.$emit("input", this.value);
          this.isUpdate = false;
        }
      } catch (e) {
        if (e.response && e.response.status === 400) {
          this.$dialog.notify.error(e.response.data.errors.memo[0]);
        }
      } finally {
        this.isLoading = false;
      }
    },
    onCancel() {
      this.memo = this.value.attributes["memo"] || "";
      this.isLoading = false;
      this.isUpdate = false;
    }
  },
  computed: {
    hasPermission() {
      return hasScope(`manage_${this.objectType}`);
    },
    formattedMemo() {
      return (this.memo && this.memo.replace(/(?:\r\n|\r|\n)/g, "<br>")) || "";
    },
    isEmpty() {
      return !this.memo;
    },
    hasChanged() {
      return this.originalMemo !== this.memo;
    }
  },
  watch: {
    "value.attributes.memo"() {
      this.memo = this.value.attributes["memo"] || "";
      this.originalMemo = this.memo;
    }
  }
};
</script>

<style lang="scss" scoped>
.pointer {
  cursor: pointer;
}
.memo-input {
  width: 400px;
  word-break: break-all;
  &__card {
    min-height: 70px;
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05);
    align-items: center;
    &__input {
      width: 100%;
    }
  }

  ::v-deep .v-input__slot {
    width: 368px;
  }
}
</style>
