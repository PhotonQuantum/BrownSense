<template>
    <v-container>
		<v-card
			class="mx-auto"
			tile
			elevation = 1
		>
			<v-card-text class="text--primary">
				<div>The <strong>BrownSense</strong> is an <a href="https://github.com/PhotonQuantum/BrownSense" target="_blank">open-source</a> IoT platform for toilet environment monitoring. Data are collected from Raspberry Pi in our dormitory. It is our final practical project of the course <strong>Introduction to Engineering(ME116)</strong> of <a href="https://www.sjtu.edu.cn/" target="_blank">Shanghai Jiao Tong University</a>. </div>
			</v-card-text>
		</v-card>
		<br>
		<v-expansion-panels
			v-model="panel"
			multiple
			accordion
		>
			<v-expansion-panel>
			<v-expansion-panel-header><h2>Introduction</h2></v-expansion-panel-header>
			<v-expansion-panel-content class="ma-2">
				The air in our dormitory smells unbearable due to the lack of ventilators in the toilet. Then we discussed and decided to install a ventilator and meanwhile set up this platform to make full use of the ventilator. 
				<br><br>
				The material device contains a Hydrogen Sulfide sensor and an Ammonia sensor in it, and this platform is able to exhibit the instant concentration data of the two gases. Not only can it automatically turn on/off the ventilator according to the data, but you can also control the ventilator remotely through this platform as you like. Besides, you can add in more devices linked to this platform which makes it possible for you to manage a number of devices at the same time. You can certainly delete them when needed.
				<br><br>
				It took us about 2 months to build the platform and materialize the device, from Nov.2019 to Dec.2019.
			</v-expansion-panel-content>
			</v-expansion-panel>
			
			<v-expansion-panel>
			<v-expansion-panel-header><h2>Sensors and Devices</h2></v-expansion-panel-header>
			<v-expansion-panel-content class="ma-2">
				<li><a href="https://www.raspberrypi.org/products/raspberry-pi-4-model-b/" target="_blank">Raspberry Pi 4 Model B</a></li>
				<li><a href="https://www.waveshare.com/wiki/High-Precision_AD/DA_Board" target="_blank">High-Precision AD/DA Board</a></li>
				<li><a href="https://www.winsensor.com/ctbdt/MQ136lhqcgq_18.html" target="_blank">MQ-136 Gas Sensor for Hydrogen Sulfide</a></li>
				<li><a href="https://www.winsensor.com/ctbdt/MQ137aqcgq_19.html" target="_blank">MQ-137 Gas Sensor for Ammonia</a></li>
			</v-expansion-panel-content>
			</v-expansion-panel>
			
			<v-expansion-panel>
			<v-expansion-panel-header><h2>Milestone</h2></v-expansion-panel-header>
			<v-expansion-panel-content> 
				<li class="ma-2"><v-chip label color="secondary">Oct 10, 2019</v-chip> Set up the project.Preliminarily determine the implementation scheme. </li>
				<li class="ma-2"><v-chip label color="secondary">Oct 14, 2019</v-chip> Carry out feasibility analysis and complete technology selection. </li>
				<li class="ma-2"><v-chip label color="secondary">Oct 17, 2019</v-chip> Worked out framework. Purchase the necessary hardware and cloud services.</li>
				<li class="ma-2"><v-chip label color="secondary">Oct 24, 2019</v-chip> Configure Raspberry Pi and cloud environment. Write back-end programs and achieve back-end data access and control operations.</li>
				<li class="ma-2"><v-chip label color="secondary">Oct 31, 2019</v-chip> Write a front-end program to achieve real-time data, charts, deodorization system running status update and view functions.</li>
				<li class="ma-2"><v-chip label color="secondary">Nov 25, 2019</v-chip> Improve the front-end program and supplement other auxiliary functions.</li>
				<li class="ma-2"><v-chip label color="secondary">Nov 30, 2019</v-chip> added/delete devices in the frontend; clean and compact database; lock user out from db operations if not admin.</li>
				<li class="ma-2"><v-chip label color="secondary">Dec 02, 2019</v-chip> Realize the operation function of back-end control terminal deodorization system.</li>
				<li class="ma-2"><v-chip label color="secondary">Dec 05, 2019</v-chip> Beautify the front page.</li>
				<li class="ma-2"><v-chip label color="secondary">Dec 07, 2019</v-chip> Debug the overall operation of the system.Carry out stability test for long running system.</li>
			</v-expansion-panel-content>
			</v-expansion-panel>
			
			<v-expansion-panel>
			<v-expansion-panel-header><h2>Team Members</h2></v-expansion-panel-header>
			<v-expansion-panel-content>
				<div class="ma-2">
				    <v-avatar tile>
						<img src="https://q1.qlogo.cn/g?b=qq&nk=2540534125&s=640">
					</v-avatar> 陈彦宁 <a href="mailto:cy.n01@outlook.com">cy.n01@outlook.com</a>
				</div>
				<div class="ma-2">
					<v-avatar tile>
						<img src="https://q1.qlogo.cn/g?b=qq&nk=826609661&s=640">
					</v-avatar> 刘涵之 <a href="mailto:misaka@sjtu.edu.cn">misaka@sjtu.edu.cn</a><br>
				</div>
				<div class="ma-2">
					<v-avatar tile>
						<img src="https://q1.qlogo.cn/g?b=qq&nk=879960008&s=640">
					</v-avatar> 陈毓仁 <a href="mailto:chenyuren@sjtu.edu.cn">chenyuren@sjtu.edu.cn</a><br>
				</div>
				<div class="ma-2">
					<v-avatar tile>
						<img src="https://q1.qlogo.cn/g?b=qq&nk=1363227303&s=640">
					</v-avatar> 罗景致 <a href="mailto:sjtu.ljz@sjtu.edu.cn">sjtu.ljz@sjtu.edu.cn</a><br>
				</div>
				<div class="ma-2">
					<v-avatar tile>
						<img src="https://q1.qlogo.cn/g?b=qq&nk=2229447547&s=640">
					</v-avatar> 冯驰 <a href="mailto:gdpeaceminusone@sjtu.edu.cn">gdpeaceminusone@sjtu.edu.cn</a><br>
				</div>
			</v-expansion-panel-content>
			</v-expansion-panel>
			
			<v-expansion-panel>
			<v-expansion-panel-header><h2>Documents</h2></v-expansion-panel-header>
			<v-expansion-panel-content class="ma-2">
				<a href="https://github.com/PhotonQuantum/BrownSense/raw/master/documents/project_proposal.pdf">project_proposal.pdf</a>
				
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
		}),
    }

</script>
