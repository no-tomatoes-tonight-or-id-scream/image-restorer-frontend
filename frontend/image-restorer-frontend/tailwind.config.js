module.exports = {
  content: [
    "./index.html", // 指定 index.html
    "./src/**/*.{vue,js,ts,jsx,tsx}", // 指定 src 文件夹内的所有 .vue, .js, .ts, .jsx, 和 .tsx 文件
  ],
  theme: {
    extend: {}, // 可以在这里扩展自定义主题
  },
  plugins: [], // 可以在这里添加 Tailwind 插件
};
