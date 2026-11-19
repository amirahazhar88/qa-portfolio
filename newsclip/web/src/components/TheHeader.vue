<template>
  <nav class="navbar navbar-light">
    <div class="container">
      <router-link class="navbar-brand" :to="{ name: 'home' }">
        newsclip
      </router-link>
      <ul v-if="!isAuthenticated" class="nav navbar-nav pull-xs-right">
        <li v-if="isUnavailable" class="nav-item">
          <span class="nav-link">Connecting&hellip;</span>
        </li>
        <li class="nav-item">
          <router-link
            class="nav-link"
            exact-active-class="active"
            :to="{ name: 'home' }"
          >
            Home
          </router-link>
        </li>
        <li class="nav-item">
          <router-link
            class="nav-link"
            exact-active-class="active"
            :to="{ name: 'login' }"
          >
            <i class="ion-compose"></i>Sign in
          </router-link>
        </li>
        <li class="nav-item">
          <router-link
            class="nav-link"
            exact-active-class="active"
            :to="{ name: 'register' }"
          >
            <i class="ion-compose"></i>Sign up
          </router-link>
        </li>
      </ul>
      <ul v-else class="nav navbar-nav pull-xs-right">
        <li class="nav-item">
          <router-link
            class="nav-link"
            exact-active-class="active"
            :to="{ name: 'home' }"
          >
            Home
          </router-link>
        </li>
        <li class="nav-item">
          <router-link
            class="nav-link"
            active-class="active"
            :to="{ name: 'editor-new' }"
          >
            <i class="ion-compose"></i>&nbsp;New Article
          </router-link>
        </li>
        <li class="nav-item">
          <router-link
            class="nav-link"
            exact-active-class="active"
            :to="{ name: 'settings' }"
          >
            <i class="ion-gear-a"></i>&nbsp;Settings
          </router-link>
        </li>
        <li class="nav-item" v-if="currentUser.username">
          <router-link
            class="nav-link"
            exact-active-class="active"
            :to="{
              name: 'profile',
              params: { username: currentUser.username }
            }"
          >
            <img :src="userPicSrc" class="user-pic" />
            {{ currentUser.username }}
          </router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/store/auth";

const { currentUser, isAuthenticated, authStatus } =
  storeToRefs(useAuthStore());

const isUnavailable = computed(() => authStatus.value === "unavailable");

const userPicSrc = computed(() =>
  currentUser.value && currentUser.value.image
    ? currentUser.value.image
    : "/default-avatar.svg"
);
</script>
