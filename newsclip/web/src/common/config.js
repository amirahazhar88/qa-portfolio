// Override with a VITE_API_URL env var (e.g. in .env.local or the shell)
// to point the app at another RealWorld backend.
export const API_URL =
  import.meta.env.VITE_API_URL || "https://api.realworld.show/api";
export default API_URL;
