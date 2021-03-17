# Hyakumori CRM

A CRM web application for forestry management under the Hyakumori Project.   

## Requirements

- yarn >= 1.22.5

## Installation

1. Copy `.env.example` to `.env` and fill necessary variables.

```
cp .env.example .env
```

2. Install yarn dependencies.

```
yarn install
```

## How to use

Compile the app and launch with hot-reload for development with:

```
yarn serve
```

Or build for production with:

```
yarn build
```

## Development Tips

Linting:

```
yarn lint
```

## Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

### Map Configuration

Map configurations are set in the `mapconfig.json` file. The current settings are configurable:

* `tilesources`:
  - An array of tile source to be used as base maps in the map.
  - Required with at least one tile source.
  - Each element in the array must be an object with the following properties:
    - `type`: (required) used to build the layer type. Must be one of `"xyz"`, `"osm"`, or `"tilewms"`.
    - `name`: (required) the name of the layer. Used for labeling.
    - `id`: (required) unique identifier.
    - `url`: (required for `tilewms` and `xyz` type) defines the source of the map tile.
    - `attributions`: (required for `xyz` type) defines the attribution of the tile.
    - `projection`: (required for `tilewms` type) defines the projection of the wms layer.
  - e.g.:
    ```json
        [{
          "type": "osm",
          "name": "OSM",
          "id": "osm"
        },
        {
          "type": "xyz",
          "name": "標準地図",
          "id": "std",
          "url": "https://maps.gsi.go.jp/xyz/std/{z}/{x}/{y}.png?_=20201001a",
          "attributions":
          "<a href=\"https://maps.gsi.go.jp/development/ichiran.html\"> 国土地理院 </a>"
        },
        {
          "type": "tilewms",
          "name": "赤色立体図",
          "id": "red",
          "url": "https://crm-server.hyakumori.net/geoserver/raster/wms",
          "layer": "raster:赤色立体図データ",
          "projection": "EPSG:4326"
        }]
    ```
* `cadastral`:
  - An object defining the source of the WMS layer for the cadastral data.
  - Required (source must be a WMS layer).
  - Properties must include:
    - `id`: Unique identifier for the layer. Currently, this _must_ be set to `wmsLayer`.
    - `url`: URL to the wms layer source.
    - `layer`: WMS layer name.
    - `projection`: WMS layer projection. 
  - e.g.: 
    ```json
      {
        "id": "wmsLayer",
        "url": "<add url to wms layer>",
        "layer": "<add layer>",
        "projection": "EPSG:4326"
      }
    ```
* `center`:
  - The map center.
  - Required. Must be a string specifying longitude and latitude separated by a space.
  - e.g. `"134.33234254149718 35.2107812998969"`
* `zoom`:
  - The map zoom.
  - Required. Must be a number surrounded by quotation marks.
  - e.g. `"11"`

Note, if map layers are being served by the Hyakumori API (over proxy), then it is important
 that the URL matches backend env variables defined in the `.env` file.

## Contributing and Support

The Hyakumori Project appreciates any [contributions](https://github.com/hyakumori/.github/blob/main/CONTRIBUTING.md).

## Authors

The Hyakumori CRM was developed by the Hyakumori Team with additional contributions from:

- [Iosefa Percival](https://github.com/iosefa)
- [Nathaniel Nasarow](https://github.com/Torgian)
- ... [and others](https://github.com/hyakumori/crm-server/graphs/contributors)

## LICENSE

This program is free software. See [LICENSE](LICENSE) for more information.
