<template>
  <div id="app">
    <AmbientLightBg />
    <transition name="fade">
      <UploadImage
          v-if="showButton"
          @file-uploaded="handleFile"
      />
    </transition>
    <Menu :isVisible="showMenu" />
  </div>
</template>

<script>
import AmbientLightBg from "./components/AmbientLightBg.vue";
import UploadImage from "./components/UploadImage.vue";
import Menu from "./components/Menu.vue";

export default {
  name: "App",
  components: {
    AmbientLightBg,
    UploadImage,
    Menu
  },
  data() {
    return {
      showMenu: false, // 控制 Menu 显示
      showButton: true // 控制上传按钮的显示
    };
  },
  methods: {
    handleFile(file) {
      console.log("App.vue 收到文件:", file);
      this.showButton = false; // 隐藏上传按钮
      setTimeout(() => {
        this.showMenu = true; // 显示菜单
      }, 500); // 与 CSS 过渡时间相匹配
    }
  }
};
</script>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active 在某些版本中 */ {
  opacity: 0;
}
</style>
