<script setup lang="ts">

import axios, { type AxiosResponse } from 'axios'
import { ref, onMounted, computed } from 'vue'

const indexURL = ref("http://tiny-pip:8000")
const numPackages = ref(0)
const numReleases = ref(0)

onMounted(() => {

    axios.get("/api/metadata")
        .then(
            response => {
                console.log(response)
                indexURL.value = response.data.indexURL
                numPackages.value = response.data.numPackages
                numReleases.value = response.data.numReleases
            }
        )
        .catch(error => {
            console.log(error)
        })

})

</script>

<template>
    <main>
        <br>
        <div>
            Index URL: {{ indexURL }}
        </div>

        <div class="container-sm search-div">
            <form>
                <input type="search" class="form-control" placeholder="Search Packages"
                    style="width: min-content; display: inline-block;" />
            </form>
        </div>

        <div class="stats-div">
            <p class="stats-div-stat">{{ numPackages }} Packages</p>
            <p class="stats-div-stat">{{ numReleases }} Releases</p>
        </div>

    </main>
</template>

<style lang="scss">
@import "../assets/tinypip.scss";

.stats-div {
    text-align: center;
    display: block;
    background-color: $secondary-color;
    color: black;
    padding: 0px;
}

.stats-div-stat {
    display: inline-block;
    box-sizing: border-box;
    padding: 20px 20px;
    font-size: 1.2rem;
    margin: 0;
}

.search-div {
    margin: 30px;
}
</style>