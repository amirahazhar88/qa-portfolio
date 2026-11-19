import { createPinia } from "pinia";

// Exported as an instance so router guards and `beforeRouteEnter` hooks can
// obtain stores outside of component setup: `useAuthStore(pinia)`.
const pinia = createPinia();

export default pinia;
