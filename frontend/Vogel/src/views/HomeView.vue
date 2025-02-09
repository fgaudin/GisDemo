<script setup lang="ts">
import Map from '@/components/Map.vue'
import Observations from '@/components/Observations.vue'
import axios from 'axios'
import { onMounted, ref } from 'vue'
import 'leaflet/dist/leaflet.css'

const observations = ref([])

onMounted(async () => {
  try {
    const response = await axios.get('/api/observations')
    observations.value = await response.data
  } catch (error) {
    console.error(error)
  }
})
</script>

<template>
  <main class="container mx-auto p-4">
    <div>Logo</div>
    <Map :observations="observations"></Map>
    <div>
      <button>Add observation</button>
    </div>
    <Observations :observations="observations"></Observations>
  </main>
</template>
