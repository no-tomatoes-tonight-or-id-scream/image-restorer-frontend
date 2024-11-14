<template>
  <div class="relative flex items-center justify-center w-full h-full bg-gray-100 rounded-2xl overflow-hidden">
    <!-- Image upload button -->
    <button class="upload-btn" @click="triggerFileInput">Upload Image</button>

    <!-- Hidden file input -->
    <input
        id="fileInput"
        type="file"
        accept="image/*"
        class="file-input"
        @change="uploadImage"
    />

    <!-- The uploaded image will be placed here -->
    <img v-if="imageSrc" :src="imageSrc" alt="Uploaded Image" class="absolute top-1/2 right-0 transform -translate-y-1/2 w-3/4 h-auto object-cover rounded-lg" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      imageSrc: null,
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    uploadImage(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imageSrc = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    }
  }
};
</script>

<style scoped>
.upload-btn {
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  z-index: 10;
}

.upload-btn:hover {
  background-color: #45a049;
}

.upload-btn:focus {
  outline: none;
}

.file-input {
  display: none;
}
</style>
