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

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

## Styling the Map

### Map Container

The map file is in `src/components/MapContainer.vue`. This file is imported into three separate files:
- Forests.vue
- CustomerDetail.vue
- ForestDetail.vue

Some minor styling is applied to the `<map-container>` component within these files for margin and padding.

The map is created using elements from [VueLayers], which is a wrapper for [OpenLayers]. Some of the documentation in VueLayers is limited, so please refer to OpenLayers for more details.

***Caution***: Any styling changed within `MapContainer.vue` will be reflected across all pages that the `map-container` is called in.

### Map Element
On Line 3 is the `vl-map` declaration. This contains styling for the map's size: `style="height: 400px; width: 100%;"` Changing this will change the size of the map on all pages.

### Map Container Panel Area

The map has a panel that can be opened and closed by clicking on it. Much of the styling is from Vuetify's integrated styling, which you can read more about in the [Vuetify] documentation. These include the `v-menu, v-switch, v-radio-group, v-radio,` and `v-slider` elements.

The class `.panel-area` controls the styling for the map's panel selection area. The button that controls this panel is styled by the class `.mapLayerBtn`, which controls the location of where the button is.

### Vector Layer styling

The vector layers are styled using the `vl-style-box` element and its child elements. `vl-style-stroke` and `vl-style-fill` declares the stroke and fill colors respectively.

There are two functions that stylize the vector layers when they are selected / unselected, such as on the map in `Forests.vue`. These are the `selectPoly` and `unSelectPoly` functions. They control the stroke, fill, and text for the selected / unselected features in a map if they are vector features.


## Layers

For the time being, layers are located within the `MapContainer.vue` file, starting with line 246.

Base Layers are configured with two variables: `baseLayers` on Line 246, and `rasterLayers` on Line 257. For example, if you wish to add more raster layers, you shall add them to the `rasterLayers` variable.

### Raster Layers

Raster layers are layers that are served from the geoserver. The properties for displaying a raster layer is a JSON object, described as follows:

```
{
  name: String,  // Whichever name you wish to identify it on the map panel

  id: String, // An ID that is used to identify the layer in other functions for display

  visible: Boolean, // Default is fault. Setting to true will force the layer to be displayed when mounted

  url: String, // URL from the geoserver. Example: geoserver_baseUrl.concat("/raster/wms")

  layer: String, // The layer identification that matches what the geoserver serves

  projection: String // Must be EPSG:4326 unless otherwise required.
}

```

Note that if you add or remove raster layers, you must modify the `rLayers()` function on line 343. The `return` must include the ID that is assigned to the layer that is added. Remove the ID from the return clause if you have removed a raster layer.

The `returnLayerLabel` function must also be modified. This is currently on Line 443. Here, the string that you wish to be seen by the client must be added. For example, the `red` raster layer is named `赤色立体図` on line 448.


### Base Layers

The base layer is currently served from a source outside of the geoserver. Open Street Maps is the current default. If you wish to add other base layers, use the following JSON object as an example:

```
{
  name: String,
  id: String,
  visible: Boolean // default should be false if multiple layers are used
  url: String,
  attributions: String // Attributions for where the base layer originates. Should include a URL.
}
```

Note that if you add or remove base layers, you must modify the `rLayers()` function on line 343. The `return` must include the ID that is assigned to the layer that is added. Remove the ID from the return clause if you have removed a base layer.

The `returnLayerLabel` function must also be modified. This is currently on Line 443. Here, the string that you wish to be seen by the client must be added. For example, the `std` base layer is named `標準地図` on line 449.






  [Vuetify]: <https://vuetifyjs.com/en/getting-started/installation/>
  [VueLayers]: <https://vuelayers.github.io/#/>
  [OpenLayers]: <https://openlayers.org>
