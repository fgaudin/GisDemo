<script setup lang="ts">
import { computed, defineProps, ref } from 'vue'
import MiniMap from './MiniMap.vue'
import type IObservation from '@/types/Observation'

const props = defineProps<{
  observation: IObservation
}>()

const expanded = ref(false)

const toggleExpanded = () => {
  expanded.value = !expanded.value
}

const computedName = computed(() => {
  const name = props.observation.species.name
  const maxLength = 27
  return expanded.value || name.length < maxLength
    ? name
    : props.observation.species.name.substring(0, maxLength - 3).concat('...')
})

const computedDate = computed(() => {
  const parts = props.observation.date.split('-')
  return `${parts[2]}/${parts[1]}/${parts[0]}`
})
</script>

<template>
  <div>
    <div class="shadow-lg rounded-lg bg-gray-100 dark:bg-gray-800 p-4">
      <div class="flex">
        <div class="w-full">
          <h2 class="text-xl font-bold">
            <button @click="toggleExpanded" class="text-left">
              {{ computedName }}
            </button>
          </h2>
        </div>
        <div class="text-gray-500 dark:text-gray-300 float-right text-right w-52">
          {{ computedDate }} - x{{ observation.count }}
        </div>
      </div>
      <div v-if="expanded">
        <div v-if="observation.species.avatar_url" class="flex justify-center mt-8">
          <img :src="observation.species.avatar_url" class="rounded-full w-30 h-30" />
        </div>

        <MiniMap
          v-if="expanded"
          :id="observation.id"
          :latitude="observation.latitude"
          :longitude="observation.longitude"
          class="mt-8"
        ></MiniMap>
      </div>
    </div>
  </div>
</template>
