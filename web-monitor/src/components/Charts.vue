<template>
  <div class="tabbed">
    <input checked="checked" id="chart1" type="radio" name="tabs" />
    <input id="chart2" type="radio" name="tabs" />
    <input id="chart3" type="radio" name="tabs" />

    <nav>
      <label for="chart1">Availability</label>
      <label for="chart2">Response Time</label>
      <label for="chart3">Failure Rate</label>
    </nav>

    <figure>
      <div id="dummy-chart" class="chart1"></div>
      <div class="chart2">…</div>
      <div class="chart3">…</div>
    </figure>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Chart } from 'frappe-charts/dist/frappe-charts.min.esm';

@Component
export default class Charts extends Vue {
  mounted() {
    const chart = new Chart('#dummy-chart', {
      data: {
        labels: [
          '12am-3am',
          '3am-6am',
          '6am-9am',
          '9am-12pm',
          '12pm-3pm',
          '3pm-6pm',
          '6pm-9pm',
          '9pm-12am',
        ],

        datasets: [
          {
            name: 'Some Data',
            chartType: 'bar',
            values: [25, 40, 30, 35, 8, 52, 17, -4],
          },
          {
            name: 'Another Set',
            chartType: 'bar',
            values: [25, 50, -10, 15, 18, 32, 27, 14],
          },
          {
            name: 'Yet Another',
            chartType: 'line',
            values: [15, 20, -3, -15, 58, 12, -17, 37],
          },
        ],

        // yMarkers: [
        //   { label: 'Marker', value: 70, options: { labelPos: 'left' } },
        // ],
        // yRegions: [
        //   {
        //     label: 'Region',
        //     start: -10,
        //     end: 50,
        //     options: { labelPos: 'right' },
        //   },
        // ],
      },

      title: 'My Awesome Chart',
      type: 'axis-mixed', // or 'bar', 'line', 'pie', 'percentage'
      height: 300,
      colors: ['purple', '#ffa3ef', 'light-blue'],

      tooltipOptions: {
        formatTooltipX: (d: string) => (d + '').toUpperCase(),
        formatTooltipY: (d: string) => d + ' pts',
      },
    });

    // chart.export();
  }
}
</script>

<style lang="scss">
.y-value-text {
  fill: #ffffff;
}

.x-value-text {
  fill: #ffffff;
}

text {
  fill: #ffffff;
}

.chart-container .legend-dataset-text {
  fill: #ffffff;
}

.tabbed figure { 
  display: block; 
  margin-left: 0; 
  clear: both;
}

.tabbed > input,
.tabbed figure > div { display: none; }

.tabbed figure > div {
  padding: 20px;
  width: 100%;
  border: 1px solid silver;
  line-height: 1.5em;
  letter-spacing: 0.3px;
  color: #ffffff;
  -webkit-box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
  -moz-box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
  box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
}

#chart1:checked ~ figure .chart1,
#chart2:checked ~ figure .chart2,
#chart3:checked ~ figure .chart3 { display: block; }

nav label {
  float: left;
  padding: 15px 15px;
  border-top: 1px solid silver;
  border-right: 1px solid silver;
  color: #eee;
}

nav label:nth-child(1) { 
  border-left: 1px solid silver;
}
nav label:hover {
  background: gray;
}

#chart1:checked ~ nav label[for="chart1"],
#chart2:checked ~ nav label[for="chart2"],
#chart3:checked ~ nav label[for="chart3"] {
  color: #ffffff;
  position: relative;
  border-bottom: none;
}

#chart1:checked ~ nav label[for="chart1"]:after,
#chart2:checked ~ nav label[for="chart2"]:after,
#chart3:checked ~ nav label[for="chart3"]:after {
  content: "";
  display: block;
  position: absolute;
  height: 2px;
  width: 100%;
  background: #2e2c2c;
  left: 0;
  bottom: -1px;
}
</style>
