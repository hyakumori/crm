const state = {
  fetchRelatedUserLoading: false,
};

const actions = {
  toggleRelatedUserLoading({ commit }, loading) {
    commit("setRelatedUserLoading", loading);
  },
};

const mutations = {
  setRelatedUserLoading(state, loading) {
    state.fetchRelatedUserLoading = loading;
  },
};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
};
