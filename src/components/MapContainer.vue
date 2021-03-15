<template>
  <div>
    <vl-map
      ref="map"
      data-projection="EPSG:4326"
      @mounted="onMapMounted"
      @singleclick="mapClicked"
      style="height: 400px; width: 100%;"
    >
      <vl-view
        :zoom.sync="zoom"
        :center.sync="center"
        ref="hyakumoriView"
      ></vl-view>
      <vl-layer-tile
        v-for="baseLayer in baseLayers"
        :key="baseLayer.name"
        :id="baseLayer.id"
        :visible="baseLayer.visible"
      >
        <vl-source-xyz
          v-if="baseLayer.type.toLowerCase() === 'xyz'"
          v-bind="baseLayer"
          :url="baseLayer.url"
          :attributions="baseLayer.attributions"
        />
        <vl-source-wms
          v-if="baseLayer.type.toLowerCase() === 'tilewms'"
          v-bind="baseLayer"
          tiled="true"
          :layers="baseLayer.layer"
          :url="baseLayer.url"
          :tile-load-function="imageLoader"
        >
        </vl-source-wms>
        <vl-source-osm
          v-if="baseLayer.type.toLowerCase() === 'osm'"
          v-bind="baseLayer"
        >
        </vl-source-osm>
      </vl-layer-tile>
      <v-menu offset-y :z-index="1005" :close-on-content-click="false">
        <template v-slot:activator="{ on, attrs }">
          <v-btn class="mapLayerBtn" color="primary" v-bind="attrs" v-on="on">
            レイヤー情報
            <v-icon>mdi-layers</v-icon>
          </v-btn>
        </template>
        <div class="panel-area">
          <v-switch
            v-for="layer of vLayers"
            :key="layer.getProperties().id"
            inset
            v-model="layer.getProperties().visible"
            @change="showMapPanelLayer(layer)"
            :label="returnLayerLabel(layer.getProperties().id)"
          >
          </v-switch>
          <v-slider
            prepend-icon="mdi-invert-colors"
            v-model="opacity"
            thumb-label
            values="100"
          >
          </v-slider>
          <v-radio-group mandatory v-model="layerRadio">
            <v-radio
              v-for="layer of baseLayers"
              :key="layer.name"
              :label="layer.name"
              :value="layer.id"
              @change="showBaseLayer(layer.id)"
            >
            </v-radio>
          </v-radio-group>
        </div>
      </v-menu>

      <div v-if="big">
        <vl-layer-image id="wmsLayer" :z-index="1000" :visible="true">
          <vl-source-image-wms
            :url="cadastral.url"
            :layers="cadastral.layer"
            :projection="cadastral.projection"
            :image-load-function="imageLoader"
            ref="hyakumoriSource"
          >
          </vl-source-image-wms>
        </vl-layer-image>

        <vl-overlay :position="overlayCoordinate">
          <template v-if="showCard">
            <v-card>
              <v-system-bar
                color="primary darken-2"
                dark
              >
                <v-spacer></v-spacer>
                <v-icon @click="showCard = false">mdi-close</v-icon>
              </v-system-bar>
              <v-card-text v-if="selectedFeature.textTwo" class="text-center">
                大茅: {{ selectedFeature.textOne }} -
                {{ selectedFeature.textTwo }}
                <v-icon
                  color="primary"
                  v-on:click="routeForest(selectedFeature.forestID)"
                >
                  mdi-arrow-right-circle</v-icon
                >
                <br />
                所有者: {{ selectedFeature.textName }}
              </v-card-text>
              <v-card-text v-else class="text-center">
                大茅: {{ selectedFeature.textOne }}
                <v-icon
                  color="primary"
                  v-on:click="routeForest(selectedFeature.forestID)"
                >
                  mdi-arrow-right-circle</v-icon
                >
                <br />
                所有者: {{ selectedFeature.textName }}
              </v-card-text>
            </v-card>
          </template>
        </vl-overlay>

        <vl-layer-vector id="tableLayer" :z-index="1001" :visible="true">
          <vl-source-vector ref="jsonSource" :features.sync="features">
          </vl-source-vector>
          <vl-style-box>
            <vl-style-stroke color="rgb(39,78,19)" :width="2"></vl-style-stroke>
            <vl-style-fill :color="color"></vl-style-fill>
          </vl-style-box>
        </vl-layer-vector>

        <vl-interaction-select
          :features.sync="selectedFeatures"
          :condition="singleClick"
        >
          <vl-style-box>
            <vl-style-stroke color="blue"></vl-style-stroke>
            <vl-style-fill color="rgba(255,255,255,0.5)"></vl-style-fill>
          </vl-style-box>
        </vl-interaction-select>
      </div>

      <div v-else>
        <vl-layer-image id="wmsLayer" :z-index="1000" :visible="false">
          <vl-source-image-wms
            :url="cadastral.url"
            :layers="cadastral.layer"
            :projection="cadastral.projection"
            :image-load-function="imageLoader"
          >
          </vl-source-image-wms>
        </vl-layer-image>

        <vl-layer-vector id="tableLayer" :z-index="1001" :visible="true">
          <vl-source-vector ref="jsonSource" :features.sync="features">
          </vl-source-vector>
          <vl-style-box>
            <vl-style-stroke color="rgb(39,78,19)" :width="2"></vl-style-stroke>
            <vl-style-fill :color="color"></vl-style-fill>
          </vl-style-box>
        </vl-layer-vector>

        <vl-interaction-select
          @select="selectPoly"
          @unselect="unSelectPoly"
          :features.sync="selectedFeatures"
        >
          <vl-style-box>
            <vl-style-stroke color="blue"></vl-style-stroke>
            <vl-style-fill color="rgba(255,255,255,0.5)"></vl-style-fill>
          </vl-style-box>
        </vl-interaction-select>
      </div>
    </vl-map>
  </div>
</template>

<script>
import Vue from "vue";
import VueLayers from "vuelayers";
import VectorSource from "vuelayers";
import WmsSource from "vuelayers";
import "vuelayers/lib/style.css";
import { ScaleLine } from "ol/control";
import { SelectInteraction } from "vuelayers";
import { Fill, Stroke, Text, Style } from "ol/style";
import { singleClick } from "ol/events/condition";
import { findPointOnSurface } from "vuelayers/src/ol-ext/geom";

Vue.use(SelectInteraction);
Vue.use(WmsSource);
Vue.use(VueLayers);
Vue.use(VectorSource);

export default {
  name: "map-container",

  props: {
    forests: {
      type: Array,
      required: true
    },
    big: {
      type: Boolean,
      default: false
    },

    echoedForestIdFromTable: {
      type: String,
      default: null
    }
  },

  data() {
    const zoom = parseInt(process.env.VUE_APP_MAP_ZOOM);
    const center = process.env.VUE_APP_MAP_CENTER.split(" ");
    const features = [];
    const loading = false;
    const mapLayers = [];
    const panelOpen = false;
    const mapVisible = true;
    const selectedFeature = "";
    const showCard = false;
    const selectedFeatures = [];
    const overlayCoordinate = [0, 0];
    const opacity = 50;

    let baseLayers = JSON.parse(process.env.VUE_APP_MAP_TILESOURCES);
    baseLayers = baseLayers.map(obj => ({ ...obj, visible: false }));
    baseLayers[0].visible = true;

    const cadastral = JSON.parse(process.env.VUE_APP_MAP_CADASTRAL);

    const layerRadio = baseLayers[0]["id"];

    const timeout = null;

    return {
      zoom,
      center,
      features,
      loading,
      mapLayers,
      panelOpen,
      mapVisible,
      baseLayers,
      selectedFeature,
      selectedFeatures,
      overlayCoordinate,
      showCard,
      opacity,
      layerRadio,
      timeout,
      cadastral
    };
  },

  mounted() {
    this.loading = true;
    this.loadMapFeatures().then(f => {
      this.features = f;
      this.initialFeatures = f;
      this.loading = false;
    });
  },

  computed: {
    color() {
      return "rgba(106,168,79,".concat(String(this.opacity / 100)).concat(")");
    },

    vLayers() {
      const allLayers = this.mapLayers;
      return allLayers.filter(function(el) {
        return ["wmsLayer", "tableLayer"].includes(el.getProperties().id);
      });
    },

    singleClick() {
      return singleClick;
    }
  },

  watch: {
    forests: {
      handler() {
        this.loadMapFeatures().then(f => {
          this.features = f;
        });
      }
    },

    echoedForestIdFromTable(val, prev) {
      const featuresSource = this.vLayers
        .find(l => l.values_.id === "tableLayer")
        .getSource();
      const filteredFeature = featuresSource
        .getFeatures()
        .find(f => f.getId() === val);
      const prevFilteredFeature = featuresSource
        .getFeatures()
        .find(f => f.getId() === prev);

      if (filteredFeature) {
        const style = new Style({
          stroke: new Stroke({ color: "FFF" }),
          fill: new Fill({ color: "gray" }),
          text: new Text({
            text: filteredFeature.values_.nametag
          })
        });

        filteredFeature.setStyle(style);
      }

      if (prev) {
        const unstyle = new Style({
          stroke: new Stroke({ color: "rgb(39,78,19)", width: 2 }),
          fill: new Fill({ color: this.color }),
          text: new Text({
            text: prevFilteredFeature.values_.nametag
          })
        });

        prevFilteredFeature.setStyle(unstyle);
      }
    }
  },

  methods: {
    routeForest(val) {
      this.$router.push(`forests/${val}`);
    },

    onMapMounted() {
      this.$refs.map.$map.getControls().extend([new ScaleLine()]);
      this.returnMapLayers().then(l => {
        this.mapLayers = l;
      });

      this.zoomToFeatures();
    },

    zoomToFeatures() {
      if (this.timeout) {
        clearTimeout(this.timeout);
      }
      this.timeout = setTimeout(() => {
        this.$refs.hyakumoriView.$view.fit(
          this.$refs.jsonSource.$source.getExtent(),
          {
            duration: 50
          }
        );
      }, 100);
    },

    selectPoly(val) {
      const style = new Style({
        stroke: new Stroke({ color: "FFF" }),
        fill: new Fill({ color: "gray" }),
        text: new Text({
          text: val.values_.nametag
        })
      });
      val.setStyle(style);
      this.zoomToSelectedFeature(val);
      this.$emit("echoSelectedFeature", val.getId());
    },

    unSelectPoly(val) {
      const style = new Style({
        stroke: new Stroke({ color: "rgb(39,78,19)", width: 2 }),
        fill: new Fill({ color: this.color }),
        text: new Text({
          text: val.values_.nametag
        })
      });
      val.setStyle(style);
      this.$emit("echoSelectedFeature", null);
    },

    returnLayerLabel(layerId) {
      const names = {
        wmsLayer: "全ての地番",
        tableLayer: "表内の情報"
      };
      return names[layerId];
    },

    returnMapLayers() {
      const layers = this.$refs.map.getLayers();
      return new Promise(resolve => {
        resolve(layers);
      });
    },

    loadMapFeatures() {
      const mapItems = this.forests.map(f => {
        return {
          type: "Feature",
          id: f.id,
          geometry: f.geodata,
          properties: {
            customer: f.attributes.customer_cache,
            internal_id: f.internal_id,
            nametag: f.tags["団地"] + " " + f.internal_id,
            land_attributes: f.land_attributes
          }
        };
      });

      return new Promise(resolve => {
        resolve(mapItems);
      });
    },

    imageLoader(im, src) {
      const xhr = new XMLHttpRequest();
      xhr.open("GET", src);
      xhr.setRequestHeader(
        "Authorization",
        "Bearer " + localStorage.getItem("accessToken")
      );
      xhr.responseType = "arraybuffer";
      xhr.onload = function() {
        const arrayBufferView = new Uint8Array(this.response);
        const blob = new Blob([arrayBufferView], { type: "image/png" });
        const urlCreator = window.URL || window.webkitURL;
        im.getImage().src = urlCreator.createObjectURL(blob);
      };
      xhr.send();
    },

    showMapPanelLayer(layer) {
      layer.getProperties().visible
        ? layer.setVisible(false)
        : layer.setVisible(true);
    },

    showBaseLayer(id) {
      let currentLayer = this.baseLayers.find(layer => layer.visible);
      currentLayer.visible = false;
      let newLayer = this.baseLayers.find(layer => layer.id === id);
      newLayer.visible = true;
    },

    returnPopupText(feature) {
      const forestID = feature.properties.id;
      const textOne = JSON.parse(feature.properties.land_attributes)[
        "地番本番"
      ];
      const textTwo = JSON.parse(feature.properties.land_attributes)[
        "地番支番"
      ];
      const textName = JSON.parse(feature.properties.attributes).customer_cache
        .repr_name_kanji;
      return { textTwo, textOne, textName, forestID };
    },

    async mapClicked(event) {
      if (this.$refs.hyakumoriSource) {
        const loggedURL = this.$refs.hyakumoriSource.getFeatureInfoUrl(
          event.coordinate,
          0.000001,
          "EPSG:4326",
          {
            INFO_FORMAT: "application/json",
            feature_count: 1,
            query_layers: "crm:Forests"
          }
        );
        this.overlayCoordinate = event.coordinate;

        let featureRequest = await this.$rest(loggedURL);
        if (featureRequest.numberReturned > 0) {
          this.selectedFeature = this.returnPopupText(
            featureRequest.features[0]
          );
          this.showCard = true;
        } else {
          this.showCard = false;
        }
      }
    },

    zoomToSelectedFeature(feat) {
      this.$refs.hyakumoriView.$view.fit(feat.getGeometry().getExtent(), {
        duration: 1000
      });
    },

    pointOnSurface: findPointOnSurface
  }
};
</script>

<style lang="scss" scoped>
.panel-area {
  padding: 5px;
  background-color: rgb(238, 232, 232);
  color: black;
  font-size: 1.2em;
  box-shadow: 0 0.25em 0.5em transparentize(#343a3a, 0.8);
}

.mapLayerBtn {
  position: relative;
  float: right;
  right: 10px;
  top: 50px;
  z-index: 1010;
}
</style>
