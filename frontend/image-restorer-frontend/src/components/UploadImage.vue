<template>
  <div class="upload-btn-wrapper">
    <!-- 上传按钮 -->
    <button
        v-if="!uploadComplete"
        class="btn btn-lg btn-outline w-[360px] h-[80px] text-2xl font-bold shadow-md transition-all duration-300"
        :class="{ 'hover:translate-x-[-25px]': isHovered }"
        @mouseenter="handleMouseEnter"
        @mouseleave="handleMouseLeave"
        @click="triggerFileInput"
    >
      上传图片
    </button>
    <!-- 隐藏的文件输入框，通过ref访问 -->
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
export default {
  name: "UploadImage",
  data() {
    return {
      isHovered: false, // 鼠标悬停状态
      uploadComplete: false, // 上传完成状态
    };
  },
  methods: {
    handleMouseEnter() {
      this.isHovered = true; // 鼠标进入时设置悬停状态
    },
    handleMouseLeave() {
      this.isHovered = false; // 鼠标离开时取消悬停状态
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
      // 触发隐藏的文件选择框
      this.$refs.fileInput.click();
    },
  },
};
</script>

<style>
.upload-btn-wrapper {
  position: fixed;
  top: 50%;
  left: 10%;
  transform: translateY(-50%);
  z-index: 10;
}
</style>
