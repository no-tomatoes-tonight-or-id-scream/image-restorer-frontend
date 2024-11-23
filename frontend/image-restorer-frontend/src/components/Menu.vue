<template>
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
</template>

<script>
import axios, {AxiosHeaders as Buffer} from 'axios';
import {ElLoading} from "element-plus";


export default {
  name: "Menu",
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
    uploadedFile: {
      type: File,
      required: true,
    },
    baseUrl: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      formData: {
        modelType: "RealESRGAN_RealESRGAN_x4plus_4x.pth", // 默认模型
        scale: 2, // 默认放大倍数
      },
      modelList: null,
      checkCnt: 0,
      loadingInstance: null,
    };
  },
  mounted()
  {
    this.getModelList();
  },
  methods: {
    checkTaskStatus(task_id) {
      const targetUrl = `${this.baseUrl}get_status?task_id=${task_id}`;
      const loadingInstance = ElLoading.service({ fullscreen: true, text: 'Loading...' });
      // 查询任务状态
      axios.get(targetUrl)
          .then((response) => {
            const { status } = response.data;

            console.log("任务状态:", status);

            // 如果任务完成，获取结果
            if (status === "completed") {
              this.getResultImg(task_id);
            } else if (status === "error") {
              console.error("任务发生错误!");
            } else {
              this.checkCnt ++;
              console.log("查询次数:", this.checkCnt);
              if (this.checkCnt >= 60) {
                //超时 强行get或者是其他的逻辑
                this.getResultImg(task_id);
                this.checkCnt = 0; // 重置
              } else {
                console.log("Task is still processing...");
                setTimeout(() => this.checkTaskStatus(task_id), 2000);  // Check again after 2 seconds
              }
            }
          })
          .catch((error) => {
            console.error("查询任务状态失败:", error);
          });
    },

    getResultImg(task_id) {
      //使用已有图片 测试失败原因是否包含 等待时间小于服务端图片处理时间
      //task_id = "9fb7e4fb-a6fc-4850-b6eb-5f0c8239654e"
      // 处理时间与上传的图片、模型的选择均有关
      const targetUrl = `${this.baseUrl}get_result?task_id=${task_id}`;

      // 请求获取结果图像
      axios.get(targetUrl, { responseType: 'arraybuffer' })  // Use 'arraybuffer' for binary data
          .then((response) => {
            // 将图像数据转换为 Base64
            // 将 ArrayBuffer 转换为二进制字符串
            const binary = new Uint8Array(response.data)
                .reduce((acc, byte) => acc + String.fromCharCode(byte), "");

            // 将二进制字符串编码为 Base64
            const base64Image = `data:image/jpeg;base64,${btoa(binary)}`;

            this.$emit("pics-upload",base64Image);

          })
          .catch((error) => {
            console.error("下载结果图像失败:", error);
          });
    },

    handleSubmit() {
      const params = {
        target_scale: this.formData.scale,
        pretrained_model_name: this.formData.modelType
      };

      // 构建查询字符串
      const queryString = new URLSearchParams(params).toString();

      // 创建 FormData 对象，只包含图像文件
      const postData = new FormData();
      postData.append("image", this.uploadedFile); // 上传图片文件

      console.log("提交表单的内容: ")
      for (const [key, value] of postData.entries()) {
        console.log(`${key}:`, value);
      }

      console.log("image", this.uploadedFile);
      console.log("target_scale", this.formData.scale);
      console.log("pretrained_model_name", this.formData.modelType);

      const targetUrl = `${this.baseUrl}process?${queryString}`;
      // 使用 axios 发送 POST 请求
      axios.post(targetUrl, postData)
          .then((response) => {
            // 从响应中提取 status 和 task_id
            const { status, task_id } = response.data;

            // 打印 status 和 task_id
            console.log("status:", status);
            console.log("task_id:", task_id);

            // 查询任务状态
            this.checkTaskStatus(task_id);
          })
          .catch((error) => {
            // 错误处理
            console.error("错误:", error);
          });
    },

    //从后端中获取模型列表
    getModelList()
    {
      const targetUrl = this.baseUrl + "get_model_list";
      // console.log("基础路径",targetUrl);
      axios.get(targetUrl)
          .then(
              (response) => {
                // let modelValues = Object.values(response.data);
                // let modelKeys = Object.keys(response.data);
                this.modelList = response.data;
              }
          )
          .catch(
              (error)=>
              {
                console.log("请求模型列表出错！出错信息：",error);
              }
          )
    }

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

.select {
  border-color: #ddd;
  transition: border-color 0.3s ease;
}

.select:focus {
  border-color: #66afe9;
  outline: none;
}
</style>
