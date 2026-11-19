// newsclip theme (adapted from the RealWorld "Conduit Minimal CSS").
import "./assets/theme/styles.css";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import pinia from "./store";

import { useAuthStore } from "./store/auth";
import JwtService from "./common/jwt.service";

const app = createApp(App);
app.use(pinia);
app.use(router);

const auth = useAuthStore(pinia);

let authResolved = false;
router.beforeEach(async (to) => {
  await auth.checkAuth();
  authResolved = true;
  // Auth-gated routes are only decided once the auth check has resolved,
  // so an invalid token redirects away instead of showing a broken page.
  const needsAuth =
    (to.meta && to.meta.requiresAuth) ||
    (to.path === "/" && to.query.feed === "following");
  if (needsAuth && !auth.isAuthenticated) {
    return { path: "/login" };
  }
});

app.mount("#app");

window.__newsclip_debug__ = {
  getToken: function () {
    return JwtService.getToken();
  },
  getAuthState: function () {
    if (!authResolved) return "loading";
    return auth.authStatus;
  },
  getCurrentUser: function () {
    if (!auth.isAuthenticated) return null;
    const u = auth.user || {};
    if (!u.username) return null;
    return {
      username: u.username,
      email: u.email,
      bio: u.bio == null ? null : u.bio,
      image: u.image == null ? null : u.image,
      token: JwtService.getToken()
    };
  }
};
