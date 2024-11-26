<template>
  <div class="upload-btn-wrapper">
    <!-- 上传按钮 -->
    <button
      v-if="!uploadComplete"
      class="btn btn-lg btn-outline w-[360px] h-[80px] text-2xl font-bold shadow-md flex items-center justify-center space-x-2 transition-all duration-300"
      :class="{
        'hover-active': isHovered,
        'hover:translate-x-[-25px]': isHovered,
      }"
      @mouseenter="handleMouseEnter"
      @mouseleave="handleMouseLeave"
      @click="triggerFileInput"
    >
      <UploadFilled class="icon-style" :class="{ 'icon-hover': isHovered }" />
      <!-- 图标 -->
      <span class="text-style" :class="{ 'text-hide': isHovered }"
        >上传图片</span
      >
      <!-- 文字 -->
    </button>
    <!-- 隐藏的文件输入框 -->
    <input
      ref="fileInput"
      type="file"
      @change="handleFileUpload"
      accept="image/*"
      class="hidden"
    />
  </div>
</template>

<script>
import { UploadFilled } from "@element-plus/icons-vue"; // 引入图标

export default {
  name: "UploadImage",
  components: {
    UploadFilled, // 注册图标组件
  },
  data() {
    return {
      isHovered: false, // 鼠标悬停状态
      uploadComplete: false, // 上传完成状态
    };
  },
  methods: {
    handleMouseEnter() {
      this.isHovered = true; // 鼠标进入设置悬停状态
    },
    handleMouseLeave() {
      this.isHovered = false; // 鼠标离开取消悬停状态
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        console.log("文件已上传：", file);
        this.uploadComplete = true; // 设置上传完成状态
        this.$emit("file-uploaded", file); // 触发上传完成事件
      }
    },
    triggerFileInput() {
      // 点击按钮时触发隐藏的文件选择框
      this.$refs.fileInput.click();
    },
  },
};
</script>

<style scoped>
.title {
  position: fixed;
  color: #283c63;
  z-index: 10;
}
.title h1 {
  font-size: 440px;
  font-weight: 900;
  color: #fbe8d3cd;
  font-family:Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  line-height: 1.2;
}

.upload-btn-wrapper {
  position: fixed;
  top: 50%;
  left: 10%;
  /* transform: translateY(-50%); */
  z-index: 10;
}

.btn {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  background-color: #fbe8d3;
  border: none;
  border-radius: 40px; /* 圆角按钮 */
  box-shadow: 0px 6px 6px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  overflow: hidden; /* 防止动画溢出 */
  transition: all 0.3s ease; /* 整体动画效果 */
}

.btn:hover {
  background-color: #283c63;
}

.icon-style {
  width: 36px;
  height: 36px;
  color: #283c63; /* 图标颜色 */
  transition: all 0.3s ease; /* 动画过渡 */
}

.icon-hover {
  width: 72px; /* 鼠标悬停时图标放大 */
  height: 72px;
  color: #ffffff;
}

.text-style {
  font-size: 28px; /* 初始文字大小 */
  line-height: 42px; /* 行高 */
  color: #283c63;
  transition: all 0.3s ease; /* 动画过渡 */
}

.text-hide {
  font-size: 0px; /* 鼠标悬停时文字缩小消失 */
  opacity: 0; /* 文字逐渐隐藏 */
}

.hidden {
  display: none;
}

/* 鼠标悬停时按钮向左移动效果 */
.hover-active {
  transform: translateX(-25px); /* 按钮整体向左移动 */
}
</style>
