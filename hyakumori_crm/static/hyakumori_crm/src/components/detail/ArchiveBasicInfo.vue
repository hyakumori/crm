<template>
  <v-row>
    <v-col cols="6">
      <range-date-picker
        :dates="['2020-03-04', '']"
        label="協議日時|カレンダー"
        v-if="isUpdate || !isDetail"
      />
      <text-info
        :isUpdate="isUpdate"
        @input="input"
        label="協議日時|カレンダー"
        v-else
        :value="info.archive_date"
      />
      <text-info
        :isUpdate="isUpdate || !isDetail"
        @input="input"
        label="今後の対応"
        :value="info.future_response"
      />
    </v-col>

    <v-col cols="6">
      <text-info
        :isUpdate="isUpdate || !isDetail"
        @input="input"
        label="場所"
        :value="info.location"
      />
      <archive-participant-card
        :class="{ 'mt-6': isUpdate }"
        :isAuthor="true"
        class="mt-3"
        :name="info.author"
        v-if="isUpdate || isDetail"
      />
    </v-col>

    <div class="pl-3 container content">
      <h5>協議内容</h5>
      <v-textarea
        :outlined="isUpdate || !isDetail"
        dense
        v-if="isUpdate || !isDetail"
        :value="info.content"
      />
      <p v-else>
        {{ info.content }}
      </p>
    </div>
  </v-row>
</template>

<script>
import TextInfo from "./TextInfo";
import RangeDatePicker from "../RangeDatePicker";
import ArchiveParticipantCard from "./ArchiveParticipantCard";

export default {
  name: "archive-basic-info",

  components: {
    TextInfo,
    RangeDatePicker,
    ArchiveParticipantCard,
  },

  props: {
    info: Object,
    isUpdate: Boolean,
    isSave: Boolean,
    isDetail: Boolean,
  },

  methods: {
    input() {
      // TODO: Handle input
    },
  },
};
</script>

<style lang="scss" scoped>
.content ::v-deep {
  h5,
  p {
    color: #444444;
    font-size: 14px;
  }

  fieldset {
    border: 1px solid #e1e1e1;
  }

  textarea {
    color: #999999;
  }
}
</style>
