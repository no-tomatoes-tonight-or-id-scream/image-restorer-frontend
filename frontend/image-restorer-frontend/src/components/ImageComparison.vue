<template>
  <div class="relative w-full h-96 overflow-hidden" ref="container">
    <!-- 左边的未处理图片部分，通过 clip-path 进行遮罩 -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden" :style="{ clipPath: `inset(0 0 0 ${leftWidth}%)` }">
      <img :src="leftImage" alt="Left Image" class="w-full h-full object-cover" />
    </div>

    <!-- 右边的处理图片部分，通过 clip-path 进行遮罩 -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden" :style="{ clipPath: `inset(0 ${100 - leftWidth}% 0 0)` }">
      <img :src="rightImage" alt="Right Image" class="w-full h-full object-cover" />
    </div>

    <!-- 滑动按钮 -->
    <div
        class="absolute top-0 bottom-0 w-[3px] bg-white cursor-ew-resize z-10"
        :style="{ left: leftWidth + '%' }"
        @mousedown="startDragging"
    >
      <span class="absolute top-1/2 -left-2.5 w-5 h-5 bg-gray-800 rounded-full transform -translate-y-1/2"></span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    leftImage: {
      type: String,
      required: true
    },
    rightImage: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      leftWidth: 50, // 初始化滑块位置为50%
      isDragging: false
    };
  },
  methods: {
    startDragging() {
      this.isDragging = true;
      window.addEventListener("mousemove", this.onDrag);
      window.addEventListener("mouseup", this.stopDragging);
    },
    stopDragging() {
      this.isDragging = false;
      window.removeEventListener("mousemove", this.onDrag);
      window.removeEventListener("mouseup", this.stopDragging);
    },
    onDrag(event) {
      if (!this.isDragging) return;
      const containerRect = this.$refs.container.getBoundingClientRect();
      const offsetX = event.clientX - containerRect.left;
      this.leftWidth = Math.min(100, Math.max(0, (offsetX / containerRect.width) * 100));
    }
  }
};
</script>

<style scoped>
/* 确保页面高度撑满 */
html, body, #app {
  height: 100%;
}
</style>
