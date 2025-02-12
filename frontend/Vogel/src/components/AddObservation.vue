<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import AutoComplete from 'primevue/autocomplete'
import axios from 'axios'
import { Button, DatePicker, InputNumber, Message } from 'primevue'
import { Form } from '@primevue/forms'
import Fieldset from 'primevue/fieldset'

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

const clearForm = () => {
  selectedSpecies.value = ''
  date.value = new Date()
  count.value = 1
  latitude.value = 0
  longitude.value = 0
}

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
  filteredSpecies.value = species.value.filter((sp: any) => {
    return sp.name.toLowerCase().includes(e.query.toLowerCase())
  })
}

const loading = ref(false)
const added = ref(false)
const failed = ref(false)
const addedMessageDelay = 3000
const errors = reactive({
  species: '',
  date: '',
  count: '',
  location: '',
})

const validateForm = () => {
  let valid = true
  if (!selectedSpecies.value) {
    errors.species = 'Bitte wählen Sie eine Spezies aus'
    valid = false
  } else {
    errors.species = ''
  }
  if (!date.value) {
    errors.date = 'Bitte wählen Sie ein Datum aus'
    valid = false
  } else {
    errors.date = ''
  }
  if (!count.value) {
    errors.count = 'Bitte geben Sie eine Anzahl ein'
    valid = false
  } else {
    errors.count = ''
  }
  if (!latitude.value || !longitude.value) {
    errors.location = 'Bitte wählen Sie einen Ort auf der Karte aus'
    valid = false
  } else {
    errors.location = ''
  }
  return valid
}

const createObservation = async () => {
  if (!validateForm()) {
    console.log(errors)
    return
  }

  const payload = {
    species_id: selectedSpecies.value.id,
    date: date.value.toISOString().split('T')[0],
    count: count.value,
    latitude: latitude.value,
    longitude: longitude.value,
  }
  try {
    loading.value = true
    const response = await axios.post('/api/observations/', payload)
    console.log(response.status)
    if (response.status !== 201) {
      failed.value = true
    } else {
      added.value = true
      clearForm()
    }
    show.value = false
  } catch (error) {
    console.log('error')
    failed.value = true
  } finally {
    loading.value = false
    setTimeout(() => {
      added.value = false
      failed.value = false
    }, addedMessageDelay + 500)
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
      icon="pi pi-check-circle"
      :life="addedMessageDelay"
      v-if="added"
      class="w-1/2 mx-auto my-8"
      >Beobachtung erfolgreich hinzugefügt</Message
    >
    <Message
      severity="error"
      icon="pi pi-times-circle"
      :life="addedMessageDelay"
      v-if="failed"
      class="w-1/2 mx-auto my-8"
      >Die Beobachtung konnte nicht gespeichert werden</Message
    >

    <form @submit.prevent="createObservation">
      <div v-if="show" class="flex flex-col items-center mt-8">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-10 mx-auto">
          <div>
            <AddMap class="h-64 w-96 rounded shadow-lg" @click="trackMapClick"></AddMap>
            <Message severity="error" v-if="errors.location">{{ errors.location }}</Message>
          </div>
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
                :invalid="!!errors.species"
                fluid
              />
              <Message severity="error" v-if="errors.species">{{ errors.species }}</Message>
            </div>
            <div class="mb-5">
              <label for="date" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Datum</label
              >
              <DatePicker v-model="date" dateFormat="dd/mm/yy" fluid :invalid="!!errors.date" />
              <Message severity="error" v-if="errors.date">{{ errors.date }}</Message>
            </div>

            <div class="mb-5">
              <label
                for="count"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Anzahl</label
              >
              <InputNumber v-model="count" inputId="integeronly" fluid :invalid="!!errors.count" />
              <Message severity="error" v-if="errors.count">{{ errors.count }}</Message>
            </div>
          </div>
        </div>
        <Button type="submit" label="Einreichen" :loading="loading" class="mx-auto" />
      </div>
    </form>
  </div>
</template>
