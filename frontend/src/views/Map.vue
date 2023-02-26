<template lang="pug">
div  
  div(id="container")
    div(id="mapContainer")

</template>

<script>
import "leaflet/dist/leaflet.css";
import * as L from "leaflet";
import "leaflet.markercluster/dist/MarkerCluster.css";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";
import "leaflet.markercluster";
import axios from "axios";

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});
export default {
  name: "MensaMap",
  data() {
    return {
      center: [51.961563, 7.628202],
      mensa_data: null,
    };
  },

  methods: {
    setupLeafletMap: function () {
      const map = L.map("mapContainer").setView(this.center, 13);
      L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
      }).addTo(map);

      // Get all canteens and bistros
      axios
        .get("mensa/mensa_data")
        .then(
          (response) => (
            (this.mensa_data = response.data), this.displayMarker(map)
          )
        );
    },
    displayMarker: function (map) {
      var cluster = L.markerClusterGroup({
        spiderfyOnMaxZoom: false,
        disableClusteringAtZoom: 17,
      }).addTo(map);

      this.mensa_data.forEach((mensa) => {
        new L.circleMarker(new L.LatLng(mensa.lat, mensa.lon))
          .setStyle({
            color: this.calculateOpeningHour(mensa),
            stroke: true,
            fill: true,
            fillOpacity: 0.8,
          })
          .addTo(cluster)
          .bindPopup(mensa.name)
          .openPopup();
      });
    },
    calculateOpeningHour: function (mensa) {
      var startTimeString = mensa.startTime;
      var endtimeSring = mensa.endTime;

      var now = new Date();
      var nowDateTime = now.toISOString();
      var nowDate = nowDateTime.split("T")[0];
      var startTime = new Date(nowDate + "T" + startTimeString);
      var endTime = new Date(nowDate + "T" + endtimeSring);

      if (now >= startTime && now < endTime) {
        return "#43a047";
      } else {
        return "#ff8a65";
      }
    },
  },
  mounted() {
    this.setupLeafletMap();
  },
};
</script>
<style scoped>
#mapContainer {
  z-index: 1;
  top: 10pt;
  width: 100vw;
  height: 80vh;
}
</style>
