<template>
  <div class="fixed w-screen h-screen">
    <div
      id="box"
      class="absolute items-center justify-center w-screen h-screen bg-gray-100 overflow-hidden"
    ></div>
  </div>
</template>

<script>
import { onBeforeUnmount } from "vue";
export default {
  name: "Bg",
  mounted() {
    const colors = this.$attrs.colors || [
      "#283c63",
      "#928a97",
      "#f85f73",
      "#f85f73",
      "#928a97",
    ];
    let colorbg = new Color4Bg.AestheticFluidBg({
      dom: "box",
      colors: colors,
      loop: true,
      seed: Math.floor(Math.random() * 10000),
    });

    const handleResize = () => {
      colorbg.destroy();
      colorbg = new Color4Bg.AestheticFluidBg({
        dom: "box",
        colors: colors,
        loop: true,
        seed: Math.floor(Math.random() * 10000),
      });
    };

    window.addEventListener("resize", handleResize);
    onBeforeUnmount(() => {
      window.removeEventListener("resize", handleResize); // 移除事件监听
      if (colorbg) {
        colorbg.destroy(); // 销毁背景资源
      }
    });
  },
};
</script>
