<script setup lang="ts">
import { onMounted } from 'vue';
import L from 'leaflet';

const props = defineProps<{
    id: number;
    lattitude: string;
    longitude: string;
}>();

onMounted(() => {
    const map = L.map('map-' + props.id).setView([parseFloat(props.lattitude), parseFloat(props.longitude)], 13);
    const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    L.marker([parseFloat(props.lattitude), parseFloat(props.longitude)]).addTo(map);
});
</script>

<template>
    <section>
        <div class="h-96" :id="'map-' +  id ">
        </div>
    </section>
</template>