<template>
  <v-content>
    <v-container grid-list-xs class="pa-0">
      <v-card class="pa-0 elevation-24">
        <v-card-title class="justify-center pb-0 px-6 pt-6">
          {{ $t("page_header.logout") }}
        </v-card-title>
        <v-card-text class="pa-6">
          <v-container fluid class="pa-0">
            <v-row no-gutters>
              <v-col cols="12">
                <p class="text-center">
                  {{ $t("messages.logging_out") }}
                </p>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-container>
  </v-content>
</template>

<script>
export default {
  mounted() {
    setTimeout(() => {
      localStorage.clear();
      this.$router.replace({ name: "auth-login" });
    }, 1000);
  }
};
</script>
