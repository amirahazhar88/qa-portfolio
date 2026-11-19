<template>
  <div class="article-page">
    <div class="banner">
      <div class="container">
        <h1>{{ article.title }}</h1>
        <RwvArticleMeta :article="article" :actions="true"></RwvArticleMeta>
      </div>
    </div>
    <div class="container page">
      <div class="row article-content">
        <div class="col-xs-12">
          <div v-html="parseMarkdown(article.body)"></div>
          <ul class="tag-list">
            <li v-for="(tag, index) of article.tagList" :key="tag + index">
              <RwvTag
                :name="tag"
                className="tag-default tag-pill tag-outline"
              ></RwvTag>
            </li>
          </ul>
        </div>
      </div>
      <hr />
      <div class="article-actions">
        <RwvArticleMeta :article="article" :actions="true"></RwvArticleMeta>
      </div>
      <div class="row">
        <div class="col-xs-12 col-md-8 offset-md-2">
          <RwvCommentEditor
            v-if="isAuthenticated"
            :slug="slug"
            :userImage="currentUser.image"
          >
          </RwvCommentEditor>
          <p v-else>
            <router-link
              :to="{ name: 'login', query: { redirect: route.fullPath } }"
            >
              Sign in
            </router-link>
            or
            <router-link
              :to="{ name: 'register', query: { redirect: route.fullPath } }"
            >
              sign up
            </router-link>
            to add comments on this article.
          </p>
          <RwvComment
            v-for="(comment, index) in comments"
            :slug="slug"
            :comment="comment"
            :key="index"
          >
          </RwvComment>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import pinia from "@/store";
import { useArticleStore } from "@/store/article";

// `beforeRouteEnter` runs before the component instance is created, so it
// has no composition-API equivalent and lives in this options block.
export default {
  name: "RwvArticle",
  async beforeRouteEnter(to) {
    const articleStore = useArticleStore(pinia);
    await Promise.all([
      articleStore.fetchArticle(to.params.slug).catch(() => null),
      articleStore.fetchComments(to.params.slug).catch(() => null)
    ]);
  }
};
</script>

<script setup>
import { storeToRefs } from "pinia";
import { useRoute } from "vue-router";
import { marked } from "marked";
import DOMPurify from "dompurify";
import { useAuthStore } from "@/store/auth";
import RwvArticleMeta from "@/components/ArticleMeta";
import RwvComment from "@/components/Comment";
import RwvCommentEditor from "@/components/CommentEditor";
import RwvTag from "@/components/VTag";

defineProps({
  slug: {
    type: String,
    required: true
  }
});

const route = useRoute();
const { article, comments } = storeToRefs(useArticleStore());
const { currentUser, isAuthenticated } = storeToRefs(useAuthStore());

const parseMarkdown = (content) => {
  // The body comes from the API and may contain attacker-controlled HTML.
  return DOMPurify.sanitize(marked.parse(content));
};
</script>
