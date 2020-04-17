<template>
  <v-card class="login-form pa-0">
    <form>
      <v-card-title class="justify-start pb-0 px-6 pt-6">
        {{ $t("page_header.login") }}
      </v-card-title>

      <v-card-text class="pa-6">
        <v-container fluid class="pa-0">
          <v-row no-gutters>
            <v-col cols="12">
              <label class="font-weight-bold">{{
                $t("login_form.email")
              }}</label>
              <text-input
                v-model="form.email"
                placeholder="abc@example.com"
                rules="required|email"
                type="email"
                name="login_form.email"
              />
            </v-col>
          </v-row>
          <v-row no-gutters class="mt-4">
            <v-col cols="12" class="relative">
              <label class="font-weight-bold">
                {{ $t("login_form.password") }}
              </label>
              <div class="forgot-password-hint">
                <router-link :to="{ name: 'auth-forgot-password' }" class="f14">
                  {{ $t("login_form.forgot_password_hint") }}
                </router-link>
              </div>
              <text-input
                type="password"
                v-model="form.password"
                rules="required|min:8"
                placeholder=" ◍ ◍ ◍ ◍ ◍ ◍ ◍ ◍ "
                name="login_form.password"
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
                >{{ $t("page_header.login") }}
              </v-btn>
            </v-col>
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
        password: "",
      },
      formError: "",
      showPassword: false,
      success: false,
    };
  },
  methods: {
    onSubmit(event) {},
  },
};
</script>

<style lang="scss" scoped>
.login-form {
  background: #fff;
}
.custom-button {
  border-color: #eaeaea;
}
.text-small {
  font-size: 12px;
}
.forgot-password-hint {
  position: absolute;
  right: 0;
  top: 0;
  a {
    text-decoration: none !important;
  }
}
</style>
