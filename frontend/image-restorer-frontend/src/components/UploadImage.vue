<template>
  <div class="upload-btn-wrapper">
    <!-- 上传按钮 -->
    <button
        class="upload-btn"
        v-if="!uploadComplete"
        @mouseenter="handleMouseEnter"
        @mouseleave="handleMouseLeave"
        @click="triggerFileInput"
    :style="buttonStyle"
    >
    上传图片
    </button>
    <!-- 隐藏的文件输入框，通过ref访问 -->
    <input
        ref="fileInput"
        type="file"
        @change="handleFileUpload"
        accept="image/*"
        style="display: none;"
    />
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
        opacity: this.uploadComplete ? 0 : 1,
        backgroundColor: this.isHovered ? "#f0f0f0" : "#ffffff", // 鼠标悬停时按钮变色
        transform: this.isHovered ? "translateX(-25px)" : "translateX(0)",
        transition: "all 0.3s ease",
      };
    },
  },
  methods: {
    handleMouseEnter() {
      this.isHovered = true; // 鼠标进入
      console.log("isHovered状态转为 true");
    },
    handleMouseLeave() {
      this.isHovered = false; // 鼠标离开
      console.log("isHovered状态转为 false");
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        console.log("文件已上传:", file);
        this.uploadComplete = true; // 设置上传完成状态
        this.$emit("file-uploaded", file); // 触发父组件事件
      }
    },
    triggerFileInput() {
      // 点击按钮时触发隐藏的文件输入框点击
      this.$refs.fileInput.click();
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
  padding: 0; /* 移除原有内边距，使用固定宽高 */
  width: 360px; /* 按钮宽度 */
  height: 80px; /* 按钮高度 */
  border-radius: 40px; /* 圆角值调整为一半高度 */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2); /* 阴影效果 */
  cursor: pointer;
  font-size: 28px; /* 字体大小 */
  line-height: 42px; /* 行高 */
  font-weight: bold; /* 增加字体粗细 */
  text-align: center; /* 居中对齐文本 */
  transition: all 0.3s ease; /* 确保移动和透明度的平滑过渡 */
}
</style>
