<script setup lang="ts">
import { onMounted, onUpdated, reactive, ref } from 'vue'
import AutoComplete, { type AutoCompleteCompleteEvent } from 'primevue/autocomplete'
import ColorPicker from 'primevue/colorpicker'
import axios from 'axios'
import type ISpecies from '@/types/Species'
import { Button, DatePicker, InputNumber, Message } from 'primevue'

import AddMap from './AddMap.vue'

const show = ref(false)

const showForm = () => {
  show.value = !show.value
  console.log(show.value)
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

const trackMapClick = (coords: [number, number]) => {
  latitude.value = coords[0]
  longitude.value = coords[1]
}

function searchSpecies(e: any) {
  filteredSpecies.value = species.value.filter((sp) => {
    return sp.name.toLowerCase().includes(e.query.toLowerCase())
  })
}

const loading = ref(false)
const added = ref(false)
const addedMessageDelay = 3000

const createObservation = () => {
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
    added.value = true
    show.value = false

    setTimeout(() => {
      added.value = false
    }, addedMessageDelay + 500)
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="my-4 bg-gray-100 rounded p-4">
    <div class="flex w-full items-center justify-center">
      <Button @click="showForm" class="font-bold py-2 px-4 rounded">Beobachtung melden</Button>
    </div>

    <Message
      severity="success"
      icon="pi pi-check"
      :life="addedMessageDelay"
      v-if="added"
      class="w-1/2 mx-auto my-8"
      >Beobachtung erfolgreich hinzugefügt</Message
    >

    <form @submit.prevent="createObservation">
      <div v-if="show" class="flex flex-col items-center mt-8">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-10 mx-auto">
          <AddMap class="h-64 w-96 rounded shadow-lg" @click="trackMapClick"></AddMap>
          <div id="form">
            <div class="mb-5">
              <label
                for="species"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Spezies</label
              >
              <AutoComplete
                v-model="selectedSpecies"
                :suggestions="filteredSpecies"
                optionLabel="name"
                @complete="searchSpecies"
                class="w-full"
                fluid
              />
            </div>
            <div class="mb-5">
              <label for="date" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Datum</label
              >
              <DatePicker v-model="date" fluid />
            </div>

            <div class="mb-5">
              <label
                for="count"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Zahl</label
              >
              <InputNumber v-model="count" inputId="integeronly" fluid />
            </div>
          </div>
        </div>
        <Button type="submit" label="Einreichen" :loading="loading" class="mx-auto" />
      </div>
    </form>
  </div>
</template>
