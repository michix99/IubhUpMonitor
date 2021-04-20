<template>
  <div class="wrapper">
    <img class="error" alt="Error" src="../assets/error.svg" />
    <div class="second-column">
      <h3>{{ website }}</h3>
      <h4>Not reachable since {{ formatedDate }}</h4>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class ErrorMessage extends Vue {
  @Prop() private website!: string;
  @Prop() private date!: Date;

  get formatedDate(): string {
    return this.date.toUTCString();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.wrapper {
  border: 1px solid #ff00008f;
  color: #ff00008f;
  padding: 0 5%;
  text-align: left;
  display: flex;
  justify-content: space-between;
  margin: 10px;
  box-shadow: rgba(100, 0, 3, 0.2) 0px 5px 15px;
}

.second-column {
  margin: 0 20px;
}

.error {
  align-self: flex-start;
  margin-top: 0.7em;
}
</style>
