<script setup lang="js">
import { ref, computed } from 'vue'

import TPNav from "./components/TPNav.vue"
import Homepage from "./pages/Homepage.vue"
import Search from "./pages/Search.vue"
import NotFound from "./pages/NotFound.vue"

const routes = {
  "/": Homepage,
  "/search": Search
}

const currentPath = ref(window.location.hash)

window.addEventListener("hashchange",
  () =>
  {
    currentPath.value = window.location.hash
  })

const currentView = computed(
  () =>
  {
    return routes[currentPath.value.slice(1) || '/'] || NotFound
  }
)

const navBarSearch = computed(
  () =>
  {
    console.log(currentPath.value)
    let x = currentPath.value != ''
    console.log(x)
    return x
  }
)


</script>

<template>
  <header>
    <TPNav :hasSearch="navBarSearch" />
  </header>
  <main>
    <component :is="currentView" />
  </main>
</template>
