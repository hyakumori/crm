<template>
  <main-section class="account-profile">
    <template #section>
      <v-content>
        <v-container grid-list-xs class="main-container">
          <div class="account-profile__section px-7">
            <div id="basic-info">
              <content-header
                content="パスワードを変更する"
                :displayAdditionBtn="false"
                :loading="isLoading"
                @toggleEdit="val => (isUpdate.basicInfo = val)"
              />
              <div class="my-4">
                <ValidationObserver ref="form" v-slot="{ dirty }">
                  <v-row>
                    <v-col>
                      <label class="font-weight-bold">現在のパスワード</label>
                      <text-input
                        name="current_password"
                        v-model="current_password"
                        type="password"
                      ></text-input>
                    </v-col>
                    <v-col>
                      <label class="font-weight-bold">新しいパスワード</label>
                      <text-input
                        name="new_password"
                        v-model="new_password"
                        type="password"
                      ></text-input>
                    </v-col>
                    <v-col>
                      <label class="font-weight-bold"
                        >新しいパスワード（確認用）</label
                      >
                      <text-input
                        name="re_new_password"
                        v-model="re_new_password"
                        type="password"
                      ></text-input>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col style="flex-grow:0;">
                      <v-btn color="primary" @click="onSave">変更する<v-btn>
                    </v-col>
                    <v-col v-if="!dirty && savedSuccess"
                      >パスワードは正常に変更されました</v-col
                    >
                    <v-spacer></v-spacer>
                  </v-row>
                </ValidationObserver>
              </div>
            </div>
          </div>
        </v-container>
      </v-content>
    </template>
  </main-section>
</template>

<script>
import { ValidationObserver } from "vee-validate";
import MainSection from "../components/MainSection";
import ScreenMixin from "./ScreenMixin";
import ContentHeader from "../components/detail/ContentHeader";
import TextInput from "../components/forms/TextInput";
import { fromNow } from "../helpers/datetime";

export default {
  mixins: [ScreenMixin],

  components: {
    MainSection,
    ContentHeader,
    ValidationObserver,
    TextInput,
  },

  data() {
    return {
      current_password: "",
      new_password: "",
      re_new_password: "",
      savedSuccess: false,
    };
  },

  async mounted() {
    this.isLoading = true;
    await this.getUserDetail();
    await this.setHeaderInfo();
    this.isLoading = false;
  },

  methods: {
    async getUserDetail() {
      const response = await this.$rest.get(`/users/me`);
      if (response) {
        this.userInfo = response;
      }
    },
    async getUserPermission(callback) {
      const response = await this.$rest.get(
        `/users/${this.userInfo && this.userInfo.id}/permissions`,
      );
      if (response) {
        this.userPermissions = response;
        if (callback) {
          callback(response);
        }
      }
    },

    async onSave() {
      try {
        await this.$rest.post("/users/set_password", {
          current_password: this.current_password,
          new_password: this.new_password,
          re_new_password: this.re_new_password,
        });
        this.current_password = "";
        this.new_password = "";
        this.re_new_password = "";
        this.$refs.form.reset();
        this.savedSuccess = true;
      } catch (error) {
        if (error.response.status == 400) {
          this.$refs.form.setErrors(error.response.data);
        }
      }
    },

    setHeaderInfo() {
      const fromNowText = fromNow(this.userInfo.last_login);
      const info = {
        title: this.userInfo.username,
        subTitle:
          fromNowText &&
          `${this.$t(
            "user_management.tables.headers.last_login",
          )} ${fromNowText}`,
        backUrl: "/me",
      };
      this.$store.dispatch("setHeaderInfo", info);
      this.$store.dispatch("setBackBtnContent", "プロフィール");
    },
  },
  watch: {},
};
</script>

<style lang="scss" scoped>
@import "../styles/variables";

.account-profile {
  &__section {
    @extend %detail-section-shared;
    width: auto;
  }

  &__expand {
    margin-top: 20px;
    margin-bottom: 50px;
    width: fit-content;
    font-size: 14px;
    color: #999999;

    &:hover {
      cursor: pointer;
    }
  }

  &__header {
    &--text {
      display: flex;
      justify-content: center;
      font-size: 14px;
      color: #444444;
      font-weight: bold;

      &__data--color {
        color: #579513;
      }
    }
  }
  .main-container {
    padding: 0;
    max-width: 974px;
  }
}
</style>
