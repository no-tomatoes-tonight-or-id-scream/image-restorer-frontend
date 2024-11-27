<template>
  <button class="btn" @click="goToHome" v-if ="canBack">
    <el-icon class="icon-style">
      <upload-filled />
    </el-icon>
    <span class="text-style">返回上传</span>
  </button>
</template>

<script>
import { UploadFilled } from "@element-plus/icons-vue";

export default {
  name: "UploadButton",
  props: {
    canBack: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    UploadFilled,
  },
  methods: {
    goToHome() {
      // 路由跳转到 home
      this.$router.push('/');

    },
  },
};
</script>

<style scoped>
.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fbe8d3;
  border: none;
  border-radius: 40px;
  padding: 10px 15px;
  box-shadow: 0px 6px 6px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  width: 10vw;
}

.btn:hover {
  background-color: #283c63;
}

.icon-style {
  width: 24px;
  height: 24px;
  color: #283c63;
  margin-right: 10px;
  transition: all 0.3s ease;
}

.btn:hover .icon-style {
  color: #ffffff;
}

.text-style {
  font-size: 16px;
  line-height: 24px;
  color: #283c63;
  transition: all 0.3s ease;
}

.btn:hover .text-style {
  color: #ffffff;
}
</style>
