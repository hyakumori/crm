from ariadne import gql

types = gql(
    """
enum RelativeType {
  SON
  DAUGHTER
  WIFE
  HUSBAND
  GRANDSON
  GRANDDAUGHTER
  SISTER
  BROTHER
}

type Customer implements Timestamp & Editor {
  id: ID!
  internal_id: String
  attributes: JSON
  profile: JSON
  updated_by: User
  created_at: DateTime
  updated_at: DateTime
}

type CustomerItem {
  fullname: String!
  address: String
  phone: String
  representative: String
}

type CustomerList implements HyakumoriResponse {
  ok: Boolean!
  error: JSON
  items: [CustomerItem!]
  total: Int
}

type CustomerResponse implements HyakumoriResponse {
  ok: Boolean!
  error: JSON
  customer: Customer
}

type Mutation {
  create_customer(data: CreateCustomerInput!): CustomerResponse
  delete_customer(pk: ID!): CustomerResponse
  update_customer(pk: ID!, data: UpdateCustomerInput!): CustomerResponse
}

type Query {
  get_customer(id: ID!): CustomerResponse
  list_customers(data: TableCustomerFilterInput!): CustomerList!
}

input CreateCustomerInput {
  internal_id: String
  name_kanji: JSON!
  name_kana: JSON!
  address: JSON
  basic_contact: JSON!
  banking: JSON
  status: String
}

input TableCustomerFilterInput {
  id: ID
  internal_id: String
  page: Int!
  itemsPerPage: Int!
  preItemsPerPage: Int
  sortBy: [String]
  sortDesc: [Boolean]
}

input UpdateCustomerInput {
  internal_id: String
  profile: JSON
  attributes: JSON
  updated_at: DateTime!
}
"""
)
