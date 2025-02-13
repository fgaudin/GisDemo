<script setup lang="ts">
import L from 'leaflet'
import { onMounted } from 'vue'

const props = defineProps<{
  id: number
  latitude: string
  longitude: string
}>()

onMounted(() => {
  const map = L.map('map-' + props.id).setView(
    [parseFloat(props.latitude), parseFloat(props.longitude)],
    13,
  )
  const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map)
  L.marker([parseFloat(props.latitude), parseFloat(props.longitude)]).addTo(map)
})
</script>

<template>
  <section>
    <div class="h-64 rounded" :id="'map-' + id"></div>
  </section>
</template>
