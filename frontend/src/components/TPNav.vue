<script setup lang="ts">
const props = defineProps(['hasSearch'])
</script>

<template>

  <nav class="navbar">
    <ul>
      <li><a href="#">
          <img src="/tiny-pip-logo.png" alt="Tiny-Pip Logo" />
        </a>
      </li>
      <li><strong>tiny-pip</strong></li>
      <li><a href="#/browse">Browse</a></li>
      <li v-if="hasSearch">Search...</li>
    </ul>
  </nav>

</template>

<style lang="scss">
@import "../assets/tinypip.scss";

.navbar {
  padding: 0px 100px;
}
</style>