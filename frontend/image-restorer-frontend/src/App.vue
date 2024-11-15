<template>
  <div class="flex h-full">
    <div>
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
    AmbientLightBg,
    test
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
