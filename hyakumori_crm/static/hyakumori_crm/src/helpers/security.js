const getScopes = () => {
  let scopes = localStorage.getItem("scopes") || "";
  scopes = scopes.split(",");
  return scopes;
};

const hasScope = scope => {
  return getScopes().findIndex(scope) !== -1;
};

const isLoggedIn = () => {
  return localStorage.getItem("accessToken") || false;
};

export { hasScope, getScopes, isLoggedIn };
