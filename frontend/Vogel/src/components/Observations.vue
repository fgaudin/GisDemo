<script setup lang="ts">
import type IObservation from '@/types/Observation'
import ObservationCard from './ObservationCard.vue'

import { ref } from 'vue'

defineProps<{
  observations: IObservation[]
}>()
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12 bg-gray-100 p-4">
    <ObservationCard
      v-for="observation in observations"
      :key="observation.id"
      :observation="observation"
    />
  </div>
</template>
