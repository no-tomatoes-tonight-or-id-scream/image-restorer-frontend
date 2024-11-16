<template>
  <div class="upload-btn-wrapper">
    <button
        class="upload-btn"
        v-if="!uploadComplete"
        @mouseenter="onHover"
        @mouseleave="onLeave"
        :style="buttonStyle"
    >
      上传图片
    </button>
    <input type="file" @change="handleFileUpload" accept="image/*" />
  </div>
</template>

<script>
export default {
  name: "UploadImage",
  data() {
    return {
      isHovered: false, // 鼠标悬停状态
      uploadComplete: false, // 上传完成状态
    };
  },
  computed: {
    buttonStyle() {
      return {
        opacity: this.uploadComplete ? 0 : 1, // 上传完成时按钮渐变消失
        transition: "opacity 0.5s ease", // 添加平滑过渡
      };
    },
  },
  methods: {
    onHover() {
      this.isHovered = true; // 鼠标进入
    },
    onLeave() {
      this.isHovered = false; // 鼠标离开
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        console.log("文件已上传:", file);
        this.uploadComplete = true; // 设置上传完成状态
        this.$emit("file-uploaded", file); // 触发父组件事件
      }
    },
  },
};
</script>

<style scoped>
.upload-btn-wrapper {
  position: fixed;
  top: 50%;
  left: 10%;
  transform: translateY(-50%);
  z-index: 10;
}

.upload-btn {
  background-color: #ffffff; /* 纯白色背景 */
  border: none; /* 去除边框 */
  padding: 15px 30px; /* 调整尺寸 */
  border-radius: 50px; /* 椭圆形 */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2); /* 阴影效果 */
  cursor: pointer;
  font-size: 16px;
  font-weight: bold; /* 增加字体粗细 */
  transition: opacity 0.5s ease; /* 确保按钮的平滑过渡 */
}

.upload-btn-wrapper input[type="file"] {
  position: absolute;
  top: 0;
  left: 0;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}
</style>
