<template>
  <div v-if="isVisible" class="menu-wrapper">
    <form @submit.prevent="handleSubmit">
      <div class="menu-item">
        <label for="modelType" class="label">
          <span class="label-text text-lg font-semibold">模型类型:</span>
        </label>
        <select
            id="modelType"
            v-model="formData.modelType"
            class="select select-bordered w-full"
        >
          <option value="modelA">模型 A</option>
          <option value="modelB">模型 B</option>
          <option value="modelC">模型 C</option>
        </select>
      </div>
      <div class="menu-item">
        <label for="denoiseLevel" class="label">
          <span class="label-text text-lg font-semibold">去噪强度:</span>
        </label>
        <select
            id="denoiseLevel"
            v-model="formData.denoiseLevel"
            class="select select-bordered w-full"
        >
          <option value="low">低</option>
          <option value="medium">中</option>
          <option value="high">高</option>
        </select>
      </div>
      <button type="submit" class="btn btn-success w-full text-lg">
        提交
      </button>
    </form>
  </div>
</template>

<script>
export default {
  name: "Menu",
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      formData: {
        modelType: "modelA", // 默认选择
        denoiseLevel: "low", // 默认选择
      },
    };
  },
  methods: {
    handleSubmit() {
      const postData = {
        modelType: this.formData.modelType,
        denoiseLevel: this.formData.denoiseLevel,
      };
      console.log("提交数据:", postData);
      fetch("https://placeholder.url/post", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(postData),
      })
          .then((response) => response.json())
          .then((data) => {
            console.log("成功:", data);
          })
          .catch((error) => {
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
