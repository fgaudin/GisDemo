<script setup lang="ts">
import Map from '@/components/Map.vue'
import Observations from '@/components/Observations.vue'
import axios from 'axios'
import { onMounted, reactive, ref } from 'vue'
import 'leaflet/dist/leaflet.css'
import AddObservation from '@/components/AddObservation.vue'

const observations = ref(<any>[])
const limit = 200
let offset = 0

let currentUrl = '/api/observations/'
let currentRegion: any = null
const loadMoreActive = ref(true)

const loadAll = async (more = false) => {
  currentRegion = null
  currentUrl = '/api/observations/'

  if (!more) {
    offset = 0
    observations.value.length = 0
  } else {
    offset += limit
  }
  try {
    const response = await axios.get(currentUrl + '?limit=' + limit + '&offset=' + offset)
    const data = await response.data
    if (data.count > offset + limit) {
      loadMoreActive.value = true
    } else {
      loadMoreActive.value = false
    }
    const newData = observations.value.concat(data.items)
    observations.value = newData
  } catch (error) {
    console.error(error)
  }
}

const regionSelected = async (region: any, more = false) => {
  currentUrl = '/api/observations/filtered/'
  if (!more) {
    offset = 0
    observations.value.length = 0
  } else {
    offset += limit
  }
  if (region === null) {
    loadAll()
    return
  } else {
    currentRegion = region
  }
  try {
    const response = await axios.post(currentUrl + '?limit=' + limit + '&offset=' + offset, {
      region: region.geometry.coordinates[0],
    })
    const data = await response.data
    if (data.count > offset + limit) {
      loadMoreActive.value = true
    } else {
      loadMoreActive.value = false
    }
    const newData = observations.value.concat(data.items)
    observations.value = newData
  } catch (error) {
    console.error(error)
  }
}

const loadMore = () => {
  if (currentRegion) {
    regionSelected(currentRegion, true)
  } else {
    loadAll(true)
  }
}

onMounted(loadAll)
</script>

<template>
  <main class="container mx-auto">
    <div
      class="flex w-full bg-green-800 text-white h-24 mb-4 py-15 content-center px-center items-center justify-center rounded-b-lg"
    >
      <div><img src="@/assets/logo.png" alt="Vogel" class="h-20 invert" /></div>
      <div class="font-bold text-center text-4xl">Vögel</div>
    </div>
    <Map :observations="observations" @regionSelected="regionSelected"></Map>
    <AddObservation></AddObservation>
    <Observations
      :observations="observations"
      @loadMoreClick="loadMore"
      :loadMoreActive="loadMoreActive"
    ></Observations>
  </main>
</template>
