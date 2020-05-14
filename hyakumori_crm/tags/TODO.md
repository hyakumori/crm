# tags settings:
- name (unique)
- code (unique)
- description
- attributes
  - color
- content_type_id
- author

# api
- get tag settings for content_type
- add, update, delete tag settings
- list values
- assign tags

# model usage
- forest, customer -> tags: name:value

# frontend:
- get all tags and listing on left column
- on click, filter by tag name
- get all tags and render by tag settings
- add tag:
  - select tag for content_type_id
  - select all values as options for autocomplete
- allow add tag when finish
- plugin to render tags

# todo:
[v] rename key in forest, using name instead
[v] fix forest import
[v] add tag setting model
[v] listed all tags in model
[v] permission
- api
- remove current implementations on separated fields (tags as separated columns)
- action logs (added tags ...)

# concerns
- how to fetch for different resource?
