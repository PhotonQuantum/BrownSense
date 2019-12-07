<template>
    <v-container>
        <v-card
                class="mx-auto"
                tile
                elevation=1
        >
            <v-card-text class="text--primary">
                <div>The <strong>BrownSense</strong> is an <a href="https://github.com/PhotonQuantum/BrownSense"
                                                              target="_blank">open-source</a> IoT platform for toilet
                    environment monitoring. Data are collected from Raspberry Pi in our dormitory. It is our final
                    practical project of the course <strong>Introduction to Engineering(ME116)</strong> of <a
                            href="https://www.sjtu.edu.cn/" target="_blank">Shanghai Jiao Tong University</a>.
                </div>
            </v-card-text>
        </v-card>
        <br>
        <v-expansion-panels
                v-model="panel"
                multiple
                accordion
        >
            <v-expansion-panel>
                <v-expansion-panel-header class="headline">Introduction</v-expansion-panel-header>
                <v-expansion-panel-content class="ma-2">
                    The air in our dormitory smells unbearable due to the lack of ventilators in the toilet. Then we
                    discussed and decided to install a ventilator and meanwhile set up this platform to make full use of
                    the ventilator.
                    <br><br>
                    The material device contains a Hydrogen Sulfide sensor and an Ammonia sensor in it, and this
                    platform is able to exhibit the instant concentration data of the two gases. Not only can it
                    automatically turn on/off the ventilator according to the data, but you can also control the
                    ventilator remotely through this platform as you like. Besides, you can add in more devices linked
                    to this platform which makes it possible for you to manage a number of devices at the same time. You
                    can certainly delete them when needed.
                    <br><br>
                    It took us about 2 months to build the platform and materialize the device, from Nov.2019 to
                    Dec.2019.
                </v-expansion-panel-content>
            </v-expansion-panel>

            <v-expansion-panel>
                <v-expansion-panel-header class="headline">Sensors and Devices</v-expansion-panel-header>
                <v-expansion-panel-content class="ma-2">
                    <li><a href="https://www.raspberrypi.org/products/raspberry-pi-4-model-b/" target="_blank">Raspberry
                        Pi 4 Model B</a></li>
                    <li><a href="https://www.waveshare.com/wiki/High-Precision_AD/DA_Board" target="_blank">High-Precision
                        AD/DA Board</a></li>
                    <li><a href="https://www.winsensor.com/ctbdt/MQ136lhqcgq_18.html" target="_blank">MQ-136 Gas Sensor
                        for Hydrogen Sulfide</a></li>
                    <li><a href="https://www.winsensor.com/ctbdt/MQ137aqcgq_19.html" target="_blank">MQ-137 Gas Sensor
                        for Ammonia</a></li>
                </v-expansion-panel-content>
            </v-expansion-panel>

            <v-expansion-panel>
                <v-expansion-panel-header class="headline">Milestone</v-expansion-panel-header>
                <v-expansion-panel-content>
                    <li class="ma-2">
                        <v-chip label color="secondary">Oct 10, 2019</v-chip>
                        Set up the project. Preliminarily determine the implementation scheme.
                    </li>
                    <li class="ma-2">
                        <v-chip label color="secondary">Oct 14, 2019</v-chip>
                        Carry out feasibility analysis and complete technology selection.
                    </li>
                    <li class="ma-2">
                        <v-chip label color="secondary">Oct 17, 2019</v-chip>
                        Worked out framework. Purchase the necessary hardware and cloud services.
                    </li>
                    <li class="ma-2">
                        <v-chip label color="secondary">Oct 24, 2019</v-chip>
                        Configure Raspberry Pi and cloud environment. Write back-end programs and achieve back-end data
                        access and control operations.
                    </li>
                    <li class="ma-2">
                        <v-chip label color="secondary">Oct 31, 2019</v-chip>
                        Write a front-end program to achieve real-time data, charts, deodorization system running status
                        update and view functions.
                    </li>
                    <li class="ma-2">
                        <v-chip label color="secondary">Nov 25, 2019</v-chip>
                        Improve the front-end program and supplement other auxiliary functions.
                    </li>
                    <li class="ma-2">
                        <v-chip label color="secondary">Nov 30, 2019</v-chip>
                        Added/delete devices in the frontend; clean and compact database; lock user out from db
                        operations if not admin.
                    </li>
                    <li class="ma-2">
                        <v-chip label color="secondary">Dec 02, 2019</v-chip>
                        Realize the operation function of back-end control terminal deodorization system.
                    </li>
                    <li class="ma-2">
                        <v-chip label color="secondary">Dec 05, 2019</v-chip>
                        Beautify the front page.
                    </li>
                    <li class="ma-2">
                        <v-chip label color="secondary">Dec 07, 2019</v-chip>
                        Debug the overall operation of the system. Carry out stability test for long running system.
                    </li>
                </v-expansion-panel-content>
            </v-expansion-panel>

            <v-expansion-panel>
                <v-expansion-panel-header class="headline">Team Members</v-expansion-panel-header>
                <v-expansion-panel-content>
                    <v-list>
                        <template v-for="member in members">
                            <v-list-item :key="member.name">
                                <v-list-item-avatar>
                                    <v-img :src="member.avatar"/>
                                </v-list-item-avatar>
                                <v-list-item-content>
                                    <v-list-item-title v-text="member.name"/>
                                </v-list-item-content>
                                <v-list-item-action>
                                    <v-btn icon :href="'mailto:' + member.mail">
                                        <v-icon color="primary">mdi-email</v-icon>
                                    </v-btn>
                                </v-list-item-action>
                            </v-list-item>
                            <v-divider v-if="member !== members[members.length-1]" :key="member.name" inset/>
                        </template>
                    </v-list>
                </v-expansion-panel-content>
            </v-expansion-panel>

            <v-expansion-panel>
                <v-expansion-panel-header class="headline">Documents</v-expansion-panel-header>
                <v-expansion-panel-content class="ma-2">
                    <v-btn class="mr-5"
                           href="https://github.com/PhotonQuantum/BrownSense/raw/master/documents/project_proposal.pdf">
                        <v-icon left>mdi-file-document</v-icon>
                        Project Proposal
                    </v-btn>
                    <v-btn href="https://raw.githubusercontent.com/PhotonQuantum/BrownSense/master/LICENSE">
                        <v-icon left>mdi-scale-balance</v-icon>
                        License
                    </v-btn>
                </v-expansion-panel-content>
            </v-expansion-panel>
            <v-expansion-panel>
                <v-expansion-panel-header class="headline">Acknowledgements</v-expansion-panel-header>
                <v-expansion-panel-content class="ma-2">
                    The BrownSense project includes the following open source software, namely<br/>
                    <div class="font-weight-light">
                        <template v-for="project in acknowledges">
                            <a :href="project.url" :key="project.name" target="_blank">{{ project.name }}</a><span
                                :key="project.name">, {{ project.description }}, which is licensed under the </span><a
                                :href="project.lic_url" :key="project.name" target="_blank">{{ project.lic }}</a><span
                                :key="project.name">.</span><br :key="project.name"/>
                        </template>
                    </div>
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
    </v-container>
</template>
<script>
    export default {
        created() {
            this.$store.commit("set_nav", [{text: "About", disabled: true}]);
        },
        data: () => ({
            panel: [0],
            members: [
                {
                    avatar: "https://q1.qlogo.cn/g?b=qq&nk=2540534125&s=640",
                    name: "陈彦宁 (Yanning Chen)", mail: "cy.n01@outlook.com"
                },
                {
                    avatar: "https://q1.qlogo.cn/g?b=qq&nk=826609661&s=640",
                    name: "刘涵之 (Hanzhi Liu)", mail: "misaka@sjtu.edu.cn"
                },
                {
                    avatar: "https://q1.qlogo.cn/g?b=qq&nk=879960008&s=640",
                    name: "陈毓仁 (Ruiren Chen)", mail: "chenyuren@sjtu.edu.cn"
                },
                {
                    avatar: "https://q1.qlogo.cn/g?b=qq&nk=1363227303&s=640",
                    name: "罗景致 (Jingzhi Luo)", mail: "sjtu.ljz@sjtu.edu.cn"
                },
                {
                    avatar: "https://q1.qlogo.cn/g?b=qq&nk=2229447547&s=640",
                    name: "冯驰 (Chi Feng)", mail: "gdpeaceminusone@sjtu.edu.cn"
                }
            ],
            acknowledges: [
                {
                    url: "https://vuejs.org/",
                    name: "Vue",
                    description: "the progressive javascript framework",
                    lic_url: "https://raw.githubusercontent.com/vuejs/vue/master/LICENSE",
                    lic: "MIT License"
                },
                {
                    url: "https://vuetifyjs.com/",
                    name: "Vuetify",
                    description: "a material component framework for Vue",
                    lic_url: "https://raw.githubusercontent.com/vuetify/vuetify/master/LICENSE.md",
                    lic: "MIT License"
                },
                {
                    url: "https://couchdb.apache.org/",
                    name: "CouchDB",
                    description: "an open-source document-oriented NoSQL database",
                    lic_url: "https://raw.githubusercontent.com/apache/couchdb/master/LICENSE",
                    lic: "Apache License 2.0"
                },
                {
                    url: "https://pouchdb.com/",
                    name: "PouchDB",
                    description: "an open-source JavaScript database inspired by Apache CouchDB",
                    lic_url: "https://raw.githubusercontent.com/pouchdb/pouchdb/master/LICENSE",
                    lic: "Apache License 2.0"
                },
                {
                    url: "https://github.com/cloudant/python-cloudant",
                    name: "Python Cloudant",
                    description: "the official Cloudant library for Python",
                    lic_url: "https://raw.githubusercontent.com/cloudant/python-cloudant/master/LICENSE",
                    lic: "Apache License 2.0"
                },
                {
                    url: "https://github.com/ul-gh/PiPyADC",
                    name: "PiPyADC",
                    description: "a Python module for interfacing Texas Instruments SPI bus based analog-to-digital converters with the Raspberry Pi",
                    lic_url: "https://github.com/ul-gh/PiPyADC/blob/master/LICENSE",
                    lic: "LGPLv2.1"
                }]
        }),
    }

</script>

