<template>
  <div>
    <h2>Similar sentences lookup:</h2>
    <h3 v-if="sentence === null">Loading...</h3>
    <h3 class="main-sentence" v-else>{{sentence.content}}</h3>
    <h3>Similar sentences:</h3>
    <p v-if="similar === null">Still loading...</p>
    <div v-else>
      <div class="similar-option" v-for="sentence in similar" :key="sentence.id">
        <p class="sentence">{{sentence.content}}</p>
        <p>This sentence was found in text:</p>
        <p class="text" v-on:click="goToText(sentence.text)">{{sentence.text.preview}}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { API, AppText, ListedSentence } from '@/api'

@Component
export default class SentenceLookup extends Vue {
  sentence: ListedSentence | null = null;
  similar: ListedSentence[] | null = null;

  beforeMount () {
    API.getSimilar(Number.parseInt(this.$route.params.id)).then(response => {
      this.sentence = response.sentence
      this.similar = response.similar_sentences
    })
  }

  goToText (text: AppText) {
    this.$router.push(`/text/${text.id}`)
  }
}
</script>

<style scoped lang="scss">
  .main-sentence {
    border-bottom: 2px solid black;
  }
  .similar-option {
    border-left: 4px solid black;
    padding-left: 16px;
    margin-bottom: 20px;
    .sentence {
      margin-left: 20px;
      border-bottom: 1px solid black;
    }
    .text {
      transition: background-color 0.2s;
      cursor: pointer;
      &:hover {
        background: lightgray;
      }
    }
  }
</style>
