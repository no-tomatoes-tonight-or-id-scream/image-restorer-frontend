<template>
  <slot></slot>
  <div class="absolute z=10 inset-0 backdrop-blur-3xl bg-black/10"></div>
</template>

<script>
export default {
  name: "Backdrop",
}
</script>

<style scoped>

</style>
