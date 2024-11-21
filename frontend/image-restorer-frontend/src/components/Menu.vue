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
          <option value="RealESRGAN_RealESRGAN_x4plus_4x.pth">RealESRGAN_RealESRGAN_x4plus_4x</option>
          <option value="RealESRGAN_RealESRGAN_x4plus_anime_6B_4x.pth">RealESRGAN_RealESRGAN_x4plus_anime_6B_4x</option>
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
  },
  data() {
    return {
      formData: {
        modelType: "RealESRGAN_RealESRGAN_x4plus_4x.pth", // 默认模型
        scale: 2, // 默认放大倍数
      },
    };
  },

  methods: {
    checkTaskStatus(task_id) {
      const statusUrl = `https://img.jrhim.com/get_status?task_id=${task_id}`;
      const testurl = `http://127.0.0.1:5000/get_status?task_id=${task_id}`;

      // 查询任务状态
      axios.get(testurl)
          .then((response) => {
            const { status } = response.data;

            console.log("任务状态:", status);

            // 如果任务完成，获取结果
            if (status === "completed") {
              this.getResultImg(task_id);
            } else if (status === "error") {
              console.error("任务发生错误!");
            } else {
              console.log("任务正在处理中...");
              // 继续轮询状态，间隔一段时间后再查询
              setTimeout(() => this.checkTaskStatus(task_id), 5000); // 每 5 秒查询一次
            }
          })
          .catch((error) => {
            console.error("查询任务状态失败:", error);
          });
    },

    getResultImg(task_id) {
      const resultUrl = `https://img.jrhim.com/get_result?task_id=${task_id}`;
      const testurl = `http://127.0.0.1:5000/get_result?task_id=${task_id}`;
      // 请求获取结果图像
      axios.get(testurl, { responseType: 'arraybuffer' })  // Use 'arraybuffer' for binary data
          .then((response) => {
            // 将图像数据转换为 Base64
            const base64Image = `data:image/jpeg;base64,${Buffer.from(response.data, 'binary').toString('base64')}`;

            // 在控制台打印 Base64 图像数据
            console.log("图像 Base64 数据:", base64Image);

            // 如果需要，可以动态添加到页面上显示
            const imgElement = document.createElement('img');
            imgElement.src = base64Image;
            document.body.appendChild(imgElement); // 动态插入页面
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


      console.log("提交数据:", postData);
      console.log("image", this.uploadedFile);
      console.log("target_scale", this.formData.scale);
      console.log("pretrained_model_name", this.formData.modelType);

      //https://img.jrhim.com/process?
      // 使用 axios 发送 POST 请求
      axios.post(`http://127.0.0.1:5000/process?${queryString}`, postData)
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


  },
};

</script>

<style scoped>
.menu-wrapper {
  position: fixed;
  top: 20%;
  left: 5%;
  width: 400px;
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
