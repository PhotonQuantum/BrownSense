<template>
  <v-container>
    <v-layout
      text-center
      wrap
    >
      <v-flex xs12>
        <v-img
          :src="require('../assets/logo.svg')"
          class="my-3"
          contain
          height="200"
        ></v-img>
      </v-flex>

      <v-flex mb-4>
        <h1 class="display-2 font-weight-bold mb-3">
          Welcome to Vuetify
        </h1>
        <p class="subheading font-weight-regular">
          For help and collaboration with other Vuetify developers,
          <br>please join our online
          <a href="https://community.vuetifyjs.com" target="_blank">Discord Community</a>
        </p>
      </v-flex>

      <v-flex
        mb-5
        xs12
      >
      <line-chart
        styles="width: 800px; height: 600px; position: relative;"
        :chart-data="datacollection"
        :options="chart_options"
        v-if="loaded"
      ></line-chart>
        <h2 class="headline font-weight-bold mb-3">What's next?</h2>

        <v-layout justify-center>
          <a
            v-for="(next, i) in whatsNext"
            :key="i"
            :href="next.href"
            class="subheading mx-3"
            target="_blank"
          >
            {{ next.text }}
          </a>
        </v-layout>
      </v-flex>

      <v-flex
        xs12
        mb-5
      >
        <h2 class="headline font-weight-bold mb-3">Important Links</h2>

        <v-layout justify-center>
          <a
            v-for="(link, i) in importantLinks"
            :key="i"
            :href="link.href"
            class="subheading mx-3"
            target="_blank"
          >
            {{ link.text }}
          </a>
        </v-layout>
      </v-flex>

      <v-flex
        xs12
        mb-5
      >
        <h2 class="headline font-weight-bold mb-3">Ecosystem</h2>

        <v-layout justify-center>
          <a
            v-for="(eco, i) in ecosystem"
            :key="i"
            :href="eco.href"
            class="subheading mx-3"
            target="_blank"
          >
            {{ eco.text }}
          </a>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import LineChart from "./LineChart.js";
export default {
  data: () => ({
    ecosystem: [
      {
        text: 'vuetify-loader',
        href: 'https://github.com/vuetifyjs/vuetify-loader',
      },
      {
        text: 'github',
        href: 'https://github.com/vuetifyjs/vuetify',
      },
      {
        text: 'awesome-vuetify',
        href: 'https://github.com/vuetifyjs/awesome-vuetify',
      },
    ],
    importantLinks: [
      {
        text: 'Documentation',
        href: 'https://vuetifyjs.com',
      },
      {
        text: 'Chat',
        href: 'https://community.vuetifyjs.com',
      },
      {
        text: 'Made with Vuetify',
        href: 'https://madewithvuejs.com/vuetify',
      },
      {
        text: 'Twitter',
        href: 'https://twitter.com/vuetifyjs',
      },
      {
        text: 'Articles',
        href: 'https://medium.com/vuetify',
      },
    ],
    whatsNext: [
      {
        text: 'Explore components',
        href: 'https://vuetifyjs.com/components/api-explorer',
      },
      {
        text: 'Select a layout',
        href: 'https://vuetifyjs.com/layout/pre-defined',
      },
      {
        text: 'Frequently Asked Questions',
        href: 'https://vuetifyjs.com/getting-started/frequently-asked-questions',
      },
    ],
    loaded: false,
    datacollection: null,
    datenow: 999999999,
    chart_options: {
      animation: {
        duration: 0 // general animation time
      },
      elements: {
        line: {
          tension: 0 // disables bezier curves
        }
      },
      scales: {
        xAxes: [
          {
            type: "time",
            time: {
              parser: "X"
            }
          }
        ]
      }
    }
  }),
  components: { LineChart },
  methods: {
    update_time() {
      this.datenow = new Date() / 1000;
    }
  },

  pouch: {
    dev_one() {
      return {
        database: "datagrid",
        selector: {
          device: "1",
          type: "h2s",
          time: { $gt: this.datenow - 100 }
        },
        sort: [{time: "asc"}]
      };
    }
  },
  /*
  computed: {
    datacollection: function() {
      return {
        // labels: ["H2S"],
        datasets: [
          {
            label: "H2S",
            backgroundColor: "#f87979",
            data: this.dev_one.map(x => ({ x: x.time, y: x.info }))
          }
        ]
      };
    }
  },
  */
  watch: {
    dev_one: function(val) {
      this.datacollection = {
        // labels: ["H2S"],
        datasets: [
          {
            label: "H2S",
            backgroundColor: "#f87979",
            data: val.map(x => ({ x: x.time, y: x.data }))
          }
        ]
      };
    }
  },
  props: {
    msg: String
  },

  created: function() {
    this.loaded = false;
    // Send all documents to the remote database, and stream changes in real-time. Note if you use filters you need to set them correctly for pouchdb and couchdb. You can set them for each direction separatly: options.push/options.pull. PouchDB might not need the same filter to push documents as couchdb to send the filtered requested documents.
    this.$pouch.sync("datagrid", "http://localhost:5984/datagrid");
    // this.$pouch.sync("dev_one", "http://localhost:5984/test");
    this.$on("pouchdb-db-created", function() {
      this.loaded = true;
    });
  },
  mounted: function() {
    setInterval(this.update_time, 1000);
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
