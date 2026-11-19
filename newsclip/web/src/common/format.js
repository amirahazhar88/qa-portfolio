import { format } from "date-fns";

// Template formatting helpers (the Vue 2 `date` and `error` filters).

export const formatDate = (date) => {
  const parsed = new Date(date);
  // A missing/invalid date (e.g. an article that failed to load) renders as
  // empty instead of throwing and aborting the whole component tree's mount.
  if (isNaN(parsed)) return "";
  return format(parsed, "MMMM d, yyyy");
};

export const formatError = (errorValue) => {
  return `${errorValue[0]}`;
};
