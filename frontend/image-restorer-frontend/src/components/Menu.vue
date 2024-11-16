<template>
  <transition name="fade">
    <div v-if="isVisible" class="menu-wrapper">
      <form @submit.prevent="handleSubmit">
        <div class="menu-item">
          <label for="modelType">模型类型:</label>
          <select id="modelType" v-model="formData.modelType">
            <option value="modelA">模型 A</option>
            <option value="modelB">模型 B</option>
            <option value="modelC">模型 C</option>
          </select>
        </div>
        <div class="menu-item">
          <label for="denoiseLevel">去噪强度:</label>
          <select id="denoiseLevel" v-model="formData.denoiseLevel">
            <option value="low">低</option>
            <option value="medium">中</option>
            <option value="high">高</option>
          </select>
        </div>
        <button type="submit" class="menu-submit-btn">提交</button>
      </form>
    </div>
  </transition>
</template>

<script>
export default {
  name: "Menu",
  props: {
    isVisible: {
      type: Boolean,
      default: false
    }
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
      // 模拟 POST 请求
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
.fade-enter-active, .fade-leave-active {
  transition: opacity 1s ease-in-out;
}
.fade-enter, .fade-leave-to /* .fade-leave-active 在某些版本中 */ {
  opacity: 0;
}

.menu-wrapper {
  position: fixed;
  top: 20%;
  left: 5%;
  width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.1); /* 设置透明背景 */
  border-radius: 15px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15); /* 更柔和的阴影 */
  backdrop-filter: blur(10px); /* 背景模糊效果 */
  z-index: 50;
  animation: fadeIn 0.5s ease-out;
}

.menu-item {
  margin-bottom: 25px;
}

label {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

select {
  width: 100%;
  padding: 12px 16px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.15); /* 选择框背景保持不透明 */
  transition: border-color 0.3s ease;
}

select:focus {
  border-color: #66afe9;
  outline: none;
}

.menu-submit-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 12px 20px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.menu-submit-btn:hover {
  background-color: #218838;
  transform: translateY(-2px);
}

.menu-submit-btn:active {
  transform: translateY(0);
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
