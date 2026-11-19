import { defineStore } from "pinia";
import {
  ArticlesService,
  CommentsService,
  FavoriteService
} from "@/common/api.service";
import { useHomeStore } from "./home";

export const useArticleStore = defineStore("article", {
  state: () => ({
    article: {
      author: {},
      title: "",
      description: "",
      body: "",
      tagList: []
    },
    comments: []
  }),
  actions: {
    async fetchArticle(articleSlug) {
      const { data } = await ArticlesService.get(articleSlug);
      this.article = data.article;
      return data;
    },
    async fetchComments(articleSlug) {
      const { data } = await CommentsService.get(articleSlug);
      this.comments = data.comments;
      return data.comments;
    },
    async createComment({ slug, comment }) {
      const { data } = await CommentsService.post(slug, comment);
      if (data && data.comment) {
        this.comments = this.comments.concat([data.comment]);
      } else {
        await this.fetchComments(slug);
      }
    },
    async destroyComment({ slug, commentId }) {
      // Any 2XX from the server means the comment is gone; update local state
      // directly instead of refetching.
      await CommentsService.destroy(slug, commentId);
      this.comments = this.comments.filter((c) => c.id !== commentId);
    },
    async addFavorite(slug) {
      const { data } = await FavoriteService.add(slug);
      // Update list as well. This allows us to favorite an article in the Home view.
      useHomeStore().updateArticleInList(data.article);
      this.article = data.article;
    },
    async removeFavorite(slug) {
      const { data } = await FavoriteService.remove(slug);
      useHomeStore().updateArticleInList(data.article);
      this.article = data.article;
    },
    publishArticle() {
      const { author, ...rest } = this.article; return ArticlesService.create(rest);
    },
    editArticle() {
      const { title, description, body } = this.article; return ArticlesService.update(this.article.slug, { title, description, body });
    },
    deleteArticle(slug) {
      return ArticlesService.destroy(slug);
    },
    addTag(tag) {
      this.article.tagList = this.article.tagList.concat([tag]);
    },
    removeTag(tag) {
      this.article.tagList = this.article.tagList.filter((t) => t !== tag);
    }
  }
});
