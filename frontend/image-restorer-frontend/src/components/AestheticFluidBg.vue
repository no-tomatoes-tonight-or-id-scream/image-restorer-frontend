<template>
  <div class="absolute w-full h-full">
    <div
        id="box"
        class="absolute w-full h-full bg-gray-100"
    ></div>
  </div>
</template>

<script>
import { onBeforeUnmount, watch } from "vue";
import * as StackBlur from "stackblur-canvas";
export default {
  name: "Bg",
  props: {
    uploadedFile: {
      type: String,
      required: false, // 表示不是必须传入的
    },
  },
  data() {
    return {
      colorbg: null, // 存储背景实例
      defaultColors: ["#283c63", "#928a97", "#f85f73", "#f85f73", "#928a97"], // 默认颜色
    };
  },
  mounted() {
    if (this.uploadedFile) {
      this.updateBackground(this.uploadedFile);
    } else {
      this.updateBackground(null); // 未传入时使用默认颜色
    }

    // 监听窗口大小变化
    const handleResize = () => {
      if (this.colorbg) {
        this.colorbg.destroy();
        this.colorbg = null;
      }
      this.updateBackground(this.uploadedFile || null); // 更新背景
    };

    window.addEventListener("resize", handleResize);

    // 移除事件监听和销毁资源
    onBeforeUnmount(() => {
      window.removeEventListener("resize", handleResize);
      if (this.colorbg) {
        this.colorbg.destroy();
      }
    });
  },
  watch: {
    // 监听 props 传入的 uploadedFile
    uploadedFile: {
      immediate: true, // 初次挂载时也会调用
      handler(newFile) {
        this.updateBackground(newFile || null); // 未传入时使用默认颜色
      },
    },
  },
  methods: {
    // 提取图片颜色并更新背景
    async updateBackground(imageUrl) {
      let colors = this.defaultColors; // 默认使用默认颜色
      try {
        if (imageUrl) {
          // 如果传入了图片路径，提取颜色
          colors = await this.processImageWithBlur(imageUrl);
          console.log("提取的颜色：", colors);
        }

        // 如果已有背景实例，销毁之前的
        if (this.colorbg) {
          this.colorbg.destroy();
        }

        // 创建新的背景实例
        this.colorbg = new Color4Bg.AestheticFluidBg({
          dom: "box",
          colors: colors,
          loop: true,
          seed: Math.floor(Math.random() * 10000),
        });
      } catch (error) {
        console.error("图片处理失败：", error);
        // 出现异常时也使用默认颜色
        if (this.colorbg) {
          this.colorbg.destroy();
        }
        this.colorbg = new Color4Bg.AestheticFluidBg({
          dom: "box",
          colors: this.defaultColors,
          loop: true,
          seed: Math.floor(Math.random() * 10000),
        });
      }
    },

    // 图片模糊和颜色提取逻辑
    processImageWithBlur(imageUrl) {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.crossOrigin = "Anonymous"; // 允许跨域处理图片
        img.onload = () => {
          const canvas = document.createElement("canvas");
          const ctx = canvas.getContext("2d");

          // 设置原始图像的尺寸
          canvas.width = img.width;
          canvas.height = img.height;

          // 绘制原始图像到画布
          ctx.drawImage(img, 0, 0);

          // 应用高斯模糊，使用 StackBlur
          StackBlur.canvasRGBA(canvas, 0, 0, img.width, img.height, 10); // 10 为模糊半径

          // 缩小到 8x8
          const smallCanvas = document.createElement("canvas");
          const smallCtx = smallCanvas.getContext("2d");
          const targetSize = 8;
          smallCanvas.width = targetSize;
          smallCanvas.height = targetSize;
          smallCtx.drawImage(canvas, 0, 0, targetSize, targetSize);

          // 获取缩小后的像素数据
          const imageData = smallCtx.getImageData(0, 0, targetSize, targetSize);
          const pixels = imageData.data; // RGBA 数据

          const generateRandomPoints = (count, maxX, maxY) => {
            const points = new Set();
            while (points.size < count) {
              const x = Math.floor(Math.random() * maxX); // 随机生成 x 坐标
              const y = Math.floor(Math.random() * maxY); // 随机生成 y 坐标
              points.add(`${x},${y}`); // 使用字符串表示点，避免重复
            }
            return Array.from(points).map((point) => point.split(",").map(Number));
          };

          // 提取几个像素点的颜色值并转换为 #RRGGBB 格式
          // const samplePoints = [
          //   [0, 0],
          //   [7, 0],
          //   [0, 7],
          //   [7, 7],
          //   [4, 4], // 5 个示例点
          // ];

          const samplePoints = generateRandomPoints(5,smallCanvas.width, smallCanvas.height);


          const colors = samplePoints.map(([x, y]) => {
            const index = (y * targetSize + x) * 4;
            const r = pixels[index];
            const g = pixels[index + 1];
            const b = pixels[index + 2];
            return this.rgbToHex(r, g, b);
          });

          resolve(colors);
        };

        img.onerror = (error) => reject(error);

        img.src = imageUrl; // 加载图片
      });
    },

    // 将 RGB 转换为 #RRGGBB 格式
    rgbToHex(r, g, b) {
      return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`;
    },
  },


};
</script>
