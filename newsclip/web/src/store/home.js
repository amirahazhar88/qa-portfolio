import { defineStore } from "pinia";
import { TagsService, ArticlesService } from "@/common/api.service";

export const useHomeStore = defineStore("home", {
  state: () => ({
    tags: [],
    articles: [],
    isLoading: true,
    articlesCount: 0
  }),
  actions: {
    async fetchArticles({ type, filters }) {
      this.isLoading = true;
      const { data } = await ArticlesService.query(type, filters);
      this.articles = data.articles;
      this.articlesCount = data.articlesCount;
      this.isLoading = false;
    },
    async fetchTags() {
      const { data } = await TagsService.get();
      this.tags = data.tags;
    },
    updateArticleInList(data) {
      this.articles = this.articles.map((article) => {
        if (article.slug !== data.slug) {
          return article;
        }
        // We could just return data, but it seems dangerous to
        // mix the results of different api calls, so we
        // protect ourselves by copying the information.
        article.favorited = data.favorited;
        article.favoritesCount = data.favoritesCount;
        return article;
      });
    }
  }
});
