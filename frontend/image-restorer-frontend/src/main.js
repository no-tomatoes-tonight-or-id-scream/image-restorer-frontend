import { createApp } from 'vue'

// 引入 Vuetify 样式和相关组件
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import router from './router';

// 引入 Tailwind CSS
import './assets/tailwind.css'

// 引入主应用组件
import App from './App.vue'

// 创建 Vuetify 实例
const vuetify = createVuetify({
    components,  // 注册 Vuetify 组件
    directives,  // 注册 Vuetify 指令
})

// 创建 Vue 应用并使用 Vuetify 和 Tailwind CSS
createApp(App)
    .use(vuetify)  // 使用 Vuetify 插件
    .use(router)
    .mount('#app')
