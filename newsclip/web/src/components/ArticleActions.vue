<template>
  <!-- Used when user is also author -->
  <span v-if="canModify">
    <router-link class="btn btn-sm btn-outline-secondary" :to="editArticleLink">
      <i class="ion-edit"></i> <span>&nbsp;Edit Article</span>
    </router-link>
    <span>&nbsp;&nbsp;</span>
    <button class="btn btn-outline-danger btn-sm" @click="deleteArticle">
      <i class="ion-trash-a"></i> <span>&nbsp;Delete Article</span>
    </button>
  </span>
  <!-- Used in ArticleView when not author -->
  <span v-else>
    <button class="btn btn-sm btn-outline-secondary" @click="toggleFollow">
      <i class="ion-plus-round"></i> <span>&nbsp;</span>
      <span v-text="followUserLabel" />
    </button>
    <span>&nbsp;&nbsp;</span>
    <button
      class="btn btn-sm"
      @click="toggleFavorite"
      :class="toggleFavoriteButtonClasses"
    >
      <i class="ion-heart"></i> <span>&nbsp;</span>
      <span v-text="favoriteArticleLabel" /> <span>&nbsp;</span>
      <span class="counter" v-text="favoriteCounter" />
    </button>
  </span>
</template>

<script setup>
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";
import { useArticleStore } from "@/store/article";
import { useProfileStore } from "@/store/profile";

const props = defineProps({
  article: { type: Object, required: true },
  canModify: { type: Boolean, required: true }
});

const router = useRouter();
const articleStore = useArticleStore();
const profileStore = useProfileStore();
const { profile } = storeToRefs(profileStore);
const { isAuthenticated } = storeToRefs(useAuthStore());

const editArticleLink = computed(() => ({
  name: "article-edit",
  params: { slug: props.article.slug }
}));

const toggleFavoriteButtonClasses = computed(() => ({
  "btn-primary": props.article.favorited,
  "btn-outline-primary": !props.article.favorited
}));

const followUserLabel = computed(
  () =>
    `${profile.value.following ? "Unfollow" : "Follow"} ${
      props.article.author.username
    }`
);

const favoriteArticleLabel = computed(() =>
  props.article.favorited ? "Unfavorite Article" : "Favorite Article"
);

const favoriteCounter = computed(() => `(${props.article.favoritesCount})`);

const toggleFavorite = () => {
  if (!isAuthenticated.value) {
    router.push({ name: "login" });
    return;
  }
  if (props.article.favorited) {
    articleStore.removeFavorite(props.article.slug);
  } else {
    articleStore.addFavorite(props.article.slug);
  }
};

const toggleFollow = () => {
  if (!isAuthenticated.value) {
    router.push({ name: "login" });
    return;
  }
  if (props.article.following) {
    profileStore.unfollow({ username: profile.value.username });
  } else {
    profileStore.follow({ username: profile.value.username });
  }
};

const deleteArticle = async () => {
  try {
    await articleStore.deleteArticle(props.article.slug);
    router.push("/");
  } catch (err) {
    console.error(err);
  }
};
</script>
