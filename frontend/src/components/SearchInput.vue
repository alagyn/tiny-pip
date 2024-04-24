<script setup>
import { ref, onMounted, computed } from 'vue'
const searchValue = ref("")

function submitSearch(event)
{
  console.log(searchValue.value)
  window.location.href = "#/search"
}

</script>

<template>
  <form role="search">
    <input type="search" class="" placeholder="Search Packages" aria-label="Search" aria-describedby="search-addon"
      id="package-search" autocomplete="off" v-model="searchValue" />
    <button id="search-addon" type="submit" @click="submitSearch">
      <i class="bi-search"></i>
    </button>

  </form>
</template>