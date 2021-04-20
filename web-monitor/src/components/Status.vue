<template>
  <div class="wrapper">
    <div class="header" v-on:click="toggleExpand">
      <div class="title">
        <img
          v-if="status == 0"
          class="icon"
          alt="Error"
          src="../assets/error.svg"
        />
        <img
          v-else-if="status > 0 && status < 1"
          class="icon"
          alt="Warning"
          src="../assets/warning.svg"
        />
        <img
          v-else-if="status == 1"
          class="icon"
          alt="Ok"
          src="../assets/ok.svg"
        />
        <h3>{{ website }}</h3>
      </div>
      <div class="expandButton">
        <img v-bind:class="{ expanded: isExpanded }" src="../assets/down.svg" />
      </div>
    </div>
    <div v-show="isExpanded" class="content">
      <div class="first-column">
        <div>
          <span>Availability: </span>
          <span class="metrics">{{ availability }}</span>
        </div>
        <div>
          <span>Response Time: </span>
          <span class="metrics">{{ responseTime }}</span>
        </div>
        <div>
          <span>Last Failure: </span>
          <span class="metrics">{{ lastFailure }}</span>
        </div>
      </div>
      <div class="second-column">
        <span v-if="status == 0">Status: down</span>
        <span v-else-if="status > 0 && status < 1">Status: pending</span>
        <span v-else-if="status == 1">Status: up</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class Status extends Vue {
  @Prop() private website!: string;
  @Prop() private status!: number;
  private isExpanded = false;

  get availability(): string {
    return `${Math.round(Math.random() * 10000) / 100}%`;
  }

  get responseTime(): string {
    return `${Math.round(Math.random() * 1000)}ms`;
  }

  get lastFailure(): string {
    return `${Math.round(Math.random() * 10)} weeks ago`;
  }

  toggleExpand(): void {
    this.isExpanded = !this.isExpanded;
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.wrapper {
  margin: 20px 10px;
}

.header {
  display: flex;
  border-bottom: 2px solid;
  justify-content: space-between;
  &:hover {
    cursor: pointer;
  }
  .title {
    display: flex;
  }
  h3 {
    font-weight: 100;
    margin: 0 0 5px 10px;
  }
}

.content {
  margin: 5px 0;
  display: flex;
  justify-content: space-between;
  .first-column {
    display: flex;
    flex-direction: column;
    text-align: left;
    color: #ffffff9a;
    div {
      display: flex;
      justify-content: space-between;
    }
    .metrics {
      padding-left: 5rem;
    }
  }
  .second-column {
    display: flex;
    text-align: right;
  }
  span {
    margin: 5px 0;
  }
}

img {
  height: 25px;
}

.expanded {
  transform: rotate(180deg);
}

.expandButton {
  border: none;
  background: transparent;

  &:hover {
    background-color: gray;
  }
  &:focus {
    outline: none;
  }
}
</style>
