<template>
  <v-card>
    <v-card-title class="justify-start pb-0 px-6 pt-6">
      Error on row number: {{ line }}
    </v-card-title>
    <v-card-text class="pa-6">
      <v-container fluid class="pa-0">
        <v-row no-gutters v-for="(msgs, key) in errors" :key="key">
          <v-col cols="12">
            <p class="mb-0">{{ key === "__root__" ? "row" : key }}</p>
            <ul>
              <li v-for="(msg, msgIndex) in msgs" :key="msgIndex">
                {{ msg }}
              </li>
            </ul>
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    line: Number,
    errors: Object,
  },
};
</script>
>
