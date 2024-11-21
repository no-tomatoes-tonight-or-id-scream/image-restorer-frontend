<template>
  <div id="box" class="absolute  items-center justify-center w-full h-full bg-gray-100  overflow-hidden">

  </div>
</template>

<script>
import { onMounted } from 'vue';

export default {
  name: 'AmbientLightBg',
  mounted() {
    let colorbg = new Color4Bg.AmbientLightBg({
    dom: "box",
    colors: ["#f3f4f6"],
    loop: true,
      seed:100
    })

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
