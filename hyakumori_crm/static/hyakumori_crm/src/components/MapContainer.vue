<template>
  <div>
    <content-header :content="headerContent" />
    <div>
      <vl-map
        :load-tiles-while-animating="true"
        :load-tiles-while-interacting="true"
        data-projection="EPSG:4326"
        style="height: 900px"
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
        <!-- <vl-layer-image>
          <vl-source-image-wms
            :url.sync="getWmsData"
            :version.sync='version'
            :projection='projection'
            :cross-origin='crossOrigin'
            :ratio='ratio'
            :server-type='serverType'
            />
        </vl-layer-image> -->
        <vl-layer-vector>
          <!-- <vl-source-vector v-if="big" render-mode="image" url='http://localhost:8600/geoserver/crm/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=crm%3AForests&outputFormat=application%2Fjson'></vl-source-vector> -->
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
import ImageWmsSource from "vuelayers";
import WmsSource from "vuelayers";
import "vuelayers/lib/style.css"; // needs css-loader
import { ScaleLine, FullScreen, OverviewMap, ZoomSlider } from "ol/control";
import { Projection, addProjection } from "ol/proj";

Vue.use(VueLayers);
Vue.use(VectorSource);
Vue.use(ImageWmsSource);
Vue.use(WmsSource);

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
    const ratio = 1;
    const layers = [];

    return {
      zoom,
      center,
      rotation,
      features,
      loading,
      layers,
      ratio,
    };
  },

  mounted() {
    this.loading = true;
    if (!this.big) {
      this.loadMapFeatures().then(features => {
        this.features = features.map(Object.freeze);
        console.log(features, 'features')
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

    urlFunction() {
      return "http://localhost:8600/geoserver/crm/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=crm%3AForests&maxFeatures=50&outputFormat=application%2Fjson";
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
        console.log(f, "FOrest?");
        featureObject.id = f.id;
        featureObject.geometry = f.geodata;
        features.push(featureObject);
      }
      console.log(features);
      return new Promise(resolve => {
        resolve(features)
      })
    },

    loadFeatures() {
      return new Promise(resolve => {
        setTimeout(() => {
          // generate GeoJSON random features
          const features = [];
          const featureObject = {
            type: "Feature",
            id: null,
            geometry: null,
          };
          console.log(this.forests)
          for (let f of this.forests) {
            console.log(f, "FOrest?");
            featureObject.id = f.id;
            featureObject.geometry = f.geodata;
            features.push(featureObject);
          }
          console.log(features);
          resolve(features);
        }, 5000);
      });
    },
  },
};
</script>
