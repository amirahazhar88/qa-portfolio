import js from "@eslint/js";
import pluginVue from "eslint-plugin-vue";
import prettier from "eslint-config-prettier";
import globals from "globals";

export default [
  js.configs.recommended,
  ...pluginVue.configs["flat/essential"],
  prettier,
  {
    files: ["src/**/*.{js,vue}"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      globals: {
        ...globals.browser,
        ...globals.node
      }
    },
    rules: {
      "no-console": process.env.NODE_ENV === "production" ? "error" : "off",
      "no-debugger": process.env.NODE_ENV === "production" ? "error" : "off"
    }
  }
];
