<template>
  <div class="auth-page">
    <div class="container page">
      <div class="row">
        <div class="col-md-6 offset-md-3 col-xs-12">
          <h1 class="text-xs-center">Sign up</h1>
          <p class="text-xs-center">
            <router-link :to="{ name: 'login' }">
              Have an account?
            </router-link>
          </p>
          <ul v-if="errors" class="error-messages">
            <li v-for="(v, k) in errors" :key="k">
              {{ k }} {{ formatError(v) }}
            </li>
          </ul>
          <form @submit.prevent="onSubmit">
            <fieldset class="form-group">
              <input
                class="form-control form-control-lg"
                type="text"
                name="username"
                v-model="username"
                placeholder="Username"
              />
            </fieldset>
            <fieldset class="form-group">
              <input
                class="form-control form-control-lg"
                type="text"
                name="email"
                v-model="email"
                placeholder="Email"
              />
            </fieldset>
            <fieldset class="form-group">
              <input
                class="form-control form-control-lg"
                type="password"
                name="password"
                v-model="password"
                placeholder="Password"
              />
            </fieldset>
            <button type="submit" class="btn btn-lg btn-primary pull-xs-right">
              Sign up
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { storeToRefs } from "pinia";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";
import { formatError } from "@/common/format";

defineOptions({ name: "RwvRegister" });

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const { errors } = storeToRefs(authStore);

const username = ref("");
const email = ref("");
const password = ref("");

const postAuthRoute = computed(() => {
  const redirect = route.query.redirect;
  // Only allow same-app paths to avoid open redirects.
  if (typeof redirect === "string" && redirect.startsWith("/")) {
    return redirect;
  }
  return { name: "home" };
});

const onSubmit = () => {
  authStore
    .register({
      email: email.value,
      password: password.value,
      username: username.value
    })
    .then(() => router.push(postAuthRoute.value))
    .catch(() => {});
};
</script>
