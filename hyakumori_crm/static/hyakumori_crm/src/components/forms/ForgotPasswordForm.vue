<template>
  <v-card class="forgot-password-form pa-0">
    <form>
      <v-card-title class="justify-start pb-0 px-6 pt-6">
        {{ $t("page_header.login") }}
      </v-card-title>

      <v-card-text class="pa-6">
        <v-container fluid class="pa-0">
          <v-row no-gutters>
            <p class="grey--text text--darken-3">
              {{ $t("messages.forgot_password_help_text") }}
            </p>
          </v-row>
          <v-row no-gutters>
            <v-col cols="12">
              <label class="font-weight-bold">{{
                $t("login_form.email")
              }}</label>
              <text-input
                v-model="form.email"
                placeholder="abc@example.com"
                hideDetails
                name="login_form.email"
              />
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-card-actions class="pa-6 pt-0">
        <v-container class="pa-0">
          <v-row class="fill-height">
            <v-col class="pt-0 pb-0 text-right" cols="12">
              <v-btn color="primary" depressed @click="onSubmit" width="100%"
                >{{ $t("buttons.send") }}
              </v-btn>
            </v-col>
          </v-row>
          <v-row>
            <div class="message ma-3 mb-0" v-if="mailSent">
              {{ $t("messages.reset_password_url_sent") }}
            </div>
          </v-row>
          <v-row>
            <a class="no-underline f14 pa-4 pt-6 pb-0" @click="$router.go(-1)">
              {{ $t("buttons.back") }}
            </a>
          </v-row>
        </v-container>
      </v-card-actions>
    </form>
  </v-card>
</template>

<script>
import TextInput from "../forms/TextInput";

export default {
  components: {
    TextInput,
  },
  data() {
    return {
      form: {
        email: "",
      },
      formError: "",
      success: false,
    };
  },
  methods: {
    onSubmit(event) {},
  },
  computed: {
    mailSent: function() {
      return this.success;
    },
  },
};
</script>

<style lang="scss" scoped>
.forgot-password-form {
  background: #fff;
}
.text-small {
  font-size: 12px;
}
.message {
  border-radius: 4px;
  padding: 15px 20px;
  font-size: 14px;
  background: #f5f5f5;
  color: #444444;
}
</style>
