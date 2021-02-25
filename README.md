# Hyakumori CRM

This repository holds the source code for the Hyakumori CRM. It

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


  [Vuetify]: <https://vuetifyjs.com/en/getting-started/installation/>
  [VueLayers]: <https://vuelayers.github.io/#/>
  [OpenLayers]: <https://openlayers.org>
