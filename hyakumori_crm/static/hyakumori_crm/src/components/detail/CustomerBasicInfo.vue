<template>
  <v-row>
    <v-col cols="6">
      <text-info title="郵便番号" info="100-1111" :isUpdate="isUpdate" />
      <text-info title="電話番号" info="04-2555-000" :isUpdate="isUpdate" />
      <text-info
        title="メールアドレス"
        info="aa@gmail.com"
        :isUpdate="isUpdate"
      />
    </v-col>
    <v-col col="6">
      <text-info title="住所" info="ヤマダタロウ" :isUpdate="isUpdate" />
      <text-info title="携帯番号" info="ヤマダタロウ" :isUpdate="isUpdate" />
    </v-col>
  </v-row>
</template>

<script>
import TextInfo from "../detail/TextInfo";

export default {
  name: "customer-basic-info",

  components: {
    TextInfo,
  },

  props: {
    isUpdate: Boolean,
  },
};
</script>
