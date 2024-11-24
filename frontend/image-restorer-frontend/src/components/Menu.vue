<template>
  <div>
    <div v-if="isVisible" class="menu-wrapper">
      <form @submit.prevent="handleSubmit">
        <!-- 模型选择 -->
        <div class="menu-item">
          <label for="modelType" class="label">
            <span class="label-text text-lg font-semibold">模型:</span>
          </label>
          <select
              id="modelType"
              v-model="formData.modelType"
              class="select select-bordered w-full"
          >
            <option
                v-for="(value, key) in modelList"
                :key="key"
                :value="value"
            >
              {{ key }}
            </option>
          </select>
        </div>
        <!-- 放大倍数 -->
        <div class="menu-item">
          <label for="scale" class="label">
            <span class="label-text text-lg font-semibold">放大倍数:</span>
          </label>
          <select
              id="scale"
              v-model.number="formData.scale"
              class="select select-bordered w-full"
          >
            <option :value="2">2</option>
            <option :value="4">4</option>
            <option :value="5">5</option>
            <option :value="8">8</option>
          </select>
        </div>
        <button type="submit" class="btn btn-success w-full text-lg">
          提交
        </button>
      </form>
    </div>

    <!-- 加载界面 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="flex flex-col items-center justify-center h-screen">
        <div class="loading loading-spinner w-16 h-16"></div>
        <p class="text-white text-xl mt-4">处理中，请稍候...</p>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

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
    // isLoading: {
    //   type: Boolean,
    //   default: false,
    //   required: true,
    // },
  },
  emits: ["pics-upload"], // 声明事件
  data() {
    return {
      formData: {
        modelType: "RealESRGAN_RealESRGAN_x4plus_4x.pth", // 默认模型
        scale: 2, // 默认放大倍数
      },
      modelList: null,
      checkCnt: 0,
      isLoading: false, // 加载状态
    };
  },
  mounted() {
    this.getModelList();
  },
  methods: {
    checkTaskStatus(task_id) {
      const targetUrl = `${this.baseUrl}get_status?task_id=${task_id}`;
      axios
          .get(targetUrl)
          .then((response) => {
            const {status} = response.data;
            console.log("任务状态:", status);

            if (status === "completed") {
              //this.isLoading = false; // 加载完成后隐藏
              this.getResultImg(task_id);
              setTimeout(() => {
                this.isLoading = false; // 加载完成后隐藏
              }, 1500); // 等待 2000 毫秒（2 秒）
            } else if (status === "error") {
              this.isLoading = false;
              console.error("任务发生错误!");
            } else {
              this.checkCnt++;
              if (this.checkCnt >= 60) {
                this.getResultImg(task_id);
                this.checkCnt = 0;
              } else {
                setTimeout(() => this.checkTaskStatus(task_id), 2000);
              }
            }
          })
          .catch((error) => {
            this.isLoading = false;
            console.error("查询任务状态失败:", error);
          });
    },

    getResultImg(task_id) {
      const targetUrl = `${this.baseUrl}get_result?task_id=${task_id}`;
      axios
          .get(targetUrl, {responseType: "arraybuffer"})
          .then((response) => {
            const binary = new Uint8Array(response.data).reduce(
                (acc, byte) => acc + String.fromCharCode(byte),
                ""
            );
            const base64Image = `data:image/jpeg;base64,${btoa(binary)}`;
            this.$emit("pics-upload", base64Image);
          })
          .catch((error) => {
            console.error("下载结果图像失败:", error);
          });
    },

    handleSubmit() {
      this.isLoading = true; // 开始加载
      const params = {
        target_scale: this.formData.scale,
        pretrained_model_name: this.formData.modelType,
      };
      const queryString = new URLSearchParams(params).toString();
      const postData = new FormData();
      postData.append("image", this.uploadedFile);

      const targetUrl = `${this.baseUrl}process?${queryString}`;
      axios
          .post(targetUrl, postData)
          .then((response) => {
            const {status, task_id} = response.data;
            console.log("status:", status, "task_id:", task_id);
            this.checkTaskStatus(task_id);
          })
          .catch((error) => {
            this.isLoading = false;
            console.error("错误:", error);
          });
    },

    getModelList() {
      const targetUrl = this.baseUrl + "get_model_list";
      axios
          .get(targetUrl)
          .then((response) => {
            this.modelList = response.data;
          })
          .catch((error) => {
            console.log("请求模型列表出错！出错信息：", error);
          });
    },
  },
};
</script>

<style scoped>
.menu-wrapper {
  position: fixed;
  top: 20%;
  left: 2%;
  max-width: 400px;
  width: 30vw;
  padding: 30px;
  background: rgba(255, 255, 255, 0.2); /* 半透明背景 */
  border-radius: 12px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15); /* 柔和阴影 */
  z-index: 50;
  backdrop-filter: blur(10px); /* 背景模糊 */
}

.menu-item {
  margin-bottom: 20px;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(255, 255, 255, 0.2); /* 背景遮罩 */
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px); /* 背景模糊 */
}
</style>
