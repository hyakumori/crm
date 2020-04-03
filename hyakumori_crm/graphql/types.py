from ariadne import gql

types = gql(
    """
scalar Date
scalar DateTime
scalar JSON

type User {
    id: ID!
}

type Query {
  get_client(id: ID!): ClientResponse
  list_clients(filter: TableClientFilterInput, limit: Int, nextToken: String): ClientConnection
  list_forests: ForestListResponse
}

type Mutation {
  create_client(data: CreateClientInput!): ClientResponse
  delete_client(pk: ID!): ClientResponse
  update_client(pk: ID!, data: UpdateClientInput!): ClientResponse
}

interface Timestamp {
    created_at: DateTime
    updated_at: DateTime
}

interface Editor {
    updated_by: User
}

interface HyakumoriResponse {
    ok: Boolean!
    error: JSON
}
"""
)
