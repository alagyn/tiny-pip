<script setup lang="ts">
const props = defineProps(['hasSearch'])
</script>

<template>
    <header>

    </header>

    <main>
        <nav class="navbar navbar-expand-lg px-5">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">
                    <img src="/tiny-pip-logo.png" alt="Logo" />
                    tiny-pip </a>
                <p v-if="hasSearch"> search.....</p>
                <p>Val: {{ hasSearch }}</p>
            </div>
        </nav>
    </main>
</template>

<style lang="scss">
@import "../assets/tinypip.scss";

.navbar {
    background-color: $primary-color;

}
</style>