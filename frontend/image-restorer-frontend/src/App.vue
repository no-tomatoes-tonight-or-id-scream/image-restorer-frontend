<template>
  <div class="flex h-full">
    <div class="p-6 w-full h-full bg-white relative">
      <UploadImage />
      <AmbientLightBg />
    </div>
  </div>
</template>

<script>
import UploadImage from './components/UploadImage.vue';
import AmbientLightBg from './components/AmbientLightBg.vue';

export default {
  name: 'App',
  components: {
    UploadImage,
    AmbientLightBg
  }
};
</script>

<style>
html, body {
  width: 100%;
  height: 100%;
}
</style>
