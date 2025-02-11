<script setup lang="ts">
import { onMounted, onUpdated, ref } from 'vue'
import L from 'leaflet'
import type IObservation from '@/types/Observation'
import 'leaflet/dist/leaflet.css'
import '@geoman-io/leaflet-geoman-free'
import '@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css'

const props = defineProps<{
  observations: IObservation[]
}>()

const emit = defineEmits(['regionSelected'])

const wiesbaden = [50.0782, 8.2398]
let map: L.Map
const selection = ref<any>()

onMounted(() => {
  map = L.map('map-main', { pmIgnore: false }).setView([wiesbaden[0], wiesbaden[1]], 6)
  const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map)

  map.pm.addControls({
    position: 'topright',
    drawCircle: false,
    drawMarker: false,
    drawPolyline: false,
    drawRectangle: false,
    drawText: false,
    drawCircleMarker: false,
    rotateMode: false,
    cutPolygon: false,
    oneBlock: true,
  })

  map.on('pm:globaldrawmodetoggled', (e) => {
    if (e.enabled === true && selection.value !== undefined) {
      selection.value.remove()
    }
  })

  const regionSelected = (e: any) => {
    selection.value = e.layer
    emit('regionSelected', e.layer.toGeoJSON())
  }

  map.on('pm:create', (e) => {
    regionSelected(e)
    e.layer.on('pm:edit', regionSelected)
  })
  map.on('pm:remove', () => {
    selection.value = undefined
    emit('regionSelected', null)
  })
})

onUpdated(() => {
  for (let obs of props.observations) {
    L.marker([parseFloat(obs.latitude), parseFloat(obs.longitude)]).addTo(map)
  }
})
</script>

<template>
  <div class="h-96 w-full rounded" id="map-main"></div>
</template>
