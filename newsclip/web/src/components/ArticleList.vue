<template>
  <div>
    <div v-if="isLoading" class="article-preview">Loading articles...</div>
    <div v-else>
      <div v-if="articles.length === 0" class="article-preview">
        No articles are here... yet.
      </div>
      <RwvArticlePreview
        v-for="(article, index) in articles"
        :article="article"
        :key="article.slug + '-' + index"
      />
      <VPagination
        :pages="pages"
        :current-page="page"
        @update:currentPage="emitPage"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from "vue";
import { storeToRefs } from "pinia";
import { useHomeStore } from "@/store/home";
import RwvArticlePreview from "./VArticlePreview";
import VPagination from "./VPagination";

const props = defineProps({
  type: {
    type: String,
    required: false,
    default: "all"
  },
  author: {
    type: String,
    required: false
  },
  tag: {
    type: String,
    required: false
  },
  favorited: {
    type: String,
    required: false
  },
  itemsPerPage: {
    type: Number,
    required: false,
    default: 10
  },
  currentPage: {
    type: Number,
    required: false,
    default: 1
  }
});

const emit = defineEmits(["update:currentPage"]);

const homeStore = useHomeStore();
const { articlesCount, isLoading, articles } = storeToRefs(homeStore);

const page = computed(() => (props.currentPage > 0 ? props.currentPage : 1));

const listConfig = computed(() => {
  const filters = {
    offset: (page.value - 1) * props.itemsPerPage,
    limit: props.itemsPerPage
  };
  if (props.author) filters.author = props.author;
  if (props.tag) filters.tag = props.tag;
  if (props.favorited) filters.favorited = props.favorited;
  return { type: props.type, filters };
});

const pages = computed(() => {
  if (isLoading.value || articlesCount.value <= props.itemsPerPage) {
    return [];
  }
  return [
    ...Array(Math.ceil(articlesCount.value / props.itemsPerPage)).keys()
  ].map((e) => e + 1);
});

const fetchArticles = () => {
  // A failed load leaves the list in its loading state; the error-handling
  // contract only requires the app not to crash.
  homeStore.fetchArticles(listConfig.value).catch(() => {});
};

// Refetch whenever the page or any filter changes.
watch(listConfig, fetchArticles);
onMounted(fetchArticles);

const emitPage = (p) => emit("update:currentPage", p);
</script>
