/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      keyframes: {
        textFlash: {
           "0%, 100%": { color: "#ffffff" }, // bright white
          "50%": { color: "#2563eb" },     // strong blue-600
        },
      },
      animation: {
        textFlash: "textFlash 1s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
