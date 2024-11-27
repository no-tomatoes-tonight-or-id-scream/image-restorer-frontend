<!--本组件一共分为两部分，这两个部分是互斥关系
并且使用一个布尔值进行控制，一个部分是显示原始图片
另外一个部分是显示两张图片的对比，初始的状态下是显示原始图片
当收到处理好的图片后进入对比部分的容器-->

<template>

  <div class="absolute h-[80%] w-full top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" ref="container"
    v-if="controlImage" @mousemove="checkMousePosition">
    <div class="absolute w-full h-full" :style="{ clipPath: `inset(-100px 0 -100px ${leftWidth}%)` }" draggable="false">
      <img :src="dirtyImage" alt="Left Image" ref="leftImage"
        class="absolute inset-0 m-auto object-contain h-full rounded-xl shadow-[0_0_50px_20px_rgba(0,0,0,0.5)]"
        draggable="false" />
    </div>

    <button class="absolute rounded-lg bottom-0 text-xs opacity-80 bg-gray-600" :style="{ left: leftBound + '%' }"
      v-if="controlTextLeft">
      Original
    </button>

    <!-- 右边的处理图片部分，通过 clip-path 进行遮罩 -->
    <div class="absolute top-0 left-0 w-full h-full "
      :style="{ clipPath: `inset(-100px ${100 - leftWidth}% -100px 0)` }" draggable="false">
      <img :src="cleanImage" alt="Right Image" ref="rightImage"
        class="absolute inset-0 m-auto object-contain h-full rounded-xl shadow-[0_0_50px_20px_rgba(0,0,0,0.5)]"
        draggable="false" />
    </div>
    <button class="absolute rounded-lg bottom-0 text-xs opacity-80 bg-gray-600" :style="{ right: leftBound + '%' }"
      v-if="controlTextRight">
      Processed
    </button>
    <!-- 滑动按钮 -->
    <div class="absolute top-0 bottom-0 w-[3px] bg-white cursor-ew-resize z-10" :style="{ left: leftWidth + '%' }"
      @mousedown.prevent="startDragging">
      <span
        class="absolute top-1/2 -left-2.5 w-5 h-5 rounded-full transform -translate-y-1/2 flex items-center justify-center">
        <img src="/svgs/左右箭头.svg" alt="icon" class="icon-img w-full h-full" draggable="false" />
      </span>
    </div>
  </div>

  <div :style="overlayStyle" class="fixed backdrop-blur-xl rounded-xl flex items-center justify-center" ref="overlay"
    v-if="loading">
    <!-- 加入加载中的内容 -->
    <div class="loading-overlay" v-cloak>
      <div id="original">

        <div class="box">
          <span></span>
          <span></span>
          <span></span>
          <span></span>
          <span></span>
        </div>
        <p class="text-white text-xl mt-4">处理中，请稍候...</p>
      </div>

    </div>、
  </div>



  <!--  原始图片部分-->
  <div id="original" class="absolute h-[80%] w-full top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
    ref="container" v-if="!controlImage">

    <img :src="dirtyImage" alt="Left Image" ref="leftImage"
      class="absolute inset-0 m-auto object-contain h-full rounded-xl shadow-[0_0_50px_20px_rgba(0,0,0,0.5)]"
      draggable="false" @load="updateOverlay" />



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
    isLoading: {
      type: Boolean,
      default: false,
      required: false,
    }
  },
  data() {
    return {
      leftWidth: 50, // 初始化滑块位置为 50%
      isDragging: false,
      containerBounds: null,
      controlImage: false, //控制遮罩容器加载
      controlTextLeft: false, //控制干净图片状态标签
      controlTextRight: false, //控制脏图片状态标签
      leftBound: null,
      rightBound: null,
      loading: false,
      overlayStyle: {},
    };
  },
  watch: {
    // 监听 externalProp 的变化
    cleanImage(newVal, oldVal) {
      this.controlImage = true;
      this.loading = false;
    },
    isLoading(newVal, oldVal) {
      this.loading = true;
    }
  },
  mounted() {
    // 获取容器的边界信息

    this.updateContainerBounds();
    // 监听窗口大小变化，更新边界信息
    window.addEventListener("resize", this.updateOverlay);
    window.addEventListener("resize", this.updateContainerBounds);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.updateContainerBounds);
  },
  methods: {
    updateContainerBounds() {
      this.containerBounds = this.$refs.container.getBoundingClientRect();
      this.imageLeftBound = this.$refs.leftImage.getBoundingClientRect().left;
      this.imageRightBound = this.$refs.leftImage.getBoundingClientRect().right;
      this.leftBound =
        ((this.$refs.leftImage.getBoundingClientRect().left -
          this.containerBounds.left) /
          this.containerBounds.width) *
        100;
      this.rightBound =
        ((this.$refs.leftImage.getBoundingClientRect().right -
          this.containerBounds.left) /
          this.containerBounds.width) *
        100;

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
      newLeftWidth = Math.max(
        this.leftBound,
        Math.min(this.rightBound, newLeftWidth)
      );
      if (newLeftWidth === this.leftBound) this.controlTextLeft = true;
      else if (newLeftWidth === this.rightBound) this.controlTextRight = true;
      else this.controlTextRight = this.controlTextLeft = false;
      // 更新滑块位置
      this.leftWidth = newLeftWidth;
    },
    onWheel(event) {
      this.updateContainerBounds();
      console.log("滚轮边界", this.imageRightBound - this.imageLeftBound);
      const step = 3; // 每次滚动调整的百分比宽度
      let newLeftWidth = this.leftWidth + (event.deltaY > 0 ? -step : step);
      newLeftWidth = Math.max(
        this.leftBound,
        Math.min(this.rightBound, newLeftWidth)
      );

      if (newLeftWidth === this.leftBound) this.controlTextLeft = true;
      else if (newLeftWidth === this.rightBound) this.controlTextRight = true;
      else this.controlTextRight = this.controlTextLeft = false;

      // 更新滑块位置
      this.leftWidth = newLeftWidth;

      // 阻止页面滚动
      event.preventDefault();
    },

    checkMousePosition(event) {
      // 检查鼠标是否在容器范围内
      const relativeX = event.clientX - this.imageLeftBound;
      const isInside =
        relativeX >= 0 &&
        relativeX <= this.imageRightBound - this.imageLeftBound;

      if (isInside) {
        this.$refs.container.addEventListener("wheel", this.onWheel);
      } else {
        this.$refs.container.removeEventListener("wheel", this.onWheel);
      }
    },
    updateOverlay() {
      const imageContainer = this.$refs.leftImage;

      if (imageContainer) {
        const rect = imageContainer.getBoundingClientRect();

        this.overlayStyle = {
          width: `${rect.width}px`,
          height: `${rect.height}px`,
          top: `${rect.top + rect.height / 2}px`,
          left: `${rect.left + rect.width / 2}px`,
          transform: "translate(-50%, -50%)", // 让覆盖层中心点对齐
          zIndex: 50,
        };

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
  transform: scale(1.01) rotate(1deg);
  /* 放大并旋转 */
  filter: brightness(1.1);
  /* 提高亮度 */
  transition-duration: 500ms;
  /* 过渡时间 */
}

img {
  transition: all 0.5s ease-in-out;
  /* 平滑过渡效果 */
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

.loading-overlay {
  position: absolute;
  width: 100.1%;
  height: 100.1%;
  background: rgba(0, 0, 0, 0.2);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border-radius: inherit;
  overflow: hidden;
  /* 边缘羽化效果 */
  animation: fadeIn 0.3s ease-in-out forwards;
}

.box {
  position: relative;
  width: 80px;
  /* 调整宽度以适配动态布局 */
  height: 20px;
  margin: 0 auto;
  display: flex;
  /* 使用 flex 布局让子元素更自然排列 */
  justify-content: space-between;
}

.box span {
  width: 15px;
  height: 15px;
  background: #3498db;
  opacity: 0.5;
  border-radius: 50%;
  animation: anim 1s infinite ease-in-out;
}

/* 动态控制子元素动画延迟 */
.box span:nth-child(1) {
  animation-delay: 0s;
}

.box span:nth-child(2) {
  animation-delay: 0.2s;
}

.box span:nth-child(3) {
  animation-delay: 0.4s;
}

.box span:nth-child(4) {
  animation-delay: 0.6s;
}

.box span:nth-child(5) {
  animation-delay: 0.8s;
}

@keyframes anim {
  0% {
    opacity: 0.3;
    transform: translateY(0);
  }

  50% {
    opacity: 1;
    transform: translateY(-10px);
    background: #f9cdff;
    /* 动态颜色变化 */
  }

  100% {
    opacity: 0.3;
    transform: translateY(0);
  }
}
</style>
