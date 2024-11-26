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

    <div id="process" class="absolute top-[20%] left-[7%] w-1/3 z-10 m-4">
      <transition name="menu-fade">
        <Menu
            :isVisible="showMenu"
            :uploadedFile="uploadedFile"
            :baseUrl="baseUrl"
            @pics-upload="menu2Image"
            @menuDone="menuDone"
        />
      </transition>
    </div>

    <!-- 返回上传按钮 -->
    <div class="absolute top-[80%] left-[8%]">
      <backToUpload :canBack="showBackAndDownload" />
    </div>

    <div class="absolute top-[80%] left-[26%]">
      <DownloadButton
          :canDownload="showBackAndDownload"
          @DownloadRequest="DownloadTheResult"
      />
    </div>
  </div>
</template>


<script>
import AestheticFluidBg from "@/components/AestheticFluidBg.vue";
import ImageComparison from "@/components/ImageComparison.vue";
import Menu from "@/components/Menu.vue";
import backToUpload from "@/components/backToUpload.vue";
import DownloadButton from "@/components/DownLoadButton.vue";

export default {
  name: "ImageProcessing",
  components: {
    DownloadButton,
    AestheticFluidBg,
    ImageComparison,
    Menu,
    backToUpload,
  },
  data() {
    return {
      showMenu: true,
      uploadedFile: null, // 从路由获取传递的文件
      dirtyImagePath: null,
      cleanImagePath: null, // 处理后的图片地址
      baseUrl: "https://img-api.jrhim.com/",
      showBackAndDownload: false,
    };
  },
  mounted() {
    // 从路由中获取传递的文件
    // this.uploadedFile = localStorage.getItem("uploadedFile");
    this.uploadedFile = this.dirtyImagePath = localStorage.getItem("uploadedFile");
    console.log(this.uploadedFile); // 验证是否接收到
  },
  methods: {
    menu2Image(cleanImagePath) {
      this.cleanImagePath = cleanImagePath;
    },
    menuDone() {
      //this.showMenu = false;
      //this.showBack = true;
      this.showBackAndDownload = true;
      //console.log("showBack 设置为:", this.showBack);
      console.log("showMenu", this.showMenu);
    },
    DownloadTheResult() {
      console.log("下载处理后的图片");
      const link = document.createElement("a");
      link.href = this.cleanImagePath;
      link.download = "cleanImage.png";
      link.click();

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
