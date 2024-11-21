<template>
  <div class="relative w-full h-screen overflow-hidden bg-black" ref="container" v-if="controlImage">
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

    <button class="absolute rounded-lg  bottom-0 text-xs opacity-80 bg-gray-400" :style="{left: leftBound + '%'}" v-if="controlTextLeft">Original</button>

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
    <button class="absolute rounded-lg  bottom-0 text-xs opacity-80 bg-gray-400" :style="{right: leftBound + '%'}" v-if="controlTextRight">Processed</button>
    <!-- 滑动按钮 -->
    <div
        class="absolute top-0 bottom-0 w-[3px] bg-white cursor-ew-resize z-10"
        :style="{ left: leftWidth + '%' }"
        @mousedown.prevent="startDragging"
    >
      <span
          class="absolute top-1/2 -left-2.5 w-5 h-5 rounded-full transform -translate-y-1/2 flex items-center justify-center"
      >
    <img src="/svgs/左右箭头.svg" alt="icon" class="w-full h-full" draggable="false"/>
</span>

    </div>
  </div>

  <div class="relative w-full h-screen overflow-hidden bg-black" ref="container" v-else>
    <div
        class="absolute top-0 left-0 w-full h-full overflow-hidden"
    >
      <img
          :src="leftImage"
          alt="Left Image"
          ref="leftImage"
          class="absolute inset-0 m-auto object-contain h-full"
      />
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
    // rightImage: {
    //   type: String,
    //   required: true,
    // },
  },
  data() {
    return {
      leftWidth: 50, // 初始化滑块位置为50%
      isDragging: false,
      containerBounds: null,
      controlImage: true,  //控制遮罩容器加载
      rightImage: "/images/processed_1.png",
      controlTextLeft: false,  //控制干净图片状态标签
      controlTextRight: false,  //控制脏图片状态标签
      leftBound : null,
      rightBound : null,

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
    changeStatus(){
      this.controlImage = !this.controlImage;
    },
    updateContainerBounds() {
      this.containerBounds = this.$refs.container.getBoundingClientRect();
      this.leftBound = (this.$refs.leftImage.getBoundingClientRect().left - this.containerBounds.left) / this.containerBounds.width * 100;
      this.rightBound = (this.$refs.leftImage.getBoundingClientRect().right - this.containerBounds.left) / this.containerBounds.width * 100;

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
      const relativeX = event.clientX - this.containerBounds.left;
      let newLeftWidth = (relativeX / this.containerBounds.width) * 100;
      newLeftWidth = Math.max(this.leftBound, Math.min(this.rightBound, newLeftWidth));
      if (newLeftWidth === this.leftBound)
        this.controlTextLeft = true;
      else if (newLeftWidth === this.rightBound)
        this.controlTextRight = true;
      else
        this.controlTextRight = this.controlTextLeft = false;
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