<script setup lang="ts">
import { onMounted, ref } from 'vue'
import L from 'leaflet'

let map: L.Map
let marker: L.Marker

const latitude = ref(0)
const longitude = ref(0)

const emit = defineEmits(['click'])

onMounted(() => {
  map = L.map('map-selector').setView([50.0782, 8.2398], 10)
  const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map)

  function onMapClick(e: any) {
    latitude.value = e.latlng.lat
    longitude.value = e.latlng.lng
    if (marker !== undefined) {
      map.removeLayer(marker)
    }
    marker = L.marker(e.latlng)
    marker.addTo(map)

    emit('click', [latitude.value, longitude.value])
  }

  map.on('click', onMapClick)
})
</script>

<template>
  <div id="map-selector"></div>
</template>
