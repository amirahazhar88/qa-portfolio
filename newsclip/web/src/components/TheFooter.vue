<template>
  <footer>
    <div class="container">
      <router-link class="logo-font" :to="{ name: 'home', params: {} }">
        newsclip
      </router-link>
      <span class="attribution">
        newsclip &mdash; your daily news. Built on the RealWorld spec
        (MIT licensed).
      </span>
    </div>
  </footer>
</template>
