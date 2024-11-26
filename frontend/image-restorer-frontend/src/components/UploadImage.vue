<template>
  <transition name="btn-fade">
    <div>
      <!-- 标题 -->
      <div class="title">
        <h1>
          Image <br />
          Restorer
        </h1>
      </div>
      <div v-if="!uploadComplete" class="upload-wrapper">
        <!-- 上传按钮区域 -->
        <div class="upload-btn-wrapper">
          <button
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
            <span class="text-style" :class="{ 'text-hide': isHovered }">
              上传图片
            </span>
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
      </div>
    </div>
  </transition>
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
.upload-wrapper {
  position: relative;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  overflow: hidden;
}

.title {
  position: fixed;
  top: -2%;
  left: 1%;
  color: #283c63;
  z-index: 10;
}

.title h1 {
  font-size: 440px;
  font-weight: 900;
  color: #fbe8d3cd;
  font-family: Cambria, Cochin, Georgia, Times, "Times New Roman", serif;
  line-height: 1.2;
}

.upload-btn-wrapper {
  position: fixed;
  top: 50%;
  left: 10%;
  z-index: 10;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fbe8d3;
  border: none;
  border-radius: 40px;
  box-shadow: 0px 6px 6px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
}

.btn:hover {
  background-color: #283c63;
}

.icon-style {
  width: 36px;
  height: 36px;
  color: #283c63;
  transition: all 0.3s ease;
}

.icon-hover {
  width: 72px;
  height: 72px;
  color: #ffffff;
}

.text-style {
  font-size: 28px;
  line-height: 42px;
  color: #283c63;
  transition: all 0.3s ease;
}

.text-hide {
  font-size: 0px;
  opacity: 0;
}

.hidden {
  display: none;
}

.hover-active {
  transform: translateX(-25px);
}

/* 过渡动画类 */
.btn-fade-enter-active,
.btn-fade-leave-active {
  transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;
}

.btn-fade-enter {
  opacity: 0;
  transform: scale(0.8);
}

.btn-fade-enter-to {
  opacity: 1;
  transform: scale(1);
}

.btn-fade-leave {
  opacity: 1;
  transform: scale(1);
}

.btn-fade-leave-to {
  opacity: 0;
  transform: scale(0.8);
}
</style>
