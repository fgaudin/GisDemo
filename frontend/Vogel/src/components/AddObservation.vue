<script setup lang="ts">
import { onMounted, onUpdated, reactive, ref } from 'vue'
import AutoComplete, { type AutoCompleteCompleteEvent } from 'primevue/autocomplete'
import ColorPicker from 'primevue/colorpicker'
import axios from 'axios'
import type ISpecies from '@/types/Species'
import { Button, DatePicker, InputNumber } from 'primevue'
import L from 'leaflet'

const show = ref(false)

const showForm = () => {
  show.value = !show.value
}

const species = ref<any>([])
const selectedSpecies = ref<any>('')
const filteredSpecies = ref<any>([])
const date = ref(new Date())
const count = ref(1)
const latitude = ref(0)
const longitude = ref(0)

onMounted(async () => {
  try {
    const response = await axios.get('/api/species/')
    const result = await response.data
    for (let sp of result) {
      species.value.push(sp)
    }
  } catch (error) {
    console.error(error)
  }
})

let map: L.Map
let marker: L.Marker

onUpdated(() => {
  if (show.value === true) {
    if (map === undefined) {
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
      }

      map.on('click', onMapClick)
    }
  } else {
    if (map !== undefined) {
      map.remove()
    }
  }
})

function searchSpecies(e: any) {
  filteredSpecies.value = species.value.filter((sp) => {
    return sp.name.toLowerCase().includes(e.query.toLowerCase())
  })
}

const loading = ref(false)

function createObservation() {
  const payload = {
    species_id: selectedSpecies.value.id,
    date: date.value.toJSON(),
    count: count.value,
    latitude: latitude.value,
    longitude: longitude.value,
  }
  try {
    loading.value = true
    axios.post('/api/observations/', payload)
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="my-4">
    <div class="flex w-full items-center justify-center">
      <button
        @click="showForm"
        class="bg-green-800 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
      >
        Add observation
      </button>
    </div>

    <div v-if="show" class="grid-cols-2 md:grid-cols-2">
      <div id="map-selector" class="h-64 w-96"></div>
      <div id="form">
        <form>
          <div class="mb-5">
            <label
              for="species"
              class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >Species</label
            >
            <AutoComplete
              v-model="selectedSpecies"
              :suggestions="filteredSpecies"
              optionLabel="name"
              @complete="searchSpecies"
              class="w-full"
            />
          </div>
          <div class="mb-5">
            <label for="date" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >Date</label
            >
            <DatePicker id="datepicker-24h" v-model="date" showTime hourFormat="24" fluid />
          </div>

          <div class="mb-5">
            <label for="count" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >Count</label
            >
            <InputNumber v-model="count" inputId="integeronly" fluid />
          </div>

          <Button label="Submit" @click="createObservation" :loading="loading" />
        </form>
      </div>
    </div>
  </div>
</template>
