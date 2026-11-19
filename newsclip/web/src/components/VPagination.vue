<template>
  <nav v-if="pages.length > 1">
    <ul class="pagination">
      <li
        v-for="page in pages"
        :data-test="`page-link-${page}`"
        :key="page"
        :class="paginationClass(page)"
      >
        <button
          type="button"
          class="page-link"
          @click.prevent="changePage(page)"
        >
          {{ page }}
        </button>
      </li>
    </ul>
  </nav>
</template>

<script setup>
const props = defineProps({
  pages: {
    type: Array,
    required: true
  },
  currentPage: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(["update:currentPage"]);

const changePage = (goToPage) => {
  if (goToPage === props.currentPage) return;
  emit("update:currentPage", goToPage);
};

const paginationClass = (page) => ({
  "page-item": true,
  active: props.currentPage === page
});
</script>
