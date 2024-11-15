<template>
  <div id="box" class="w-screen h-screen fixed top-0 left-0 -z-10"></div>
</template>

<script>
import { onMounted } from 'vue';

export default {
  name: 'Bg',
  mounted() {
    let colorbg = new Color4Bg.BlurGradientBg({
      dom: "box",
      colors: ["#FC8408","#EE340D","#CA2406","#46AFE0"],
      loop: true
    })
  }
};
</script>

<style scoped>

</style>
