<template>
  <v-app>
    <v-img src="./assets/app-bar.png" height="150"></v-img>
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
