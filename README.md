# Hyakumori CRM

This repository holds the source code for the Hyakumori CRM.

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

## Usage

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
          "url": "https://crm-server.demo.georeport.org/geoserver/raster/wms",
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

#### Map Code
The map file is in `src/components/MapContainer.vue`. This file is imported into three separate files:
- Forests.vue
- CustomerDetail.vue
- ForestDetail.vue

Some minor styling is applied to the `<map-container>` component within these files for margin and padding.

The map is created using elements from [VueLayers], which is a wrapper for [OpenLayers]. Some of the documentation in VueLayers is limited, so please refer to OpenLayers for more details.

***Caution***: Any styling changed within `MapContainer.vue` will be reflected across all pages that the `map-container` is called in.

**Map Element**
[The  `vl-map`] declaration. This contains styling for the map's size: `style="height: 400px; width: 100%;"` Changing this will change the size of the map on all pages.

**Map Container Panel Area**

The map has a panel that can be opened and closed by clicking on it. Much of the styling is from Vuetify's integrated styling, which you can read more about in the [Vuetify] documentation. These include the `v-menu, v-switch, v-radio-group, v-radio,` and `v-slider` elements.

The class `.panel-area` controls the styling for the map's panel selection area. The button that controls this panel is styled by the class `.mapLayerBtn`, which controls the location of where the button is.

**Vector Layer styling**

The vector layers are styled using the `vl-style-box` element and its child elements. `vl-style-stroke` and `vl-style-fill` declares the stroke and fill colors respectively.

There are two functions that stylize the vector layers when they are selected / unselected, such as on the map in `Forests.vue`. These are the `selectPoly` and `unSelectPoly` functions. They control the stroke, fill, and text for the selected / unselected features in a map if they are vector features.



  [Vuetify]: <https://vuetifyjs.com/en/getting-started/installation/>
  [VueLayers]: <https://vuelayers.github.io/#/>
  [OpenLayers]: <https://openlayers.org>
  [The `vl-map`]: <https://github.com/hyakumori/crm/blob/e2d824ea06a2d415f845efed66ac778a1537c5a4/src/components/MapContainer.vue#L3>
  [located here]: <https://github.com/hyakumori/crm/blob/e2d824ea06a2d415f845efed66ac778a1537c5a4/src/components/MapContainer.vue#L233>
  [`rasterLayers`]: <https://github.com/hyakumori/crm/blob/e2d824ea06a2d415f845efed66ac778a1537c5a4/src/components/MapContainer.vue#L244>
  [`baseLayers`]: <https://github.com/hyakumori/crm/blob/e2d824ea06a2d415f845efed66ac778a1537c5a4/src/components/MapContainer.vue#L233>
  [`rLayers()`]: <https://github.com/hyakumori/crm/blob/e2d824ea06a2d415f845efed66ac778a1537c5a4/src/components/MapContainer.vue#L314>
  [`returnLayerLabel`]: <https://github.com/hyakumori/crm/blob/e2d824ea06a2d415f845efed66ac778a1537c5a4/src/components/MapContainer.vue#L425>
