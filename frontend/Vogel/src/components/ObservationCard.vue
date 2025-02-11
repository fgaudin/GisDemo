<script setup lang="ts">
import { defineProps, ref } from 'vue'
import MiniMap from './MiniMap.vue'
import type IObservation from '@/types/Observation'

const props = defineProps<{
  observation: IObservation
}>()

const expanded = ref(false)

const toggleExpanded = () => {
  expanded.value = !expanded.value
}
</script>

<template>
  <div>
    <div class="dark:bg-gray-700 shadow-lg rounded-lg p-4">
      <h2 class="text-xl font-bold">
        <a @click="toggleExpanded">{{ observation.species.name }}</a>
      </h2>
      <p class="text-gray-500">{{ observation.date }} - x{{ observation.count }}</p>
      <MiniMap
        v-if="expanded"
        :id="observation.id"
        :latitude="observation.latitude"
        :longitude="observation.longitude"
      ></MiniMap>
    </div>
  </div>
</template>
