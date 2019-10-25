import Vue from 'vue'
import Router from 'vue-router'
import Summary from '@/components/Summary'
import About from '@/components/About'
import Detail from '@/components/Detail'
import DeviceDetail from '@/components/DeviceDetail'
Vue.use(Router)
export default new Router({
    routes:[
        {
            path: "/",
            redirect: "/summary"
        },
        {
            path: "/summary",
            component: Summary
        },
        {
            path: "/about",
            component: About
        },
        {
            path: "/Detail",
            component: Detail,
            children: [
                {
                    path: ":id",
                    component: DeviceDetail
                }
            ]
        }
    ]
})