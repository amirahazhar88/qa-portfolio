import { defineStore } from "pinia";
import ApiService from "@/common/api.service";
import JwtService from "@/common/jwt.service";
import { extractErrors } from "@/common/errors";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    errors: null,
    user: {},
    isAuthenticated: !!JwtService.getToken(),
    // 'authenticated' | 'unauthenticated' | 'unavailable'
    authStatus: JwtService.getToken() ? "authenticated" : "unauthenticated"
  }),
  getters: {
    currentUser: (state) => state.user
  },
  actions: {
    setAuth(user) {
      this.isAuthenticated = true;
      this.authStatus = "authenticated";
      this.user = user;
      this.errors = {};
      if (user.token) JwtService.saveToken(user.token);
    },
    setAuthUnavailable() {
      this.isAuthenticated = false;
      this.authStatus = "unavailable";
      this.user = {};
    },
    purgeAuth() {
      this.isAuthenticated = false;
      this.authStatus = "unauthenticated";
      this.user = {};
      this.errors = {};
      JwtService.destroyToken();
    },
    async login(credentials) {
      try {
        const { data } = await ApiService.post("users/login", {
          user: credentials
        });
        this.setAuth(data.user);
        return data;
      } catch (error) {
        this.errors = extractErrors(error);
        throw error;
      }
    },
    logout() {
      this.purgeAuth();
    },
    async register(credentials) {
      try {
        const { data } = await ApiService.post("users", { user: credentials });
        this.setAuth(data.user);
        return data;
      } catch (error) {
        this.errors = extractErrors(error);
        throw error;
      }
    },
    async checkAuth() {
      if (!JwtService.getToken()) {
        this.purgeAuth();
        return;
      }
      try {
        const { data } = await ApiService.get("user");
        if (data && data.user) {
          this.setAuth(data.user);
        } else {
          // 2XX without a parsable user payload (empty body, malformed
          // JSON): treat the server as unavailable but keep the token.
          this.setAuthUnavailable();
        }
      } catch (error) {
        const status = error && error.response && error.response.status;
        if (status >= 400 && status < 500) {
          // The token was rejected: clear it and show the logged-out UI.
          this.purgeAuth();
        } else {
          // 5XX or network failure: the token may still be valid, so keep
          // it and let the user browse in degraded mode.
          this.setAuthUnavailable();
        }
      }
    },
    async updateUser(payload) {
      const { email, username, password, image, bio } = payload;
      const user = {
        email,
        username,
        bio,
        image
      };
      if (password) {
        user.password = password;
      }

      const { data } = await ApiService.put("user", { user });
      this.setAuth(data.user);
      return data;
    }
  }
});
