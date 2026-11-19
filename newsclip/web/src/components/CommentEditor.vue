<template>
  <div>
    <RwvListErrors :errors="errors" />
    <form class="card comment-form" @submit.prevent="onSubmit(slug, comment)">
      <div class="card-block">
        <textarea
          class="form-control"
          v-model="comment"
          placeholder="Write a comment..."
          rows="3"
        >
        </textarea>
      </div>
      <div class="card-footer">
        <img :src="userImageSrc" class="comment-author-img" />
        <button class="btn btn-sm btn-primary">Post Comment</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { useArticleStore } from "@/store/article";
import RwvListErrors from "./ListErrors.vue";
import { extractErrors } from "@/common/errors";

const props = defineProps({
  slug: { type: String, required: true },
  content: { type: String, required: false },
  userImage: { type: String, required: false }
});

const articleStore = useArticleStore();

const comment = ref(props.content || null);
const errors = ref({});

const userImageSrc = computed(() => props.userImage || "/default-avatar.svg");

const onSubmit = (slug, body) => {
  articleStore
    .createComment({ slug, comment: body })
    .then(() => {
      comment.value = null;
      errors.value = {};
    })
    .catch((error) => {
      errors.value = extractErrors(error);
    });
};
</script>
