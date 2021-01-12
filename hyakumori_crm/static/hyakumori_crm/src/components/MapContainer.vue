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
          <vl-source-vector :features.sync="features"></vl-source-vector>

          <vl-style-box>
            <vl-style-stroke color="green" :width="3"></vl-style-stroke>
            <vl-style-fill color="rgba(255,255,255,0.5)"></vl-style-fill>
          </vl-style-box>
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
import ContainerMixin from "./detail/ContainerMixin.js";
import ContentHeader from "./detail/ContentHeader";
import Vue from "vue";
import VueLayers from "vuelayers";
import "vuelayers/lib/style.css"; // needs css-loader

Vue.use(VueLayers);

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
    this.loadFeatures().then(features => {
      this.features = features.map(Object.freeze);
      this.loading = false;
    });
  },
  methods: {
    // emulates external source
    loadMapFeatures() {
      const features = []
      const featureObject = {
        type: "Feature",
        id: null,
        geometry: null,
      }
      for (f in this.forests) {
        console.log(f, 'FOrest?')
        featureObject.id = f.id
        featureObject.geometry = f.geodata
        features.push(featureObject)
      }
      console.log(features)
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
