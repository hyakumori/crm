import * as forestApi from "../../api/forest";
import { find, some } from "lodash";
import { tags_to_array } from "../../helpers/tags";

const state = {
  forest: null,
  forestLoading: false,
  customers: [],
  customersLoading: false,
  customersContacts: [],
  customersContactsLoading: false,
  archives: [],
  postalHistories: [],
  archivesLoading: false,
  postalHistoriesLoading: false
};

const getters = {
  headerInfo(state, getters) {
    if (!state.forest) return {};
    return {
      title: `${getters.sector} ${getters.lotnumber}${getters.sub_lotnumber}`,
      subTitle: getters.owner_repr,
      desc: state.forest.internal_id,
      tags: tags_to_array(state.forest.tags),
      backUrl: { name: "forests" }
    };
  },
  owner_repr(state) {
    const names = state.forest.attributes.customer_cache.repr_name_kanji.split(
      ","
    );
    if (names.length === 0) return "";
    return `${names[0]}${names.length > 1 ? ` 他${names.length - 1}名` : ""}`;
  },
  sector(state) {
    if (!state.forest) return "";
    return state.forest.cadastral.sector;
  },
  lotnumber(state) {
    if (!state.forest) return "";
    return state.forest.land_attributes["地番本番"] || "";
  },
  sub_lotnumber(state) {
    if (!state.forest) return "";
    return state.forest.land_attributes["地番支番"]
      ? "-" + state.forest.land_attributes["地番支番"]
      : "";
  },
  customerIdNameMap(state) {
    if (state.customers.length === 0) return {};
    return Object.fromEntries(
      state.customers.map(c => [c.id, c.self_contact?.name_kanji])
    );
  },
  taggedCustomers(state) {
    if (state.customers.length === 0) return [];
    return state.customers.filter(c => some(Object.values(c.tags), Boolean));
  }
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
  async getCustomersContacts({ commit }, id) {
    commit("customersContactsLoadingOn");
    const contacts = await forestApi.fetchCustomersContacts(id);
    commit("setCustomersContacts", contacts);
    commit("customersContactsLoadingOff");
  },
  async getArchives({ commit }, id) {
    commit("archivesLoadingOn");
    const archives = await forestApi.fetchForestArchives(id);
    commit("setArchives", archives);
    commit("archivesLoadingOff");
  },
  async getPostalHistories({ commit }, id) {
    commit("postalHistoriesLoadingOn");
    const postalHistories = await forestApi.fetchForestPostalHistories(id);
    commit("setPostalHistories", postalHistories);
    commit("postalHistoriesLoadingOff");
  },
  toggleDefaultCustomerLocal({ commit }, { customer_id, val }) {
    commit("toggleDefaultCustomerLocal", { customer_id, val });
  },
  toggleDefaultCustomerContactLocal(
    { commit },
    { customer_id, contact_id, val }
  ) {
    commit("toggleDefaultCustomerContactLocal", {
      customer_id,
      contact_id,
      val
    });
  },
  async toggleDefaultCustomer({}, { id, customer_id, val }) {
    await forestApi.toggleDefaultCustomer(id, customer_id, val);
  },
  async toggleDefaultCustomerContact({}, { id, customer_id, contact_id, val }) {
    await forestApi.toggleDefaultCustomerContact(
      id,
      customer_id,
      contact_id,
      val
    );
  }
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
  setCustomersContacts(state, contacts) {
    state.customersContacts = contacts;
  },
  customersContactsLoadingOn() {
    state.customersContactsLoading = true;
  },
  customersContactsLoadingOff() {
    state.customersContactsLoading = false;
  },
  setArchives(state, archives) {
    state.archives = archives;
  },
  archivesLoadingOn() {
    state.archivesLoading = true;
  },
  archivesLoadingOff() {
    state.archivesLoading = false;
  },
  setPostalHistories(state, postalHistories) {
    state.postalHistories = postalHistories;
  },
  postalHistoriesLoadingOn() {
    state.postalHistoriesLoading = true;
  },
  postalHistoriesLoadingOff() {
    state.postalHistoriesLoading = false;
  },
  toggleDefaultCustomerLocal(state, { customer_id, val }) {
    const newCustomers = [...state.customers];
    const c = find(newCustomers, { id: customer_id });
    c.default = val;
    state.customers = newCustomers;
  },
  toggleDefaultCustomerContactLocal(state, { customer_id, contact_id, val }) {
    const newCustomersContacts = [...state.customersContacts];
    const c = find(newCustomersContacts, {
      id: contact_id,
      customer_id: customer_id
    });
    c.default = val;
    state.customersContacts = newCustomersContacts;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
