<template>
  <div id="app" class="absolute w-screen h-screen z-0">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
}
</style>
