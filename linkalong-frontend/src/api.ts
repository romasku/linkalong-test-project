export interface AppText {
  id: number;
  preview: string;
  processed: boolean;
}

export interface Sentence {
  id: number;
  content: string;
}

export interface Paragraph {
  sentences: Sentence[];
}

export interface FullText extends AppText {
  paragraphs: Paragraph[];
}

export interface ListedSentence extends Sentence {
  text: AppText;
}

interface SimilarResponse {
  sentence: ListedSentence;
  similar_sentences: ListedSentence[];
}

class APIClient {
  apiURL = 'http://localhost:8000/api/'

  getTexts (): Promise<AppText[]> {
    return fetch(`${this.apiURL}texts/`).then(value => value.json())
  }

  getText (textId: number): Promise<FullText> {
    return fetch(`${this.apiURL}texts/${textId}/`).then(value => value.json())
  }

  uploadText (text: string): Promise<FullText> {
    return fetch(`${this.apiURL}texts/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ content: text })
    }).then(value => value.json())
  }

  getSimilar (sentenceId: number): Promise<SimilarResponse> {
    return fetch(`${this.apiURL}similar/${sentenceId}/`).then(value => value.json())
  }
}

export const API = new APIClient()
