<template>
  <div>
    <add-text></add-text>
    <div v-if="texts !== null">
      <h2>Uploaded texts:</h2>
      <p class="uploaded-text" v-for="text of texts" :key="text.id" v-on:click="goToText(text)">
        {{ text.preview }}
      </p>
    </div>
    <div v-else>
      <h2>Texts loading is in progress...</h2>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import AddText from '@/components/AddText.vue'
import { API, AppText } from '@/api'
@Component({
  components: { AddText }
})
export default class Home extends Vue {
  texts: AppText[] | null = null;

  beforeMount () {
    API.getTexts().then(texts => (this.texts = texts))
  }

  goToText (text: AppText) {
    this.$router.push(`/text/${text.id}`)
  }
}
</script>

<style scoped lang="scss">
.uploaded-text {
  cursor: pointer;
  margin-bottom: 20px;
  &:hover {
    text-decoration: underline;
  }
}
</style>
