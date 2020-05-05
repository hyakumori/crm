<template>
  <div>
    <content-header
      :content="headerContent"
      :editBtnContent="editBtnContent"
      :loading="$store.state.archive.fetchRelatedUserLoading"
      @toggleEdit="val => (isUpdate = val)"
      class="mb-4"
    />
    <archive-participant-list
      :participants="relatedUsers"
      :isUpdate="isUpdate"
    />
    <select-list-modal :shown="shown" @update:shown="val => (shown = val)">
      <template #list>
        <h3>Hello World</h3>
      </template>
    </select-list-modal>
    <template v-if="isUpdate">
      <addition-button
        class="my-2"
        :content="addBtnContent"
        @click="addRelatedUser.bind(this)"
      />
      <update-button :cancel="cancel.bind(this)" />
    </template>
  </div>
</template>

<script>
import ContentHeader from "./ContentHeader";
import ContainerMixin from "./ContainerMixin";
import ArchiveParticipantList from "./ArchiveParticipantList";
import AdditionButton from "../AdditionButton";
import UpdateButton from "./UpdateButton";
import SelectListModal from "../SelectListModal";

export default {
  name: "ArchiveRelatedUserContainer",

  mixins: [ContainerMixin],

  components: {
    ContentHeader,
    ArchiveParticipantList,
    UpdateButton,
    AdditionButton,
    SelectListModal,
  },

  data() {
    return {
      archive_id: this.$route.params.id,
      isUpdate: false,
      relatedUsers: [],
      shown: false,
      fetchRelatedUserLoading: false,
    };
  },

  mounted() {
    this.fetchRelatedUsers();
  },

  methods: {
    async fetchRelatedUsers() {
      await this.$store.dispatch("archive/toggleRelatedUserLoading", true);
      const relatedUsers = await this.$rest.get(
        `/archives/${this.archive_id}/users`,
      );
      await this.$store.dispatch("archive/toggleRelatedUserLoading", false);
      if (relatedUsers) {
        this.relatedUsers = relatedUsers.results;
      }
    },

    addRelatedUser() {
      this.shown = true;
    },
  },
};
</script>

<style scoped></style>
