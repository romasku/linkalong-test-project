<template>
  <div class="add-form" v-bind:class="{ uploading: uploading }">
    <label :for="textareaId" v-if="!uploading">
      <template v-if="!uploading">
        Enter text to upload:
      </template>
      <template v-else>
        Upload is in progress...
      </template>
    </label>
    <textarea :id="textareaId" rows="4" v-model="text" :disabled="uploading"></textarea>
    <button v-on:click="uploadText" :disabled="uploading">Upload text</button>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { API } from '@/api'

@Component
export default class AddText extends Vue {
  textareaId = `add-text-area${Math.random()}`;
  text = 'Enter your text here';
  uploading = false;

  uploadText () {
    this.uploading = true
    API.uploadText(this.text).then(text =>
      this.$router.push(`/text/${text.id}`)
    )
  }
}
</script>

<style scoped lang="scss">
  .add-form {
    margin: 20px 0;
    label {
      display: block;
      margin-bottom: 10px;
    }
    textarea {
      width: 100%;
      padding: 4px;
      font-size: 14px;
      margin-bottom: 10px;
    }
    button {
      display: block;
      width: 200px;
      height: 50px;
      margin-left: auto;
      border: 1px solid black;
      border-radius: 0;
      background: white;
      font-size: 20px;
      transition: background-color 0.2s;
      cursor: pointer;
      &:hover {
        background: lightgray;
      }
      &:active {
        background: gray;
      }
    }
  }
</style>
