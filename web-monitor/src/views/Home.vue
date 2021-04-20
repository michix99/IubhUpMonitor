<template>
  <div id="home">
    <!-- <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/> -->
    <h1>Up Monitor</h1>
    <h2>Current Faults</h2>
    <ErrorMessage website="MyTestSite 2" :date="date" />
    <ErrorMessage website="MyTestSite 4" :date="date" />
    <h2>Current Status</h2>
    <Status website="MyTestSite" status="1" />
    <Status website="MyTestSite 2" status="0" />
    <Status website="MyTestSite 3" status="0.5" />
    <Status website="MyTestSite 4" status="0" />
    <h2>7-Days Trend</h2>
    <Charts msg="Charts" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import HelloWorld from '../components/HelloWorld.vue';
import { Charts, ErrorMessage, Status } from '../components/index';

@Component({
  components: {
    HelloWorld,
    Charts,
    ErrorMessage,
    Status,
  },
})
export default class Home extends Vue {
  private date: Date = new Date();
}
</script>

<style scoped lang="scss">
h1 {
  margin-bottom: 30px;
  font-weight: 500;
}
h2 {
  margin-top: 25px;
  font-weight: 500;
  text-align: left;
}
#home {
  // X-Small
  @media (max-width: 575px) {
    margin-left: 0;
    margin-right: 0;
  }
  // Small
  @media (max-width: 767px) and (min-width: 576px) {
    margin-left: 10%;
    margin-right: 10%;
  }
  // Medium
  @media (max-width: 991px) and (min-width: 768px) {
    margin-left: 15%;
    margin-right: 15%;
  }
  // Large
  @media (max-width: 1199px) and (min-width: 992px) {
    margin-left: 20%;
    margin-right: 20%;
  }
  // Extra large
  @media (max-width: 1399px) and (min-width: 1200px) {
    margin-left: 25%;
    margin-right: 25%;
  }
  // Extra extra large
  @media (max-width: 1699px) and (min-width: 1400px) {
    margin-left: 30%;
    margin-right: 30%;
  }
  // Extra extra extra large
  @media (min-width: 1700px) {
    margin-left: 35%;
    margin-right: 35%;
  }
}
</style>
