from ariadne import gql

types = gql(
    """
    type Forest implements Timestamp & Editor {
        id: ID!
        internal_id: String
        attributes: JSON
        cadastral: JSON
        owner: JSON
        contracts: JSON
        tag: JSON
        land_attributes: JSON
        forest_attributes: JSON
        geodata: JSON
        updated_by: User
        updated_at: DateTime
        created_at: DateTime
    }

    extend type Query {
        list_forests(data: ForestListFilterInput): ForestListResponse
    }

    type ForestListResponse implements HyakumoriResponse {
        ok: Boolean!
        error: JSON
        forests: [Forest!]
        total: Int
    }

    input ForestListFilterInput {
        page: Int
        items_per_page: Int
        order_by: String
        desc: Boolean
    }
"""
)
