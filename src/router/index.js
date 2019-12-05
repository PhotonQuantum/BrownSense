import Vue from 'vue'
import Router from 'vue-router'
import Summary from '@/components/Summary'
import About from '@/components/About'
import Manage from "@/components/Manage";
import Detail from "@/components/Detail";
import DetailOverview from "../components/DetailOverview";
import Graph from "../components/Graph";
import NotFound from "@/components/NotFound"

Vue.use(Router);
export default new Router({
    mode: 'history',
    routes: [
        {
            path: "/",
            component: Summary
        },
        {
            path: "/device/:id",
            component: Detail,
            children:[
                {
                    path: "",
                    redirect: "overview"
                },
                {
                    path: "overview",
                    component: DetailOverview
                },
                {
                    path: "graph",
                    component: Graph
                }
            ]
        },
        {
            path: "/about",
            component: About
        },
        {
            path: "/manage",
            component: Manage
        },
        {
            path: "/404",
            component: NotFound
        },
        {
            path: "*",
            redirect: "/404"
        }
    ]
})