import JwtService from "@/common/jwt.service";
import { API_URL } from "@/common/config";

// Thin fetch wrapper. Resolves with `{ data }` and rejects with an error
// carrying `response: { status, data }` for HTTP errors (no `response` for
// network failures), which is the shape extractErrors() consumes.
async function request(method, path, body) {
  const headers = { Accept: "application/json" };
  const token = JwtService.getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  const options = { method, headers };
  if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`${API_URL}/${path}`, options);

  // 204s and malformed payloads both yield null data rather than throwing.
  let data;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    const error = new Error(`[RWV] API ${method} ${path} ${response.status}`);
    error.response = { status: response.status, data: data || {} };
    throw error;
  }
  return { data };
}

const ApiService = {
  query(resource, config) {
    const params = (config && config.params) || {};
    const search = new URLSearchParams(params).toString();
    return request("GET", search ? `${resource}?${search}` : resource);
  },

  get(resource, slug = "") {
    const path = slug ? `${resource}/${slug}` : resource;
    return request("GET", path);
  },

  post(resource, params) {
    return request("POST", resource, params);
  },

  update(resource, slug, params) {
    return request("PUT", `${resource}/${slug}`, params);
  },

  put(resource, params) {
    return request("PUT", resource, params);
  },

  delete(resource) {
    return request("DELETE", resource);
  }
};

export default ApiService;

export const TagsService = {
  get() {
    return ApiService.get("tags");
  }
};

export const ArticlesService = {
  query(type, params) {
    return ApiService.query("articles" + (type === "feed" ? "/feed" : ""), {
      params: params
    });
  },
  get(slug) {
    return ApiService.get("articles", slug);
  },
  create(params) {
    return ApiService.post("articles", { article: params });
  },
  update(slug, params) {
    return ApiService.update("articles", slug, { article: params });
  },
  destroy(slug) {
    return ApiService.delete(`articles/${slug}`);
  }
};

export const CommentsService = {
  get(slug) {
    if (typeof slug !== "string") {
      throw new Error(
        "[RWV] CommentsService.get() article slug required to fetch comments"
      );
    }
    return ApiService.get("articles", `${slug}/comments`);
  },

  post(slug, payload) {
    return ApiService.post(`articles/${slug}/comments`, {
      comment: { body: payload }
    });
  },

  destroy(slug, commentId) {
    return ApiService.delete(`articles/${slug}/comments/${commentId}`);
  }
};

export const FavoriteService = {
  add(slug) {
    return ApiService.post(`articles/${slug}/favorite`);
  },
  remove(slug) {
    return ApiService.delete(`articles/${slug}/favorite`);
  }
};
