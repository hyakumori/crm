<template>
  <div>
    <content-header
      :content="headerContent"
    />
  </div>
</template>
<script>
import ContainerMixin from "./ContainerMixin";
import ContentHeader from "./ContentHeader";

export default {
  name: "map-container",

  mixins: [ContainerMixin, SelectListModalMixin],

  components: {
    ContentHeader,
  }
}
</script>
