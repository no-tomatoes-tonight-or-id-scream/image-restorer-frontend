<template>
  <button class="btn" @click="emitDownload" v-if="canDownload">
    <el-icon class="icon-style">
      <download />
    </el-icon>
    <span class="text-style">下载图片</span>
  </button>
</template>

<script>
import { Download } from "@element-plus/icons-vue";

export default {
  name: "DownloadButton",
  props: {
    canDownload: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    Download,
  },
  emits: ["DownloadRequest"],
  methods: {
    emitDownload() {
      // 向父组件发送下载事件信号
      this.$emit("DownloadRequest");
      console.log("send signal");
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
