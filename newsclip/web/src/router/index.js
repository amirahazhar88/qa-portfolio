import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      name: "home",
      path: "/",
      component: () => import("@/views/Home")
    },
    {
      name: "home-tag",
      path: "/tag/:tag",
      component: () => import("@/views/Home")
    },
    {
      name: "login",
      path: "/login",
      component: () => import("@/views/Login")
    },
    {
      name: "register",
      path: "/register",
      component: () => import("@/views/Register")
    },
    {
      name: "settings",
      path: "/settings",
      component: () => import("@/views/Settings"),
      meta: { requiresAuth: true }
    },
    {
      name: "profile",
      path: "/profile/:username",
      component: () => import("@/views/Profile")
    },
    {
      name: "profile-favorites",
      path: "/profile/:username/favorites",
      component: () => import("@/views/Profile")
    },
    {
      name: "article",
      path: "/article/:slug",
      component: () => import("@/views/Article"),
      props: true
    },
    {
      name: "editor-new",
      path: "/editor",
      component: () => import("@/views/ArticleEdit"),
      meta: { requiresAuth: true }
    },
    {
      name: "article-edit",
      path: "/editor/:slug",
      props: true,
      component: () => import("@/views/ArticleEdit"),
      meta: { requiresAuth: true }
    }
  ]
});

// Auth-gated redirects live in main.js, after the auth check has resolved.

export default router;
