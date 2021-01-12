<template>
  <div>
    <content-header :content="headerContent" />
    <div>
      <vl-map
        :load-tiles-while-animating="true"
        :load-tiles-while-interacting="true"
        data-projection="EPSG:4326"
        style="height: 400px"
      >
        <vl-view
          :zoom.sync="zoom"
          :center.sync="center"
          :rotation.sync="rotation"
        ></vl-view>

        <vl-layer-tile>
          <vl-source-osm></vl-source-osm>
        </vl-layer-tile>

        <vl-layer-vector>
          <vl-source-vector :url="urlFunction"></vl-source-vector>
          <!-- <vl-style-box>
            <vl-style-stroke color="green" :width="3"></vl-style-stroke>
            <vl-style-fill color="rgba(255,255,255,0.5)"></vl-style-fill>
          </vl-style-box> -->
        </vl-layer-vector>
      </vl-map>
      <p v-if="loading">
        Loading features, please wait...
      </p>
      <p v-if="features.length > 0">
        Features: {{ forests }}
        <!-- Loaded features: {{ features.map(feature => feature.id) }} -->
      </p>
    </div>
  </div>
</template>
<script>
import axios from "../plugins/http";
import * as olExt from 'vuelayers/lib/ol-ext'
import ContainerMixin from "./detail/ContainerMixin.js";
import ContentHeader from "./detail/ContentHeader";
import Vue from "vue";
import VueLayers from "vuelayers";
import VectorSource from "vuelayers";
import "vuelayers/lib/style.css"; // needs css-loader

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
    const zoom = 2;
    const center = [0, 0];
    const rotation = 0;
    const features = [];
    const loading = false;
    return {
      zoom,
      center,
      rotation,
      features,
      loading,
    };
  },

  mounted() {
    this.loading = true;
    if (this.big) {
      console.log('big!')
      // this.getWfsData()
    } else {
      this.loadFeatures().then(features => {
        this.features = features.map(Object.freeze);
        this.loading = false;
      });
    }
  },
  methods: {
    urlFunction (extent, resolution, projection) {
      return 'http://localhost:8600/geoserver/crm/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=crm%3AForests&outputFormat=application%2Fjson'
    },
    // loadingStrategyFactory () {
    //   // VueLayers.olExt available only in UMD build
    //   // in ES build it should be imported explicitly from 'vuelayers/lib/ol-ext'
    //   return olExt.loadingBBox
    // },
    // emulates external source
    loadMapFeatures() {
      const features = [];
      const featureObject = {
        type: "Feature",
        id: null,
        geometry: null,
      };
      for (f in this.forests) {
        console.log(f, "FOrest?");
        featureObject.id = f.id;
        featureObject.geometry = f.geodata;
        features.push(featureObject);
      }
      console.log(features);
    },

    getWfsData() {
      // const forestData = axios.get('http://localhost:8600/geoserver/crm/ows?service=WFS')
      const forestData = axios.get('http://localhost:8600/geoserver/crm/wms?service=WMS&version=1.1.0&request=GetMap&layers=crm%3AForests&bbox=-180.0%2C-90.0%2C180.0%2C90.0&width=768&height=384&srs=EPSG%3A4326&styles=&format=application/openlayers')
      console.log(forestData)
    },

    loadFeatures() {
      return new Promise(resolve => {
        setTimeout(() => {
          // generate GeoJSON random features
          resolve([
            {
              type: "Feature",
              id: 1232,
              geometry: {
                type: "Polygon",
                coordinates: [
                  [
                    [-23.37890625, 45.336701909968134],
                    [-49.39453125, 33.137551192346145],
                    [-47.4609375, 3.6888551431470478],
                    [-20.390625, -8.059229627200192],
                    [-13.0078125, 20.138470312451155],
                    [-23.37890625, 45.336701909968134],
                  ],
                ],
              },
              properties: {
                name: "Null Country22",
                country: "Japan22",
                city: "osak22a",
                street: "M2inamitanabe",
              },
            },
            {
              type: "Feature",
              id: 112,
              geometry: {
                type: "LineString",
                coordinates: [
                  [44.47265625, -1.7575368113083125],
                  [23.5546875, 9.795677582829743],
                  [47.109375, 23.241346102386135],
                  [22.8515625, 33.137551192346145],
                  [48.33984375, 42.032974332441405],
                  [19.86328125, 48.574789910928864],
                  [47.8125, 56.65622649350222],
                ],
              },
              properties: {
                name: "Null Country",
                country: "Japan",
                city: "osaka",
                street: "Minamitanabe",
              },
            },
          ]);
        }, 5000);
      });
    },
  },
};
</script>
