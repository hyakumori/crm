<template>
  <div>
    <content-header :content="headerContent" />
    <div>
      <vl-map
        :load-tiles-while-animating="true"
        :load-tiles-while-interacting="true"
        ref="map"
        data-projection="EPSG:4326"
        @mounted="onMapMounted"
        style="height: 600px; width: 100%"
      >
        <vl-view
          :zoom.sync="zoom"
          :center.sync="center"
          :rotation.sync="rotation"
        ></vl-view>

        <vl-layer-tile>
          <vl-source-osm></vl-source-osm>
        </vl-layer-tile>
        <div v-if="big">
          <component
            v-for="layer in layers"
            :is="layer.cmp"
            :key="layer.id"
            v-bind="layer"
          >
            <component :is="layer.source.cmp" v-bind="layer.source">
              <template
                v-if="
                  layer.source.staticFeatures &&
                    layer.source.staticFeatures.length
                "
              >
                <vl-feature
                  v-for="feature in layer.source.staticFeatures"
                  :key="feature.id"
                  :id="feature.id"
                  :properties="feature.properties"
                >
                  <component
                    :is="geometryTypeToCmpName(feature.geometry.type)"
                    v-bind="feature.geometry"
                  />
                </vl-feature>
              </template>
            </component>
          </component>
        </div>
        <vl-layer-vector v-else>
          <vl-source-vector :features.sync="features"></vl-source-vector>
          <vl-style-box>
            <vl-style-stroke color="red" :width="3"></vl-style-stroke>
            <vl-style-fill color="rgba(255,255,255,0.5)"></vl-style-fill>
          </vl-style-box>
        </vl-layer-vector>
      </vl-map>
    </div>
  </div>
</template>
<script>
import axios from "../plugins/http";
import * as olExt from "vuelayers/lib/ol-ext";
import ContainerMixin from "./detail/ContainerMixin.js";
import ContentHeader from "./detail/ContentHeader";
import Vue from "vue";
import VueLayers from "vuelayers";
import VectorSource from "vuelayers";
import "vuelayers/lib/style.css"; // needs css-loader
import { ScaleLine, ZoomSlider } from "ol/control";

Vue.use(VueLayers);
Vue.use(VectorSource);

export default {
  name: "map-container",

  mixins: [ContainerMixin],

  components: {
    ContentHeader,
  },

  props: {
    forests: {
      type: Array,
      required: true,
    },
    big: {
      type: Boolean,
      default: false,
    },
  },

  data() {
    const zoom = 5;
    const center = [-223.11344101316652, 33.82734357069114];
    const rotation = 0;
    const features = [];
    const loading = false;
    const layers = [];

    return {
      zoom,
      center,
      rotation,
      features,
      loading,
      layers,
    };
  },

  mounted() {
    this.loading = true;
    if (!this.big) {
      this.loadMapFeatures().then(features => {
        this.features = features.map(Object.freeze);
        this.loading = false;
      });
    } else {
      this.layers.push(
        {
          id: "wfs",
          title: "WFS",
          cmp: "vl-layer-vector",
          visible: true,
          renderMode: 'image',
          features: [],
          source: {
            cmp: "vl-source-vector",
            url: 'http://localhost:8600/geoserver/crm/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=crm%3AForests&outputFormat=application%2Fjson',
            layers: "crm:forests",
            extParams: { TILED: true },
            serverType: "geoserver",
          },
        },
      );
    }
  },

  methods: {
    geometryTypeToCmpName(type) {
      return "vl-geom-" + kebabCase(type);
    },

    onMapMounted() {
      this.$refs.map.$map.getControls().extend([
        new ScaleLine(),
        new ZoomSlider(),
      ])
    },
    // emulates external source
    loadMapFeatures() {
      const features = [];
      const featureObject = {
        type: "Feature",
        id: null,
        geometry: null,
      };

      for (let f of this.forests) {
        featureObject.id = f.id;
        featureObject.geometry = f.geodata;
        features.push(featureObject);
      }

      return new Promise(resolve => {
        resolve(features)
      })
    },
  },
};
</script>
