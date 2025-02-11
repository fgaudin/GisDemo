<script setup lang="ts">
import Map from '@/components/Map.vue'
import Observations from '@/components/Observations.vue'
import axios from 'axios'
import { onMounted, ref } from 'vue'
import 'leaflet/dist/leaflet.css'
import AddObservation from '@/components/AddObservation.vue'

const observations = ref([])

onMounted(async () => {
  try {
    const response = await axios.get('/api/observations/')
    observations.value = await response.data
  } catch (error) {
    console.error(error)
  }
})
</script>

<template>
  <main class="container mx-auto">
    <div
      class="flex w-full bg-green-950 text-white h-24 mb-4 py-15 content-center px-center items-center justify-center rounded-b-lg"
    >
      <div><img src="@/assets/logo.png" alt="Vogel" class="h-20 invert" /></div>
      <div class="font-bold text-center text-4xl">Vögel</div>
    </div>
    <Map :observations="observations"></Map>
    <AddObservation></AddObservation>
    <Observations :observations="observations"></Observations>
  </main>
</template>
