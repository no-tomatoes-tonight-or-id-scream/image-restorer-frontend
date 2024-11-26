<template>
  <div class="absolute w-full h-full z-0">
    <AestheticFluidBg />
    <!-- 背景动效 -->
    <div id="home">
      <transition name="btn-fade">
        <UploadImage v-if="showButton" @file-uploaded="navigateToProcessing" />
      </transition>
    </div>
  </div>
</template>

<script>
import AestheticFluidBg from "@/components/AestheticFluidBg.vue";
import UploadImage from "@/components/UploadImage.vue";

export default {
  name: "Home",
  components: {
    AestheticFluidBg,
    UploadImage,
  },
  data() {
    return {
      showButton: true, // 控制上传按钮显示
    };
  },
  methods: {
    navigateToProcessing(file) {
      localStorage.setItem("uploadedFile",URL.createObjectURL(file));
      this.$router.push({
        name: "ImageProcessing",
      });
      this.showButton = false; // 隐藏按钮触发过渡效果
    },
  },
};
</script>

<style scoped>
.btn-fade-enter-active,
.btn-fade-leave-active {
  transition: opacity 0.5s ease-in-out, transform 0.5s ease-in-out;
}
.btn-fade-leave-to {
  opacity: 0;
  transform: scale(0.1);
}
</style>
