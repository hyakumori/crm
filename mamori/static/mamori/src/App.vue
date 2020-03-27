<template>
  <v-app>
    <forest />
  </v-app>
</template>

<script>
import Forest from "./screens/Forest";

export default {
  name: "App",

  components: {
    Forest
  },

  data: () => ({}),
  methods: {
    rowData(val) {
      console.log(val);
    }
  }
};
</script>
