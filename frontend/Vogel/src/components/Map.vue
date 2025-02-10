<script setup lang="ts">
import { onMounted, onUpdated } from 'vue'
import L from 'leaflet'
import type IObservation from '@/types/Observation'

const props = defineProps<{
  observations: IObservation[]
}>()

const wiesbaden = [50.0782, 8.2398]

onUpdated(() => {
  const map = L.map('map-main').setView([wiesbaden[0], wiesbaden[1]], 6)
  const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map)

  for (let obs of props.observations) {
    L.marker([parseFloat(obs.latitude), parseFloat(obs.longitude)]).addTo(map)
  }
})
</script>

<template>
  <div class="h-96 w-full" id="map-main"></div>
</template>
