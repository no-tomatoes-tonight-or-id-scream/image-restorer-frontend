<template>
  <div class="absolute w-full h-full z-0">
    <AestheticFluidBg />
    <!-- 背景动效 -->
    <div class="absolute right-0 w-2/3 h-full z-10 m-4" draggable="false">
      <ImageComparison
          :dirtyImage="dirtyImagePath"
          :cleanImage="cleanImagePath"
      />
    </div>
    <div id="process">
      <transition name="menu-fade">
        <Menu
            :isVisible="showMenu"
            :uploadedFile="uploadedFile"
            :baseUrl="baseUrl"
            @pics-upload="menu2Image"
        />
      </transition>
    </div>
  </div>
</template>


<script>
import AestheticFluidBg from "@/components/AestheticFluidBg.vue";
import ImageComparison from "@/components/ImageComparison.vue";
import Menu from "@/components/Menu.vue";

export default {
  name: "ImageProcessing",
  components: {
    AestheticFluidBg,
    ImageComparison,
    Menu,
  },
  data() {
    return {
      showMenu: true,
      uploadedFile: null, // 从路由获取传递的文件
      dirtyImagePath: null,
      cleanImagePath: null, // 处理后的图片地址
      baseUrl: "https://img-api.jrhim.com/",
    };
  },
  setup() {
    console.log("ImageProcessing component loaded!");
  },
  created() {
    console.log("ImageProcessing component created!");
    this.dirtyImagePath = this.$route.query.uploadedFilePath;
  },
  methods: {
    menu2Image(cleanImagePath) {
      this.cleanImagePath = cleanImagePath;
    },
  },
};
</script>

<style scoped>
.menu-fade-enter-active,
.menu-fade-leave-active {
  transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;
}
.menu-fade-enter {
  opacity: 0;
  transform: scale(0.2);
}
.menu-fade-enter-to {
  opacity: 1;
  transform: scale(1);
}
.menu-fade-leave-to {
  opacity: 0;
  transform: scale(0.2);
}
</style>
