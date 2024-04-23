<script setup lang="ts">

import axios, { type AxiosResponse } from 'axios'
import { ref, onMounted, computed } from 'vue'

const indexURL = ref("http://tiny-pip:8000")
const numPackages = ref(0)
const numReleases = ref(0)
const searchValue = ref("")

onMounted(() => {

  axios.get("/api/metadata")
    .then(
      response => {
        indexURL.value = response.data.indexURL
        numPackages.value = response.data.numPackages
        numReleases.value = response.data.numReleases
      }
    )
    .catch(error => {
      console.log(error)
    })

})

function submitSearch(event: Event) {
  console.log(searchValue.value)
  window.location.href = "#/search"
}

</script>

<template>
  <main>
    <div class="search-div">
      <div class="main-text">
        <b>
          Find, install, and publish Python packages<br>
          with tiny-pip

        </b>
      </div>
      <div class="container-sm mx-5 px-5">
        <form>
          <div class="input-group mb-4">
            <input type="search" class="form-control" placeholder="Search Packages" aria-label="Search"
              aria-describedby="search-addon" id="package-search" autocomplete="off" v-model="searchValue" />
            <div class="input-group-append">
              <button id="search-addon" type="submit" class="btn btn-primary" @click="submitSearch">
                <i class="bi-search"></i>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <div class="stats-div">
      <p class="stats-div-stat">{{ numPackages }} Packages</p>
      <p class="stats-div-stat">{{ numReleases }} Releases</p>
    </div>

    <div class="container-sm info-div">
      Access your packages via
      <pre><code>{{ indexURL }}</code></pre>
    </div>

  </main>
</template>

<style lang="scss">
@import "../assets/tinypip.scss";

.stats-div {
  text-align: center;
  display: block;
  background-color: $offwhite;
  color: black;
  padding: 0px;
  border-bottom: 1px solid #d3d3d3;
  border-top: 1px solid #d3d3d3;
  margin-bottom: 30px;
}

.stats-div-stat {
  display: inline-block;
  box-sizing: border-box;
  padding: 20px 20px;
  font-size: 1.2rem;
  margin: 0;
}

.search-div {
  //margin: 30px;
  text-align: center;
  padding-bottom: 50px;
  background-color: $secondary-color;
}

.search-box {
  width: 30%;
  display: inline-block;
  padding: 10px 5px;
  font-size: larger;
  border-radius: 5px;
  border-color: #d3d3d3;
}

.main-text {
  font-size: xx-large;
  color: $blue;
  padding: 20px 20px;
  border-top: 1px solid #d29a00;
}

.info-div {
  text-align: center;
  color: black;
}
</style>