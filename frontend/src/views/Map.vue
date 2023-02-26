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

      var cluster = L.markerClusterGroup({
        spiderfyOnMaxZoom: false,
        disableClusteringAtZoom: 17,
      }).addTo(map);

      new L.circleMarker(new L.LatLng(51.96836, 7.594853))
        .setStyle({
          color: "#43a047",
          stroke: true,
          fill: true,
          fillOpacity: 0.8,
        })
        .addTo(cluster);

      new L.circleMarker(new L.LatLng(51.975033, 7.602068))
        .setStyle({
          color: "#ff8a65",
          stroke: true,
          fill: true,
          fillOpacity: 0.8,
        })
        .addTo(cluster)
        .bindPopup("Mensa DaVinci")
        .openPopup();
      new L.circleMarker(new L.LatLng(51.963451, 7.594432)).addTo(cluster);
      new L.circleMarker(new L.LatLng(51.9507932, 7.6079902)).addTo(cluster);
      new L.circleMarker(new L.LatLng(51.962632, 7.625869)).addTo(cluster);
      new L.circleMarker(new L.LatLng(51.9622951, 7.6209285)).addTo(cluster);
      new L.circleMarker(new L.LatLng(51.95554, 7.616978)).addTo(cluster);
      new L.circleMarker(new L.LatLng(51.95559, 7.617199)).addTo(cluster);
      new L.circleMarker(new L.LatLng(51.965806, 7.600138)).addTo(cluster);
      new L.circleMarker(new L.LatLng(51.960372, 7.619707)).addTo(cluster);
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
