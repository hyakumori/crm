<template>
  <v-row>
    <v-col cols="6">
      <text-info title="口座指定者" info="山田 花子" :isUpdate="isUpdate" />
      <text-info title="支店名|検索" info="424-0023" :isUpdate="isUpdate" />
      <text-info title="口座番号" info="090-1242-2122" :isUpdate="isUpdate" />
    </v-col>
    <v-col cols="6">
      <text-info title="銀行名|検索" info="三井住友銀行" :isUpdate="isUpdate" />
      <text-info
        title="預金種類|選択式"
        info="岡山県倉敷市大谷4-1-3"
        :isUpdate="isUpdate"
      />
      <text-info title="口座名義" info="03-1212-4131" :isUpdate="isUpdate" />
    </v-col>
  </v-row>
</template>

<script>
import TextInfo from "../detail/TextInfo";

export default {
  name: "account-info",

  components: {
    TextInfo,
  },

  props: {
    isUpdate: Boolean,
  },
};
</script>
