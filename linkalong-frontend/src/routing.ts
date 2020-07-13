import { RouteConfig } from 'vue-router'
import Home from '@/pages/Home.vue'
import AddedText from '@/pages/AddedText.vue'
import SentenceLookup from '@/pages/SentenceLookup.vue'

export const routes: RouteConfig[] = [
  { path: '/', component: Home },
  { path: '/text/:id', component: AddedText },
  { path: '/sentence/:id', component: SentenceLookup }
]
