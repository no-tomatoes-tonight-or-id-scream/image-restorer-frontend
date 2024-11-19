<template>
  <div class="upload-btn-wrapper">
    <!-- 上传按钮 -->
    <button
        v-if="!uploadComplete"
        class="btn btn-lg btn-outline w-[360px] h-[80px] text-2xl font-bold shadow-md flex items-center justify-center space-x-2 transition-all duration-300"
        :class="{ 'hover:translate-x-[-25px]': isHovered }"
        @mouseenter="handleMouseEnter"
        @mouseleave="handleMouseLeave"
        @click="triggerFileInput"
    >
      <UploadFilled class="text-3xl" /> <!-- 图标 -->
      <span class="text-style">上传图片</span> <!-- 文字 -->
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
        console.log("文件已上传:", file);
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
.upload-btn-wrapper {
  position: fixed;
  top: 50%;
  left: 10%;
  transform: translateY(-50%);
  z-index: 10;
}

.btn {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  background-color: #ffffff;
  border: none;
  border-radius: 40px; /* 圆角按钮 */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  color: #333; /* 文字颜色 */
}

.btn:hover {
  background-color: #D32F2F;
}

.btn .text-3xl {
  width: 36px;
  height: 36px;
  color: #666; /* 图标颜色 */
}

.space-x-2 > :not([hidden]) ~ :not([hidden]) {
  margin-left: 0.5rem; /* 图标与文字间距 */
}
.text-style {
  font-size: 28px; /* 文字大小 */
  line-height: 42px; /* 文字行高 */
  color: #333;
}

.hidden {
  display: none;
}
</style>
