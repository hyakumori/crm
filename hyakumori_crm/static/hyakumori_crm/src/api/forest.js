import axios from "../plugins/http";

export function fetchBasicInfo(forestId) {
  return axios.get(`forests/${forestId}`);
}

export async function fetchForestOwners(forestId) {
  const customers = [];
  let data = await axios.get(`forests/${forestId}/customers`);
  customers.push(...data.results);
  while (data.next) {
    data = await axios.get(data.next);
    customers.push(...data.results);
  }
  return customers;
}

export function updateBasicInfo(forestId, info) {
  return axios.put(`forests/${forestId}/basic-info`, info);
}
