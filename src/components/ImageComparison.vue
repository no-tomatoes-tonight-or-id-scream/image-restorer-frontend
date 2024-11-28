<template>

  <!--
        本组件简单分为三部分
          按照先后出现的顺序为
          原始图片(即含有噪声的图片)
          Loading页面(点击提交后的等候页面)
          对比图片部分(处理和未处理用遮罩动态对比)
        接口
          dirtyImage由UploadImage组件传入 代表含噪音的图片 类型是URL
          cleanImage由Menu组件传入 代表处理好的图片 类型是URL
          isLoading由Menu组件传入 用于触发加载页面 不是必要传的(首次挂载本组件)

  -->

  <!-- 第一部分 原始图片部分-->
  <div id="original" class="absolute h-[80%] w-full top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" ref="container" v-if="!canCompare">

    <img
        :src="dirtyImage"
        alt="Left Image"
        ref="leftImage"
        class="absolute inset-0 m-auto object-contain h-full rounded-xl shadow-[0_0_50px_20px_rgba(0,0,0,0.5)]"
        draggable="false"
        @load="handleImageLoaded"
    />

  </div>

  <!-- 第二部分 Loading页面-->
  <div
      :style="overlayStyle"
      class="fixed backdrop-blur-xl rounded-xl flex items-center justify-center"
      ref="overlay"
      v-if="loading"
  >
    <div  class="loading-overlay" v-cloak>
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

    </div>
  </div>

  <!--第三部分 对比图片 包含滑块 遮罩层 按钮标签等   -->
  <div
      class="absolute h-[80%] w-full top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
      ref="container"
      v-if="canCompare"
      @mousemove="checkMousePosition"
  >
    <div
        class="absolute w-full h-full"
        :style="{ clipPath: `inset(-100px 0 -100px ${leftWidth}%)`}"
        draggable="false"

    >
      <img
          :src="dirtyImage"
          alt="Left Image"
          ref="leftImage"
          class="absolute inset-0 m-auto object-contain h-full rounded-xl shadow-[0_0_50px_20px_rgba(0,0,0,0.5)]"

          draggable="false"
      />
    </div>

    <button
        class="absolute rounded-lg bottom-0 text-xs opacity-80 bg-gray-600"
        :style="{ left: imageLeftBoundPer + '%' }"
        v-if="controlTextLeft"
    >
      Original
    </button>

    <!-- 右边的处理图片部分，通过 clip-path 进行遮罩 -->
    <div
        class="absolute top-0 left-0 w-full h-full "
        :style="{ clipPath: `inset(-100px ${100 - leftWidth}% -100px 0)` }"
        draggable="false"

    >
      <img
          :src="cleanImage"
          alt="Right Image"
          ref="rightImage"
          class="absolute inset-0 m-auto object-contain h-full rounded-xl shadow-[0_0_50px_20px_rgba(0,0,0,0.5)]"
          draggable="false"
      />
    </div>
    <button
        class="absolute rounded-lg bottom-0 text-xs opacity-80 bg-gray-600"
        :style="{ right: imageLeftBoundPer + '%' }"
        v-if="controlTextRight"
    >
      Processed
    </button>

    <!-- 滑动按钮 -->
    <div
        class="absolute top-0 bottom-0 w-[3px] bg-white cursor-ew-resize z-10"
        :style="{ left: leftWidth + '%' }"
        @mousedown.prevent="startDragging"
    >
      <span
          class="absolute top-1/2 -left-2.5 w-5 h-5 rounded-full transform -translate-y-1/2 flex items-center justify-center"
      >
        <img
            src="/svgs/左右箭头.svg"
            alt="icon"
            class="icon-img w-full h-full"
            draggable="false"
        />
      </span>
    </div>
  </div>

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
    isLoading:{
      type: Boolean,
      default: false,
      required: false,
    }
  },

  data() {
    return {
      leftWidth: 50,           //初始化滑块位置为 50%
      canCompare: false,       //控制遮罩容器加载
      controlTextLeft: false,  //控制干净图片状态标签
      controlTextRight: false, //控制脏图片状态标签
      loading: false,          //控制 加载中 动画
      overlayStyle: {},        //动态 加载中 样式
      imageLeftBoundPer : 0,   //图片左边界占父容器宽度的百分比
    };
  },

  watch: {

    cleanImage(newVal, oldVal) {
      this.canCompare = true;
      this.loading = false;
    },

    isLoading(newVal, oldVal) {
      this.loading = true;
      this.leftWidth = 50;
    }

  },

  mounted()
  {

    // 获取容器的边界信息
    this.initShareVar();
    this.updateContainerBounds();

    // 监听窗口大小变化，更新边界信息
    window.addEventListener("resize", this.updateOverlay);
    window.addEventListener("resize", this.updateContainerBounds);

  },

  beforeDestroy()
  {
    window.removeEventListener("resize", this.updateContainerBounds);
    window.removeEventListener("resize", this.updateOverlay);
  },

  methods: {

    //初始化共享变量
    initShareVar()
    {

      //函数间非响应式共享变量的定义
      this.share = {

        //图片容器边界占父容器宽度的百分比
        imageBoundsPercent : {
          left : null,
          right : null,
        },

        //图片容器信息
        imageBounds : {
          left : null,
          right : null,
          width : null,
          height: null,
          top : null,
        },

        //图片父容器的左右边界的实际位置
        imageFatherBounds : {
          left : null,
          right : null,
          width : null,
        }

      }
    },

    //图片加载完成后的触发函数
    handleImageLoaded()
    {
      this.updateContainerBounds();
      this.updateOverlay();
    },

    //更新图片及其父容器的信息
    updateContainerBounds()
    {
      //更新图片左右占父容器宽度的占比
      let imageFatherBounds = this.$refs.container.getBoundingClientRect();
      let imageBounds = this.$refs.leftImage.getBoundingClientRect();

      this.share.imageBounds.left = imageBounds.left;
      this.share.imageBounds.right = imageBounds.right;
      this.share.imageBounds.width = imageBounds.width;
      this.share.imageBounds.height = imageBounds.height;
      this.share.imageBounds.top = imageBounds.top;

      this.share.imageFatherBounds.left = imageFatherBounds.left;
      this.share.imageFatherBounds.right = imageFatherBounds.right;
      this.share.imageFatherBounds.width = imageFatherBounds.width;

      this.share.imageBoundsPercent.left =
        ((imageBounds.left - imageFatherBounds.left) / imageFatherBounds.width) * 100;
      this.share.imageBoundsPercent.right =
        ((imageBounds.right - imageFatherBounds.left) / imageFatherBounds.width) * 100;

      this.imageLeftBoundPer = imageBounds.left; //更新边界动态变量

    },

    startDragging(event)
    {
      window.addEventListener("mousemove", this.onDrag);
      window.addEventListener("mouseup", this.stopDragging);
    },

    stopDragging()
    {
      window.removeEventListener("mousemove", this.onDrag);
      window.removeEventListener("mouseup", this.stopDragging);
    },

    onDrag(event)
    {
      const relativeX = event.clientX - this.share.imageFatherBounds.left;
      let newLeftWidth = (relativeX / this.share.imageFatherBounds.width) * 100;

      //限制越界行为
      newLeftWidth = Math.max(
        this.share.imageBoundsPercent.left,
        Math.min(this.share.imageBoundsPercent.right, newLeftWidth)
      );

      if (newLeftWidth === this.share.imageBoundsPercent.left) this.controlTextLeft = true;
      else if (newLeftWidth === this.share.imageBoundsPercent.right) this.controlTextRight = true;
      else this.controlTextRight = this.controlTextLeft = false;

      // 更新滑块位置
      this.leftWidth = newLeftWidth;
    },

    onWheel(event) {

      const step = 3; // 每次滚动调整的百分比宽度
      let newLeftWidth = this.leftWidth + (event.deltaY > 0 ? -step : step);

      newLeftWidth = Math.max(
          this.share.imageBoundsPercent.left,
          Math.min(this.share.imageBoundsPercent.right, newLeftWidth)
      );

      if (newLeftWidth === this.share.imageBoundsPercent.left) this.controlTextLeft = true;
      else if (newLeftWidth === this.share.imageBoundsPercent.right) this.controlTextRight = true;
      else this.controlTextRight = this.controlTextLeft = false;

      // 更新滑块位置
      this.leftWidth = newLeftWidth;

      // 阻止页面滚动
      event.preventDefault();

    },

    // 检查鼠标是否在容器范围内
    checkMousePosition(event)
    {
      const relativeX = event.clientX - this.share.imageBounds.left;
      const isInside =
        relativeX >= 0 &&
        relativeX <= this.share.imageBounds.width;

      if (isInside)
        this.$refs.container.addEventListener("wheel", this.onWheel);
      else
        this.$refs.container.removeEventListener("wheel", this.onWheel);

    },

    updateOverlay() {
      const imageContainer = this.$refs.leftImage;

      if (imageContainer) {

        this.overlayStyle = {
          width: `${this.share.imageBounds.width}px`,
          height: `${this.share.imageBounds.height}px`,
          top: `${this.share.imageBounds.top + this.share.imageBounds.height / 2}px`,
          left: `${this.share.imageBounds.left + this.share.imageBounds.width / 2}px`,
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
  transform: scale(1.01) rotate(1deg); /* 放大并旋转 */
  filter: brightness(1.1); /* 提高亮度 */
  transition-duration: 500ms; /* 过渡时间 */
}

img {
  transition: transform 0.5s, filter 0.5s; /* 过渡效果 */
}


.loading-overlay {
  position: absolute; /* 确保覆盖容器的范围适配 */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.2); /* 背景遮罩 */
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px); /* 背景模糊效果 */
  border-radius: inherit; /* 确保和父容器一致的圆角 */
  overflow: hidden; /* 限制内容不超出容器 */
}


.box {
  position: relative;
  width: 80px; /* 调整宽度以适配动态布局 */
  height: 20px;
  margin: 0 auto;
  display: flex; /* 使用 flex 布局让子元素更自然排列 */
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
    background: #f9cdff; /* 动态颜色变化 */
  }
  100% {
    opacity: 0.3;
    transform: translateY(0);
  }
}

</style>
