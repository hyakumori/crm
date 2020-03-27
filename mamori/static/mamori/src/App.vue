<template>
  <v-app>
    <page-header />
    <forest />
  </v-app>
</template>

<script>
import Forest from "./screens/Forest";
import PageHeader from './components/PageHeader';

export default {
  name: "App",

  components: {
    Forest,
    PageHeader
  },
  data: () => ({}),
  methods: {
    rowData(val) {
      console.log(val);
    }
  }
};
</script>
