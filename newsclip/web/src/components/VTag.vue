<template>
  <router-link :to="homeRoute" :class="className">{{ name }}</router-link>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  className: {
    type: String,
    default: "tag-pill tag-default"
  }
});

const homeRoute = computed(() => ({
  name: "home-tag",
  params: { tag: props.name }
}));
</script>
