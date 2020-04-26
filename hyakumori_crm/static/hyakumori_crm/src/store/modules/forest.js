import * as forestApi from "../../api/forest";

const state = {
  forest: null,
  forestLoading: false,
  customers: [],
  customersLoading: false,
  customerContacts: [],
  customerContactsLoading: false,
  archives: [],
  archivesLoading: false,
};

const getters = {
  headerInfo(state) {
    if (!state.forest) return {};
    return {
      title: state.forest.internal_id,
      subTitle: state.forest.owner.name_kanji,
      tag: [state.forest.tag.danchi],
      backUrl: { name: "forests" },
    };
  },
};

const actions = {
  async getForest({ commit }, id) {
    commit("forestLoadingOn");
    const forest = await forestApi.fetchBasicInfo(id);
    commit("setForest", forest);
    commit("forestLoadingOff");
  },
  async getCustomers({ commit }, id) {
    commit("customersLoadingOn");
    const customers = await forestApi.fetchForestOwners(id);
    commit("setCustomers", customers);
    commit("customersLoadingOff");
  },
};

const mutations = {
  setForest(state, forest) {
    state.forest = forest;
  },
  forestLoadingOn() {
    state.forestLoading = true;
  },
  forestLoadingOff() {
    state.forestLoading = false;
  },
  setCustomers(state, customers) {
    state.customers = customers;
  },
  customersLoadingOn() {
    state.customersLoading = true;
  },
  customersLoadingOff() {
    state.customersLoading = false;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
