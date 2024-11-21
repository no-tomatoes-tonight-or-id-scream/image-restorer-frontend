<template>
  <div class="relative w-full h-screen bg-gray-100 overflow-hidden">
    <AmbientLightBg /> <!-- 背景动效 -->

    <!-- 右边图片区域 -->
    <div class="absolute right-0 top-0 w-2/3 h-full" draggable="false">
      <ImageComparison leftImage="/images/preprocess_1.png" />
    </div>
  </div>
</template>


<script>
import Backdrop from "./components/Backdrop.vue";
import AmbientLightBg from './components/AmbientLightBg.vue';
import ImageComparison from "./components/ImageComparison.vue";

export default {
  name: 'App',
  components: {
    Backdrop,
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
