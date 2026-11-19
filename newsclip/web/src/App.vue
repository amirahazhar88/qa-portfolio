<template>
  <div id="app">
    <RwvHeader />
    <router-view></router-view>
    <RwvFooter />
  </div>
</template>

<script setup>
import RwvHeader from "@/components/TheHeader";
import RwvFooter from "@/components/TheFooter";
</script>

<style></style>
