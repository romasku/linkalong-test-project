<template>
  <div id="app">
    <div id="nav-bar">
      <div class="content">
        <router-link to="/">Example app for sentence relations studying</router-link>
      </div>
    </div>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class App extends Vue {

}
</script>

<style lang="scss">
body {
  margin: 0;
  font-family: sans-serif;
}

.content {
  max-width: 800px;
  margin: 0 auto;
}

#nav-bar {
  border-bottom: solid 1px black;
  padding: 50px 10px;
  a {
    display: block;
    width: 100%;
    padding: 10px;
    text-decoration: none;
    color: black;
    font-size: 36px;
    font-weight: bold;
    transition: background-color 0.2s;
    &:hover {
      background: lightgray;
    }
  }
}
</style>
