<template>
  <div>
    <content-header
      :content="headerContent"
      :toggleEditBtnContent="toggleEditBtnContent"
      :update="isEditing"
      @toggleEdit="handleToggleEdit"
      class="mb-4"
    />
    <archive-participant-list
      :participants="relatedParticipants"
      :isEditing="isEditing"
      @deleteParticipant="handleDeleteParticipant"
      @undoDeletedParticipant="handleUndoDeletedParticipant"
    />
    <select-list-modal
      submitBtnIcon="mdi-plus"
      :loading="itemsForAddingLoading"
      :submitBtnText="$t('buttons.add')"
      :shown.sync="showSelect"
      :handleSubmitClick="submitRelatedParticipant"
      :disableAdditionBtn="itemsForAddingLoading"
      @search="debounceLoadInitItemsForAdding"
      @needToLoad="handleLoadMore"
      ref="selectListModal"
    >
      <template #list>
        <archive-participant-card
          v-for="(participant, index) in itemsForAdding.results"
          showPointer
          :key="index"
          :index="index"
          :name="participant.full_name"
          :showAction="false"
          :card_id="participant.id"
          :selectedId="modalSelectingId"
          @selected="
            (pId, pIndex) => {
              modalSelectingId = pId;
              modelSelectingIndex = pIndex;
            }
          "
          flat
        />
      </template>
    </select-list-modal>
    <template v-if="isEditing">
      <addition-button
        class="my-2"
        :content="addBtnContent"
        :click="() => (showSelect = true)"
      />
      <update-button
        :cancel="cancel"
        :saving="saving"
        :save="updateParticipant"
        :saveDisabled="saveDisabled"
      />
    </template>
  </div>
</template>

<script>
import ContentHeader from "./ContentHeader";
import ContainerMixin from "./ContainerMixin";
import SelectListModalMixin from "./SelectListModalMixin";
import ArchiveParticipantList from "./ArchiveParticipantList";
import AdditionButton from "../AdditionButton";
import UpdateButton from "./UpdateButton";
import SelectListModal from "../SelectListModal";
import ArchiveParticipantCard from "./ArchiveParticipantCard";
import { cloneDeep, pullAllWith, debounce } from "lodash";

export default {
  name: "ArchiveRelatedUserContainer",

  mixins: [ContainerMixin, SelectListModalMixin],

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
      relatedParticipants: [],
      immutableRelatedParticipants: [],
      immutableAllParticipants: [],
      next: "",
      itemsForAddingUrl: "/users/minimal",
      isLoading_: false,
    };
  },

  mounted() {
    this.fetchRelatedParticipants();
  },

  methods: {
    itemsForAddingResultFilter(p) {
      return false;
    },
    handleToggleEdit(val) {
      if (!this.isEditing && this.relatedParticipants) {
        this.immutableRelatedParticipants = cloneDeep(this.relatedParticipants);
      }
      this.isEditing = val;
    },

    cancel() {
      this.isEditing = false;
      this.relatedParticipants = cloneDeep(this.immutableRelatedParticipants);
      this.itemsForAdding = cloneDeep(this.immutableAllParticipants);
    },

    async updateParticipant() {
      if (this.relatedParticipants.length === 0) {
        this.isEditing = false;
      } else {
        this.saving = true;
        await this.deleteParticipants();
        await this.addParticipants();
        this.saving = false;
        this.isEditing = false;
      }
    },

    async deleteParticipants() {
      if (this.deletedParticipants.length > 0) {
        const deletedIds = this.deletedParticipants.map(p => p.id);
        const isDeleted = await this.$rest.delete(
          `/archives/${this.archive_id}/users`,
          {
            data: {
              ids: deletedIds,
            },
          },
        );
        if (isDeleted) {
          this.modalSelectingId = null;
          this.relatedParticipants = this.removeDuplicateParticipant(
            this.relatedParticipants,
            this.deletedParticipants,
          );
          const pureParticipants = cloneDeep(this.deletedParticipants);
          pureParticipants.forEach(p => (p.deleted = false));
          this.itemsForAdding.push(...pureParticipants);
          this.immutableAllParticipants = cloneDeep(this.itemsForAdding);
        }
      }
    },

    async addParticipants() {
      if (this.addedParticipants.length > 0) {
        const addedIds = this.addedParticipants.map(p => p.id);
        const newParticipants = await this.$rest.post(
          `/archives/${this.archive_id}/users`,
          { ids: addedIds },
        );
        if (newParticipants) {
          const tempParticipants = this.removeDuplicateParticipant(
            this.relatedParticipants,
            newParticipants.data,
          );
          this.itemsForAdding = this.removeDuplicateParticipant(
            this.itemsForAdding,
            this.addedParticipants,
          );
          this.immutableAllParticipants = cloneDeep(this.itemsForAdding);
          tempParticipants.push(...newParticipants.data);
          this.relatedParticipants = tempParticipants;
        }
      }
    },

    fetchRelatedParticipants() {
      this.isLoading_ = true;
      this.$rest
        .get(`/archives/${this.archive_id}/users`)
        .then(async response => {
          let tempRelatedData = response.results;
          let next = response.next;
          while (!!next) {
            const paginationResponse = await this.$rest.get(next);
            if (paginationResponse) {
              tempRelatedData.push(...paginationResponse.results);
              next = paginationResponse.next;
            }
          }
          this.relatedParticipants = tempRelatedData;
          this.isLoading_ = false;
        });
    },

    addRelatedParticipant() {
      this.showSelect = true;
      if (this.itemsForAdding.length === 0 || this.next === "") {
        this.fetchAllParticipants();
      }
    },

    submitRelatedParticipant() {
      if (this.modalSelectingId && this.modelSelectingIndex) {
        const selectedParticipant = this.itemsForAdding[
          this.modelSelectingIndex
        ];
        selectedParticipant.added = true;
        this.relatedParticipants.push(selectedParticipant);
        this.itemsForAdding.splice(this.modelSelectingIndex, 1);
        this.modalSelectingId = null;
        this.modelSelectingIndex = null;
      } else {
        this.itemsForAdding[0].added = true;
        this.relatedParticipants.push(this.itemsForAdding[0]);
        this.itemsForAdding.splice(0, 1);
      }
    },

    handleDeleteParticipant(participant, index) {
      if (participant.added) {
        this.relatedParticipants.splice(index, 1);
        this.itemsForAdding = [participant, ...this.itemsForAdding];
      } else {
        this.$set(participant, "deleted", true);
      }
    },

    handleUndoDeletedParticipant(participant) {
      this.$set(participant, "deleted", false);
    },
  },

  computed: {
    saveDisabled() {
      return (
        this.addedParticipants.length === 0 &&
        this.deletedParticipants.length === 0
      );
    },
    addedParticipants() {
      return (
        this.relatedParticipants &&
        this.relatedParticipants.filter(participant => participant.added)
      );
    },

    deletedParticipants() {
      return (
        this.relatedParticipants &&
        this.relatedParticipants.filter(participant => participant.deleted)
      );
    },
  },

  watch: {
    itemsForAdding: {
      deep: true,
      handler(itemsForAdding) {
        if (itemsForAdding.length <= 3 && this.next !== null) {
          this.handleLoadMore();
        }
      },
    },
  },
};
</script>

<style scoped></style>
