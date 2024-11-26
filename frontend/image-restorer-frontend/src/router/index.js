import {createRouter, createWebHashHistory, createWebHistory} from "vue-router";
import Home from "@/views/Home.vue";
import ImageProcessing from "@/views/ImageProcessing.vue";

const routes = [
    {
        path: "/",
        name: "Home",
        component: ()=>import("@/views/Home.vue"),
    },
    {
        path: "/processing",
        name: "ImageProcessing",
        component: ()=>import("@/views/ImageProcessing.vue"),
    },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

export default router;
