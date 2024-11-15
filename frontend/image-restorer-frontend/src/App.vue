<template>
  <div class="flex h-full w-full">
    <!-- 左边的空白区域，占据屏幕的三分之一 -->
    <div class="w-1/3 h-full"></div>

    <!-- 右边的图片对比组件，占据屏幕的三分之二 -->
    <div class="w-2/3 h-full">
      <ImageComparison
          leftImage="/images/processed_1.png"
          rightImage="/images/preprocess_1.png"
      />
    </div>
  </div>
</template>

<script>
import UploadImage from './components/UploadImage.vue';
import AmbientLightBg from './components/AmbientLightBg.vue';
import ImageComparison from "./components/ImageComparison.vue";

export default {
  name: 'App',
  components: {
    UploadImage,
    AmbientLightBg,
    ImageComparison
  }
};
</script>

<style>
html, body {
  width: 100%;
  height: 100%;
  margin: 0;
}
</style>
