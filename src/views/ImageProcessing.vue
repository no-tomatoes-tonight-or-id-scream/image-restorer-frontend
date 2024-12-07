<template>
  <div class="absolute w-screen h-screen z-0 overflow-hidden grid grid-cols-7">
    <AestheticFluidBg :uploadedFile="uploadedFile" />

    <!-- 左侧部分 -->
    <div class="relative col-span-3 flex justify-center items-center ">
      <transition name="menu-fade">
        <Menu
            :isVisible="showMenu"
            :uploadedFile="uploadedFile"
            :baseUrl="baseUrl"
            @pics-upload="menu2Image"
            @menuDone="menuDone"
            @isLoading="sendIsLoading"
            @DownloadRequest="DownloadTheResult"
        />
      </transition>
    </div>

    <!-- 右侧部分居中 -->
    <div class="relative col-span-4 flex justify-center items-center">
      <ImageComparison
          :dirtyImage="dirtyImagePath"
          :cleanImage="cleanImagePath"
          :isLoading="isLoading"
          class="w-full h-auto max-w-[90%]"
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
// read base url from .env file
const baseUrl = import.meta.env.VITE_APP_BASE_URL;
console.log("baseUrl:", baseUrl);

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
      uploadedFile: null,
      dirtyImagePath: null,
      cleanImagePath: null,
      baseUrl: baseUrl,
      showBackAndDownload: false,
      isLoading: false,
    };
  },
  mounted() {
    this.uploadedFile = this.dirtyImagePath = localStorage.getItem("uploadedFile");
    console.log("父组件测试：", this.uploadedFile);
  },
  methods: {
    menu2Image(cleanImagePath) {
      this.cleanImagePath = cleanImagePath;
    },
    menuDone() {
      this.showBackAndDownload = true;
      console.log("showMenu", this.showMenu);
    },
    DownloadTheResult() {
      console.log("下载处理后的图片");
      const link = document.createElement("a");
      link.href = this.cleanImagePath;
      link.download = "cleanImage.png";
      link.click();
    },
    sendIsLoading(data) {
      this.isLoading = { value: true };
      console.log("父组件触发：", data);
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
