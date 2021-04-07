<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <router-view />
  </div>
</template>

<style lang="scss">
html {
  background: #2e2c2c;
  // for firefox support
  scrollbar-color: #554f4f #2e2c2c;
  scrollbar-width: auto;
}

#app {
  color: #ffffff;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

#nav {
  padding: 30px 0 15px 0;

  a {
    font-weight: bold;
    color: #ffffff;

    &.router-link-exact-active {
      color: #2086dabb;
    }
  }
}

// for chrome and safari
::-webkit-scrollbar {
  width: 12px;
}

::-webkit-scrollbar-track {
  background: #2e2c2c;
  // border: 2px solid #554f4f;
}

::-webkit-scrollbar-thumb {
  background: #554f4f;
}

</style>
