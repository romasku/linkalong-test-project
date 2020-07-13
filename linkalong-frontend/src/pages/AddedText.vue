<template>
  <div>
    <h2>Text:</h2>
    <p v-if="text == null">Loading...</p>
    <p v-else-if="!text.processed">Text is still being processed, please wait...</p>
    <div v-else>
      <p v-for="paragraph in text.paragraphs" :key="paragraph">
        <span class="sentence" v-for="sentence in paragraph.sentences" :key="sentence.id"
              v-on:click="goToSentencePage(sentence)">
          {{sentence.content}}
        </span>
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { API, FullText, Sentence } from '@/api'

@Component
export default class AddedText extends Vue {
  text: FullText | null = null;
  loadTimeoutHandle: number | null = null;

  reloadText () {
    // TODO: add check that url contains number
    API.getText(Number.parseInt(this.$route.params.id)).then(text => {
      this.text = text
      if (!text.processed) {
        this.loadTimeoutHandle = setTimeout(() => this.reloadText(), 1000)
      }
    })
  }

  goToSentencePage (sentence: Sentence) {
    this.$router.push(`/sentence/${sentence.id}`)
  }

  beforeMount () {
    this.reloadText()
  }

  beforeDestroy () {
    if (this.loadTimeoutHandle != null) {
      clearTimeout(this.loadTimeoutHandle)
    }
  }
}
</script>

<style scoped lang="scss">
  .sentence {
    cursor: pointer;
    &:hover {

      &:nth-child(5n+1) {
        background-color: red;
      }

      &:nth-child(5n+2) {
        background-color: green;
      }

      &:nth-child(5n+3) {
        background-color: blue;
      }

      &:nth-child(5n+4) {
        background-color: yellow;
      }

      &:nth-child(5n) {
        background-color: grey;
      }
    }
  }
</style>
