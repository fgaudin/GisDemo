<script setup lang="ts">
import type IObservation from '@/types/Observation'
import '@geoman-io/leaflet-geoman-free'
import '@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import { onMounted, onUpdated, ref } from 'vue'

const props = defineProps<{
  observations: IObservation[]
}>()

const emit = defineEmits(['regionSelected'])

const wiesbaden = [50.0782, 8.2398]
let map: L.Map
const selection = ref<any>()

let layerGroup = L.layerGroup()

// remove all the markers in one go

onMounted(() => {
  map = L.map('map-main', { pmIgnore: false }).setView([wiesbaden[0], wiesbaden[1]], 6)
  const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map)

  layerGroup.addTo(map)

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

  map.on('moveend', function () {
    if (selection.value !== undefined) {
      return
    }
    const bounds = map.getBounds()
    var poly = {
      type: 'Feature',
      geometry: {
        type: 'Polygon',
        coordinates: [
          [
            [bounds.getNorthWest().lng, bounds.getNorthWest().lat],
            [bounds.getNorthEast().lng, bounds.getNorthEast().lat],
            [bounds.getSouthEast().lng, bounds.getSouthEast().lat],
            [bounds.getSouthWest().lng, bounds.getSouthWest().lat],
            [bounds.getNorthWest().lng, bounds.getNorthWest().lat],
          ],
        ],
      },
    }
    emit('regionSelected', poly)
  })
})

onUpdated(() => {
  layerGroup.clearLayers()
  for (let obs of props.observations) {
    let img = ''
    if (obs.species.avatar_url) {
      img = `<img src="${obs.species.avatar_url}" class="rounded-full float-left w-12 h-12 mr-4"/>`
    }

    L.marker([parseFloat(obs.latitude), parseFloat(obs.longitude)])
      .bindPopup(
        `<div class="w-48 h-12">${img}<p><b>${obs.species.name}</b><br>${obs.date}<br>x${obs.count}</p></div>`,
      )
      .addTo(layerGroup)
  }
})
</script>

<template>
  <div class="h-96 w-full rounded" id="map-main"></div>
</template>
