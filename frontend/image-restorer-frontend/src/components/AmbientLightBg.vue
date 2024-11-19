<template>
  <div id="box" class="relative flex items-center justify-center w-full h-full bg-gray-100  overflow-hidden">

  </div>
</template>

<script>
import { onMounted } from 'vue';

export default {
  name: 'AmbientLightBg',
  mounted() {
    let colorbg = new Color4Bg.AmbientLightBg({
      dom: "box",
      colors: ["#F00911", "#F3AA00", "#F6EE0B", "#39E90D", "#195ED2", "#F00911"],
      seed: 1000,
      loop: true
    });
  }
};
</script>

<style scoped>
#box {
  position: relative;
  width: 100%;
  height: 100%;
}
</style>
