<template>
  <div class="absolute  w-full h-screen z-0">
    <AmbientLightBg /> <!-- 背景动效 -->
<!--    <TitlePage />-->
    <!-- 右边图片区域 -->
    <div class="absolute right-0 w-2/3 h-screen z-10" draggable="false" v-if="!showButton">
      <ImageComparison :dirtyImage="dirtyImagePath" :cleanImage="cleanImagePath" />
    </div>
  <div id="app">
    <!-- 上传按钮的过渡效果 -->
    <transition name="btn-fade" @after-leave="showMenu = true">
      <UploadImage v-if="showButton" @file-uploaded="handleFile" />
    </transition>
    <!-- 菜单的过渡效果 -->
    <transition name="menu-fade">
      <!-- showMenu 和 组件中的 isVisible 实现绑定-->
      <Menu :isVisible="showMenu" :uploadedFile="uploadedFile" :baseUrl="baseUrl" @pics-upload="menu2Image"/>
    </transition>
  </div>
  </div>
</template>


<script>
import Backdrop from "./components/Backdrop.vue";
import AmbientLightBg from './components/AmbientLightBg.vue';
import ImageComparison from "./components/ImageComparison.vue";
import UploadImage from "@/components/UploadImage.vue";
import Menu from "@/components/Menu.vue";
import TitlePage from "@/components/TitlePage.vue";

export default {
  name: 'App',
  components: {
    Backdrop,
    AmbientLightBg,
    ImageComparison,
    UploadImage,
    Menu,
    TitlePage,
  },
  data() {
    return {
      showMenu: false, // 控制菜单显示
      showButton: true, // 控制上传按钮显示
      uploadedFile: null,
      dirtyImagePath: null, //未处理的图片地址
      cleanImagePath: null, //处理过的图片地址
      baseUrl:"https://img-api.jrhim.com/",
    };
  },
  methods: {
    handleFile(file) {
      console.log("App.vue 收到文件:", file);
      this.uploadedFile = file;
      this.dirtyImagePath = URL.createObjectURL(file);
      this.showButton = false; // 隐藏上传按钮
      setTimeout(() => {
        this.showMenu = true; // 显示菜单
        console.log("showMenu 设置为 true:", this.showMenu);
      }, 500); // 与过渡效果匹配
    },
    menu2Image(cleanImagePath)
    {
      this.cleanImagePath = cleanImagePath;
    }
  },
};

</script>

<style scoped>
html, body {
  width: 100%;
  height: 100%;
  margin: 0;
}
/* 上传按钮的缩小淡出效果 */
.btn-fade-enter-active,
.btn-fade-leave-active {
  transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;
}
.btn-fade-leave-to {
  opacity: 0;
  transform: scale(0.1); /* 按钮缩小到 50% */
}

/* 菜单的放大淡入效果 */
.menu-fade-enter-active,
.menu-fade-leave-active {
  transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;
}

.menu-fade-enter {
  opacity: 0; /* 初始状态为透明 */
  transform: scale(0.2); /* 初始状态为缩小 */
}

.menu-fade-enter-to {
  opacity: 1; /* 结束时完全可见 */
  transform: scale(1); /* 结束时正常大小 */
}

.menu-fade-leave-to {
  opacity: 0;
  transform: scale(0.2); /* 离开时缩小 */
}
</style>
