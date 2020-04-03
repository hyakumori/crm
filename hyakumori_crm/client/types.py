from ariadne import gql

types = gql(
    """
type Client implements Timestamp & Editor {
  id: ID!
  internal_id: String
  attributes: JSON
  profile: JSON
  updated_by: User
  created_at: DateTime
  updated_at: DateTime
}

type ClientConnection {
  items: [Client!]
  nextToken: String
}

type ClientResponse implements HyakumoriResponse {
  ok: Boolean!
  error: JSON
  client: Client
}

input CreateClientInput {
  internal_id: String
  profile: JSON
  attributes: JSON
}

input TableClientFilterInput {
  id: ID
  internal_id: String
}

input UpdateClientInput {
  internal_id: String
  profile: JSON
  attributes: JSON
  updated_at: DateTime!
}
"""
)
