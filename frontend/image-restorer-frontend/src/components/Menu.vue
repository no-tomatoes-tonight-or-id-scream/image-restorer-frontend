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
  transition: opacity 1s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active 在某些版本中 */ {
  opacity: 0;
}

.menu-wrapper {
  position: fixed;
  top: 30%; /* 调整菜单的纵向位置 */
  left: 5%; /* 保持在左侧 */
  width: 300px; /* 菜单宽度 */
  padding: 40px;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 10px; /* 圆角 */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2); /* 阴影效果 */
  z-index: 50; /* 提高 z-index 确保不被覆盖 */
}

.menu-item {
  margin-bottom: 15px;
}

label {
  display: block;
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
}

select {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.menu-submit-btn {
  background-color: #28a745; /* 绿色提交按钮 */
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
  width: 100%; /* 提交按钮宽度占满 */
  transition: background-color 0.3s ease;
}

.menu-submit-btn:hover {
  background-color: #218838; /* 悬停时加深绿色 */
}
</style>
