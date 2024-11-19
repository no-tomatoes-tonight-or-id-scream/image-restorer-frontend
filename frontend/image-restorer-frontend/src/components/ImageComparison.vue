<template>
  <div class="relative w-full h-screen overflow-hidden bg-black" ref="container">
    <!-- 左边的未处理图片部分，通过 clip-path 进行遮罩 -->
    <div
        class="absolute top-0 left-0 w-full h-full overflow-hidden"
        :style="{ clipPath: `inset(0 0 0 ${leftWidth}%)` }"
    >
      <img
          :src="leftImage"
          alt="Left Image"
          ref="leftImage"
          class="absolute inset-0 m-auto object-contain h-full"
      />
    </div>

    <!-- 右边的处理图片部分，通过 clip-path 进行遮罩 -->
    <div
        class="absolute top-0 left-0 w-full h-full overflow-hidden"
        :style="{ clipPath: `inset(0 ${100 - leftWidth}% 0 0)` }"
    >
      <img
          :src="rightImage"
          alt="Right Image"
          ref="rightImage"
          class="absolute inset-0 m-auto object-contain h-full"
      />
    </div>

    <!-- 滑动按钮 -->
    <div
        class="absolute top-0 bottom-0 w-[3px] bg-white cursor-ew-resize z-10"
        :style="{ left: leftWidth + '%' }"
        @mousedown="startDragging"
    >
      <span
          class="absolute top-1/2 -left-2.5 w-5 h-5 bg-gray-800 rounded-full transform -translate-y-1/2"
      ></span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    leftImage: {
      type: String,
      required: true,
    },
    rightImage: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      leftWidth: 50, // 初始化滑块位置为50%
      isDragging: false,
      containerBounds: null,
    };
  },
  mounted() {
    // 获取容器的边界信息
    this.updateContainerBounds();
    // 监听窗口大小变化，更新边界信息
    window.addEventListener('resize', this.updateContainerBounds);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.updateContainerBounds);
  },
  methods: {
    updateContainerBounds() {
      this.containerBounds = this.$refs.container.getBoundingClientRect();
      // console.log(this.containerBounds);
    },
    startDragging(event) {
      this.isDragging = true;
      this.updateContainerBounds();
      window.addEventListener("mousemove", this.onDrag);
      window.addEventListener("mouseup", this.stopDragging);
    },
    stopDragging() {
      this.isDragging = false;
      window.removeEventListener("mousemove", this.onDrag);
      window.removeEventListener("mouseup", this.stopDragging);
    },
    onDrag(event) {
      if (!this.isDragging || !this.containerBounds) return;

      // 计算鼠标相对图片边界的位置
      const relativeX = event.clientX - this.containerBounds.left;

      // 滑块位置百分比，基于图片显示区域宽度计算
      let newLeftWidth = (relativeX / this.containerBounds.width) * 100;

      // 限制滑块位置在图片范围内
      let leftBound = (this.$refs.leftImage.getBoundingClientRect().left - this.containerBounds.left) / this.containerBounds.width * 100;
      let rightBound = (this.$refs.leftImage.getBoundingClientRect().right - this.containerBounds.left) / this.containerBounds.width * 100;

      // console.log(this.$refs.leftImage.getBoundingClientRect())
      // console.log(this.$refs.container.getBoundingClientRect())
      // console.log(leftBound,rightBound)

      newLeftWidth = Math.max(leftBound, Math.min(rightBound, newLeftWidth));

      // 更新滑块位置
      this.leftWidth = newLeftWidth;
    },

  },
};
</script>

<style scoped>
/* 保证背景为全黑 */
.bg-black {
  background-color: #000;
}
</style>