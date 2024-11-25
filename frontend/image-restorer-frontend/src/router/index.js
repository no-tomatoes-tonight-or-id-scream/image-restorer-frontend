import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import ImageProcessing from "@/views/ImageProcessing.vue";

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home, // 首页
    },
    {
        path: '/process',
        name: 'ImageProcessing',
        component: ImageProcessing, // 图片处理页
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
