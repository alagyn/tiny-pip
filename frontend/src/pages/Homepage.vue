<script setup>
import axios from 'axios'
import { ref, onMounted, computed } from 'vue'

import SearchInput from "../components/SearchInput.vue"

const indexURL = ref("http://tiny-pip/api/index/")
const numPackages = ref(0)
const numReleases = ref(0)


onMounted(() =>
{

  axios.get("/api/metadata")
    .then(
      response =>
      {
        indexURL.value = response.data.indexURL
        numPackages.value = response.data.numPackages
        numReleases.value = response.data.numReleases
      }
    )
    .catch(error =>
    {
      console.log(error)
    })

})


</script>

<template>
  <div class="main-text">
    <b>
      Find, install, and publish Python packages<br>
      with tiny-pip
    </b>

    <div class="search-div container">
      <SearchInput />
    </div>
  </div>

  <hr>
  <div class="stats-div">
    <xxx class="stats-div-stat">{{ numPackages }} Packages</xxx>
    <xxx class="stats-div-stat">{{ numReleases }} Releases</xxx>
  </div>

  <hr>

  <div>
    <div class="info-div">
      Access your packages via
      <pre><code>{{ indexURL }}</code></pre>

      Example .pypirc
      <pre><code>[distutils]
  index-servers =
    pypi
    tiny-pip

[tiny-pip]
  repository = {{ indexURL }}
</code></pre>
    </div>
  </div>

</template>

<style lang="scss">
@import "../assets/tinypip.scss";


.main-text {
  text-align: center;
  font-size: xx-large;
  color: $blue;
  //background-color: $secondary-color;
  //padding: 20px 20px;
  //border-top: 1px solid #d29a00;
}

.search-div {
  text-align: center;
  font-size: medium;
  margin: 30px;
  margin-top: 50px;
  padding-bottom: 50px;
}

.stats-div {
  text-align: center;
}

.stats-div-stat {
  display: inline-block;
  box-sizing: border-box;
  padding: 20px 20px;
  font-size: 1.2rem;
  margin: 0;
}

.info-div {
  //margin: 0px 50px;
  //width: 50%;
}
</style>