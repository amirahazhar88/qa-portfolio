<template>
  <div class="card">
    <div class="card-block">
      <p class="card-text">{{ comment.body }}</p>
    </div>
    <div class="card-footer">
      <a href="" class="comment-author">
        <img :src="authorImage" class="comment-author-img" />
      </a>
      <router-link
        class="comment-author"
        :to="{ name: 'profile', params: { username: comment.author.username } }"
      >
        {{ comment.author.username }}
      </router-link>
      <span class="date-posted">{{ formatDate(comment.createdAt) }}</span>
      <span v-if="isCurrentUser" class="mod-options">
        <i class="ion-trash-a" @click="destroy(slug, comment.id)"></i>
      </span>
    </div>
    <RwvListErrors v-if="hasErrors" :errors="errors" />
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/store/auth";
import { useArticleStore } from "@/store/article";
import { formatDate } from "@/common/format";
import RwvListErrors from "./ListErrors.vue";
import { extractErrors } from "@/common/errors";

const props = defineProps({
  slug: { type: String, required: true },
  comment: { type: Object, required: true }
});

defineOptions({ name: "RwvComment" });

const articleStore = useArticleStore();
const { currentUser } = storeToRefs(useAuthStore());

const errors = ref({});

const isCurrentUser = computed(() => {
  if (currentUser.value.username && props.comment.author.username) {
    return props.comment.author.username === currentUser.value.username;
  }
  return false;
});

const authorImage = computed(() =>
  props.comment.author && props.comment.author.image
    ? props.comment.author.image
    : "/default-avatar.svg"
);

const hasErrors = computed(() => Object.keys(errors.value).length > 0);

const destroy = (slug, commentId) => {
  articleStore
    .destroyComment({ slug, commentId })
    .then(() => {
      errors.value = {};
    })
    .catch((error) => {
      errors.value = extractErrors(error);
    });
};
</script>
