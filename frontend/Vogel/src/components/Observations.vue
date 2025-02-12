<script setup lang="ts">
import type IObservation from '@/types/Observation'
import ObservationCard from './ObservationCard.vue'
import { Button } from 'primevue'

import { ref } from 'vue'

defineProps<{
  observations: IObservation[]
  loadMoreActive: boolean
}>()

const emit = defineEmits(['loadMoreClick'])

const loadMore = () => {
  emit('loadMoreClick')
}
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 rounded">
    <ObservationCard
      v-for="observation in observations"
      :key="observation.id"
      :observation="observation"
    />
  </div>
  <div class="w-full flex justify-center mt-8">
    <Button @click="loadMore" v-if="loadMoreActive" class="font-bold py-2 px-4 rounded"
      >Mehr laden</Button
    >
  </div>
</template>
