import { defineStore } from "pinia";
import ApiService from "@/common/api.service";
import { extractErrors } from "@/common/errors";

const PROFILE_FETCH_RETRIES = 2;
const PROFILE_FETCH_RETRY_DELAY = 400;

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export const useProfileStore = defineStore("profile", {
  state: () => ({
    errors: {},
    profile: {}
  }),
  actions: {
    async fetchProfile({ username }) {
      // Profiles can be briefly missing right after registration on an
      // eventually-consistent backend, so retry before declaring an error.
      for (let attempt = 0; ; attempt++) {
        try {
          const { data } = await ApiService.get("profiles", username);
          this.profile = data.profile;
          this.errors = {};
          return data;
        } catch (error) {
          if (attempt >= PROFILE_FETCH_RETRIES) {
            this.profile = {};
            this.errors = extractErrors(error);
            return;
          }
          await delay(PROFILE_FETCH_RETRY_DELAY);
        }
      }
    },
    async follow({ username }) {
      try {
        const { data } = await ApiService.post(`profiles/${username}/follow`);
        this.profile = data.profile;
        this.errors = {};
        return data;
      } catch {
        // Leave the profile as-is; the follow button simply stays unchanged.
      }
    },
    async unfollow({ username }) {
      try {
        const { data } = await ApiService.delete(`profiles/${username}/follow`);
        this.profile = data.profile;
        this.errors = {};
        return data;
      } catch {
        // Leave the profile as-is; the unfollow button simply stays unchanged.
      }
    }
  }
});
