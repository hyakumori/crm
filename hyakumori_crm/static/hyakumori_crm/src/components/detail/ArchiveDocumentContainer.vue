<template>
  <div class="attachments">
    <content-header
      class="mb-3"
      :content="headerContent"
      :editBtnContent="editBtnContent"
      :loading="loading"
      @toggleEdit="handleToggleEdit"
    />
    <document-card
      class="my-2"
      v-for="(doc, index) in documents"
      :isUpdating="isUpdate"
      :key="index"
      :fileName="doc.filename || doc.name"
      :downloadUrl="doc.download_url"
      :deleteClick="onDeleteClick.bind(this, index)"
      :downloadClick="onDownloadClick.bind(this, index)"
    />
    <template v-if="isUpdate">
      <div class="attachments__addition-container">
        <addition-button
          class="mb-2"
          :content="addBtnContent"
          :click="onAdditionClick.bind(this)"
        />
        <input
          class="attachments__addition-container__file"
          ref="fileInput"
          type="file"
          accept=".xlsx, .xls, .csv, .doc, .docx, .pdf"
          multiple
          @change="onFileChange"
        />
      </div>
      <update-button
        :cancel="cancel.bind(this)"
        :save="save.bind(this)"
        :save-disabled="saveDisabled"
        :saving="addAttachmentLoading"
      />
    </template>
  </div>
</template>

<script>
import ContentHeader from "./ContentHeader";
import ContainerMixin from "./ContainerMixin";
import DocumentCard from "./DocumentCard";
import UpdateButton from "./UpdateButton";
import AdditionButton from "../AdditionButton";
import { unionWith, isNil, cloneDeep } from "lodash";

export default {
  name: "archive-document-container",

  mixins: [ContainerMixin],

  components: {
    ContentHeader,
    DocumentCard,
    UpdateButton,
    AdditionButton,
  },

  data() {
    return {
      id: this.$route.params.id,
      isUpdate: false,
      documents: [],
      fileRef: this.$refs.fileInput,
      addAttachmentLoading: false,
      loading: false,
      deleteDocuments: [],
      immutableDocs: [],
      saveDisabled: false,
    };
  },

  mounted() {
    this.fetchAttachments();
  },

  methods: {
    handleToggleEdit(val) {
      this.isUpdate = val;
      this.immutableDocs = cloneDeep(this.documents);
    },

    cancel() {
      this.isUpdate = false;
      this.saveDisabled = false;
      this.documents = this.immutableDocs;
      this.deleteDocuments = [];
    },

    async fetchAttachments() {
      this.loading = true;
      const attachments = await this.$rest(`/archives/${this.id}/attachments`)
        .then(res => res)
        .catch();
      if (attachments) {
        this.loading = false;
        this.documents = attachments.data;
      }
    },

    onAdditionClick() {
      this.$refs.fileInput.click();
    },

    onDeleteClick(index) {
      this.deleteDocuments.push(this.documents[index]);
      this.documents.splice(index, 1);
    },

    onDownloadClick(index) {
      document.getElementsByClassName("download")[index].click();
    },

    onFileChange(e) {
      const files = e.target.files;
      this.documents = unionWith(this.documents, files, (document, file) => {
        return (
          (document.name || document.filename) === file.name ||
          document.size === file.size
        );
      });
    },

    save() {
      if (this.documents.length === 0) {
        this.isUpdate = false;
        this.deleteDocuments = [];
      } else {
        this.addAttachmentLoading = true;
        const data = new FormData();
        const newDocs = this.documents.filter(doc => isNil(doc.id));
        newDocs.forEach(doc => data.append("file", doc));
        this.$rest.post(`archives/${this.id}/attachments`, data).then(res => {
          this.documents.splice(
            this.documents.length - 1 - (newDocs.length - 1),
            newDocs.length,
            ...res.data,
          );
          this.addAttachmentLoading = false;
          this.isUpdate = false;
        });
        this.deleteDocuments.forEach(doc => {
          if (doc.id) {
            this.$rest
              .delete(`/archives/${this.id}/attachments/${doc.id}`)
              .then();
          }
        });
        this.deleteDocuments = [];
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.attachments {
  &__addition-container {
    position: relative;
    display: flex;

    &__file {
      position: absolute;
      height: 0;
      width: 0;
    }
  }
}
</style>
