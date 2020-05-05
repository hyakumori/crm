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
    <select-list-modal
      submitBtnIcon="mdi-plus"
      :loading="fetchAllUserLoading"
      :submitBtnText="$t('buttons.add')"
      :shown="shown"
      @update:shown="val => (shown = val)"
    >
      <template #list>
        <archive-participant-card
          v-for="(user, index) in allUsers"
          :key="index"
          :name="user.full_name"
          :showAction="false"
          flat
        />
      </template>
    </select-list-modal>
    <template v-if="isUpdate">
      <addition-button
        class="my-2"
        :content="addBtnContent"
        :click="addRelatedUser.bind(this)"
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
import ArchiveParticipantCard from "./ArchiveParticipantCard";

export default {
  name: "ArchiveRelatedUserContainer",

  mixins: [ContainerMixin],

  components: {
    ContentHeader,
    ArchiveParticipantList,
    UpdateButton,
    AdditionButton,
    SelectListModal,
    ArchiveParticipantCard,
  },

  data() {
    return {
      archive_id: this.$route.params.id,
      isUpdate: false,
      relatedUsers: [],
      allUsers: [],
      shown: false,
      next: null,
      fetchRelatedUserLoading: false,
      fetchAllUserLoading: false,
    };
  },

  mounted() {
    this.fetchRelatedUsers();
  },

  methods: {
    fetchRelatedUsers() {
      this.fetchRelatedUserLoading = true;
      this.$rest.get(`/archives/${this.archive_id}/users`).then(res => {
        this.fetchRelatedUserLoading = false;
        this.relatedUsers = res.results;
      });
    },

    fetchAllUsers() {
      this.fetchAllUserLoading = true;
      this.$rest.get(this.next || "/users").then(res => {
        this.fetchAllUserLoading = false;
        this.allUsers = res.results;
        this.next = res.next;
      });
    },

    addRelatedUser() {
      this.shown = true;
      if (this.allUsers.length === 0) {
        this.fetchAllUsers();
      }
    },
  },
};
</script>

<style scoped></style>
