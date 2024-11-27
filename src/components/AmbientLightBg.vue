<template>
  <div class="fixed w-screen h-screen">
    <div
      id="box"
      class="absolute items-center justify-center w-screen-2x h-screen-2x bg-gray-100 overflow-hidden"
    ></div>
  </div>
</template>

<script>
import { onMounted } from "vue";

export default {
  name: "Bg",
  mounted() {
    const colors = this.$attrs.colors || [
      "#283c63",
      "#283c63",
      "#928a97",
      "#f85f73",
      "#fbe8d3",
    ];
    let colorbg = new Color4Bg.AmbientLightBg({
      dom: "box",
      colors: colors,
      loop: true,
      seed: Math.floor(Math.random() * 10000),
    });
  },
};
</script>

<style scoped>
.w-screen-2x {
  width: 200vw;
}

.h-screen-2x {
  height: 200vh;
}
</style>
