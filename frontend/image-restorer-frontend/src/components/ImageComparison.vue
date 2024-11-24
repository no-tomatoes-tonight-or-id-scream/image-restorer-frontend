<!--本组件一共分为两部分，这两个部分是互斥关系
并且使用一个布尔值进行控制，一个部分是显示原始图片
另外一个部分是显示两张图片的对比，初始的状态下是显示原始图片
当收到处理好的图片后进入对比部分的容器-->


<template>
<!--  对比图片部分-->
  <div class="absolute h-full w-full" ref="container" v-if="controlImage" @mousemove="checkMousePosition">
    <div
        class="absolute inset-0 bg-center bg-cover blur-[64px]"
        :style="{ backgroundImage: 'url(' + dirtyImage + ')' }"
    ></div>
    <div class="absolute inset-0 bg-gradient-to-t from-grey via-transparent to-transparent"></div>


    <!-- 左边的未处理图片部分，通过 clip-path 进行遮罩 -->
    <div
        class="absolute w-full h-full"
        :style="{ clipPath: `inset(0 0 0 ${leftWidth}%)` }"
        draggable="false"
    >
      <img
          :src="dirtyImage"
          alt="Left Image"
          ref="leftImage"
          class="absolute inset-0 m-auto  object-contain h-full shadow-2xl"
          draggable="false"
      />
    </div>

    <button class="absolute rounded-lg  bottom-0 text-xs opacity-80 bg-gray-600" :style="{left: leftBound + '%'}" v-if="controlTextLeft">Original</button>

    <!-- 右边的处理图片部分，通过 clip-path 进行遮罩 -->
    <div
        class="absolute top-0 left-0 w-full h-full overflow-hidden"
        :style="{ clipPath: `inset(0 ${100 - leftWidth}% 0 0)` }"
        draggable="false"
    >
      <img
          :src="cleanImage"
          alt="Right Image"
          ref="rightImage"
          class="absolute inset-0 m-auto object-contain h-full shadow-2xl"
          draggable="false"
      />
    </div>
    <button class="absolute rounded-lg  bottom-0 text-xs opacity-80 bg-gray-600" :style="{right: leftBound + '%'}" v-if="controlTextRight">Processed</button>
    <!-- 滑动按钮 -->
    <div
        class="absolute top-0 bottom-0 w-[3px] bg-white cursor-ew-resize z-10"
        :style="{ left: leftWidth + '%' }"
        @mousedown.prevent="startDragging"

    >
      <span
          class="absolute top-1/2 -left-2.5 w-5 h-5 rounded-full transform -translate-y-1/2 flex items-center justify-center"
      >
    <img src="/svgs/左右箭头.svg" alt="icon" class="icon-img w-full h-full" draggable="false"/>
</span>

    </div>
  </div>


<!--  原始图片部分-->
  <div class="absolute h-full w-full" ref="container" v-else>
    <div
        class="absolute inset-0 bg-center bg-cover blur-[25px]"
        :style="{ backgroundImage: 'url(' + dirtyImage + ')' }"
    ></div>
    <div class="absolute inset-0 bg-gradient-to-t from-grey via-transparent to-transparent"></div>
<!--    <div class="absolute inset-0 bg-grey bg-opacity-80"></div>-->
      <img
          :src="dirtyImage"
          alt="Left Image"
          ref="leftImage"
          class="absolute  object-contain  w-full h-full shadow-inner"

      />
  </div>
<!--            style="clip-path: inset(0 10% 0 10%);"-->
<!--            :style="{ transform: 'translateX(24%)' }"-->
</template>

<script>
export default {
  props: {
    dirtyImage: {
      type: String,
      required: true,
    },
    cleanImage: {
      type: [String, null],
      required: true,
    },

  },
  data() {
    return {
      leftWidth: 50, // 初始化滑块位置为50%
      isDragging: false,
      containerBounds: null,
      controlImage: false,  //控制遮罩容器加载
      controlTextLeft: false,  //控制干净图片状态标签
      controlTextRight: false,  //控制脏图片状态标签
      leftBound : null,
      rightBound : null,

    };
  },
  watch: {
    // 监听 externalProp 的变化
    cleanImage(newVal, oldVal) {
      // console.log("图片base",newVal);
      this.controlImage = true;
    },
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
      this.imageLeftBound = this.$refs.leftImage.getBoundingClientRect().left;
      this.imageRightBound = this.$refs.leftImage.getBoundingClientRect().right;
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
    onWheel(event) {
      this.updateContainerBounds();
      console.log("滚轮边界",this.imageRightBound-this.imageLeftBound);
      const step = 3; // 每次滚动调整的百分比宽度
      let newLeftWidth = this.leftWidth + (event.deltaY > 0 ? -step : step);
      newLeftWidth = Math.max(this.leftBound, Math.min(this.rightBound, newLeftWidth));

      if (newLeftWidth === this.leftBound)
        this.controlTextLeft = true;
      else if (newLeftWidth === this.rightBound)
        this.controlTextRight = true;
      else
        this.controlTextRight = this.controlTextLeft = false;

      // 更新滑块位置
      this.leftWidth = newLeftWidth;

      // 阻止页面滚动
      event.preventDefault();
    },

    checkMousePosition(event)
    {
      // 检查鼠标是否在容器范围内
      const relativeX = event.clientX - this.imageLeftBound;
      const isInside = relativeX >= 0 && relativeX <= (this.imageRightBound-this.imageLeftBound);

      if (isInside)
      {
        this.$refs.container.addEventListener('wheel', this.onWheel);
      }
      else
      {
        this.$refs.container.removeEventListener('wheel', this.onWheel);
      }
    },


  },
};
</script>

<style scoped>
/* 保证背景为全黑 */
.bg-black {
  background-color: #000;
}

img:hover {

  transform: scale(1.01); /* 略微旋转和放大 */
  filter: brightness(1.1); /* 提高亮度 */
}


</style>