<template>
  <div>
    <div v-if="isVisible" class="menu-wrapper rounded-xl">
      <form @submit.prevent="handleSubmit">
        <!-- 模型选择 -->
        <div class="menu-item">
          <label for="modelType" class="label">
            <span class="label-text text-lg font-semibold text-white">模型：</span>
          </label>
          <select id="modelType" v-model="formData.modelType" class="select select-bordered w-full">
            <!-- 显示模型选项 -->
            <option v-for="(value, key) in modelList" :key="key" :value="value">
              {{ key }}
            </option>
          </select>
        </div>

        <!-- 放大倍数 -->
        <div class="menu-item">
          <label for="scale" class="label">
            <span class="label-text text-lg font-semibold text-white">放大倍数：</span>
          </label>
          <div class="flex items-center">
            <input id="scale" type="range" v-model.number="formData.scale" min="1" max="2.5" step="0.1"
                   class="range-primary custom-slider" />
            <span class="ml-4 text-lg text-white">{{ formData.scale.toFixed(1) }}</span>
          </div>
        </div>

        <!-- 提交按钮 -->
        <button type="submit" class="btn w-full text-lg">
          提交
        </button>

        <!-- 返回上传按钮 -->
        <button type="button" @click="goBack" class="btn w-full text-lg mt-2">
          返回上传
        </button>

        <!-- 图片下载按钮（任务完成时显示） -->
        <button
            v-if="isCompleted"
            type="button"
            @click="downloadImage"
            class="btn w-full text-lg mt-2"
        >
          下载图片
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Menu",
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
    uploadedFile: {
      type: File,
      required: false,
    },
    baseUrl: {
      type: String,
      required: true,
    },
  },
  emits: ["pics-upload", "menuDone", "isLoading", "DownloadRequest",],
  data() {
    return {
      formData: {
        modelType: "", // 默认模型为空，动态填充
        scale: 1.0, // 默认放大倍数
      },
      modelList: {}, // 初始化为空对象，确保 v-for 能正常运行
      checkCnt: 0,
      isCompleted: false,
    };
  },
  mounted() {
    this.getModelList();
  },

  methods: {
    goBack() {
      // 路由跳转到 home
      this.$router.push('/');

    },
    downloadImage() {
      // 向父组件发送下载事件信号
      this.$emit("DownloadRequest");
      console.log("send signal");
    },

    checkTaskStatus(task_id) {
      const targetUrl = `${this.baseUrl}get_status?task_id=${task_id}`;
      axios
        .get(targetUrl)
        .then((response) => {
          const { status } = response.data;
          console.log("任务状态：", status);

          if (status === "completed") {
            this.getResultImg(task_id);
            setTimeout(() => {
              this.isLoading = false; // 加载完成后隐藏
              //this.isVisible = false; // 隐藏菜单
              this.$emit("menuDone");
              this.isCompleted = true;
            }, 1500);
          } else if (status === "error") {
            this.isLoading = false;
            this.$emit("menuDone");
            console.error("任务发生错误！");
          } else {
            this.isLoading = true;
            this.checkCnt++;
            if (this.checkCnt >= 60) {
              this.getResultImg(task_id);
              this.isLoading = false;
              this.$emit("menuDone");
              this.checkCnt = 0;
            } else {
              setTimeout(() => this.checkTaskStatus(task_id), 2000);
            }
          }
        })
        .catch((error) => {
          this.isLoading = false;
          console.error("查询任务状态失败：", error);
          this.$emit("menuDone");
        });
    },

    getResultImg(task_id) {
      const targetUrl = `${this.baseUrl}get_result?task_id=${task_id}`;
      axios
        .get(targetUrl, { responseType: "arraybuffer" })
        .then((response) => {
          const binary = new Uint8Array(response.data).reduce(
            (acc, byte) => acc + String.fromCharCode(byte),
            ""
          );
          const base64Image = `data:image/jpeg;base64,${btoa(binary)}`;
          this.$emit("pics-upload", base64Image);
        })
        .catch((error) => {
          console.error("下载结果图像失败：", error);
          this.isLoading = false;
        });
    },

    async handleSubmit() {
      this.$emit("isLoading",true);


      const params = {
        target_scale: this.formData.scale,
        pretrained_model_name: this.formData.modelType,
      };
      const queryString = new URLSearchParams(params).toString();
      const postData = new FormData();
      const file = await this.convertUrlToFile(this.uploadedFile, "uploaded_image.jpg");
      postData.append("image", file);

      const targetUrl = `${this.baseUrl}process?${queryString}`;
      axios
        .post(targetUrl, postData)
        .then((response) => {
          const { status, task_id } = response.data;
          console.log("status:", status, "task_id:", task_id);
          this.checkTaskStatus(task_id);
        })
        .catch((error) => {
          this.isLoading = false;
          console.log("处理失败！");
          this.$emit("menuDone");
          console.log(this.isVisible);
          console.error("错误：", error);
        });
    },

    getModelList() {
      const targetUrl = `${this.baseUrl}get_model_list`;
      axios
        .get(targetUrl)
        .then((response) => {
          this.modelList = response.data;
          // 设置默认模型为返回列表中的第一个模型
          const firstModel = Object.values(response.data)[0];
          if (firstModel) {
            this.formData.modelType = firstModel;
          }
        })
        .catch((error) => {
          console.error("请求模型列表出错！出错信息：", error);
        });
    },
    //将 url 重构为文件
    async convertUrlToFile(url, fileName) {
      const response = await fetch(url);
      const blob = await response.blob();
      return new File([blob], fileName, { type: blob.type });
    }
  },
};
</script>

<style scoped>
.menu-wrapper {

  top: 20%;
  left: 10%;

  width: 30vw;
  padding: 30px;
  background: #131a268e;
  /* 半透明背景 */
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
  /* 柔和阴影 */
  z-index: 50;
  backdrop-filter: blur(50px);
  /* 背景模糊 */
}

.menu-item {
  margin-bottom: 20px;
}

.btn {
  background: #fbe8d3;
  /* 绿色按钮 */
  color: #283c63;
  /* 白色文字 */
}

.btn:hover {
  background: #283c63;
  /* 鼠标悬停变色 */
  color: #ffffff;
  /* 鼠标悬停变色 */
}

.custom-slider {
  -webkit-appearance: none;
  /* 去除默认样式 */
  width: 100%;
  height: 8px;
  border-radius: 10px;
  background: linear-gradient(90deg, #928a97, #283c63);
  /* 渐变色背景 */
  outline: none;
  opacity: 0.9;
  transition: opacity 0.3s, background 0.3s;
}

.custom-slider:hover {
  opacity: 1;
}

.custom-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  /* 去除默认样式 */
  appearance: none;
  width: 20px;
  height: 20px;
  background: #fbe8d3;
  /* 滑块颜色 */
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  /* 添加阴影 */
  cursor: pointer;
  transition: background 0.3s, transform 0.3s;
}

.custom-slider::-webkit-slider-thumb:hover {
  background: #f85f73;
  /* 鼠标悬停变色 */
  transform: scale(1.2);
  /* 鼠标悬停放大 */
}

.custom-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: rgb(87, 38, 63);
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: background 0.3s, transform 0.3s;
}

.custom-slider::-moz-range-thumb:hover {
  background: #f85f73;
  transform: scale(1.2);
}
</style>
