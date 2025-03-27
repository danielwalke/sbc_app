<template>
  <div class="p-4 lg:p-8 custom-height w-full overflow-y-auto">
    <h1 class="text-center">Youtube-Tutorials</h1>
    <div class="text-center mb-2">You can find a list of explanatory Tutorials on <a target="_blank" href="https://www.youtube.com/watch?v=mFxcSfSPRqE&list=PLcMekJvaLnV-5TUurOS3Q58yYGhsn2Fzg&ab_channel=MDOAToolsBielefeld">Youtube</a>: </div>
    <div class="grid gap-4 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3">
      <div v-for="(video, index) in embeddedLinks" :key="index" class="rounded-lg overflow-hidden shadow-lg">
        <div class="aspect-w-16 aspect-h-9">
          <iframe
              :src="video"
              :title="titles[index]"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
              class="w-full h-48"
          ></iframe>
        </div>
        <div class="p-2 bg-sky-800 text-white text-center font-semibold">
          {{ titles[index] }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed} from "vue";

const videoLinks = ["https://www.youtube.com/embed/mFxcSfSPRqE?si=bEX_jaI35hjWxA4I",
  "https://www.youtube.com/embed/MAZnUR2NAtE?si=ta7Z6hLE-vMXifmm",
  "https://www.youtube.com/embed/ltawHl3CHTs?si=1waaawz9zkJ8Cwz5",
  "https://www.youtube.com/embed/luiYG8DT59I?si=wyh2IOf08B6IWOOY",
  "https://www.youtube.com/embed/25aA9UL8NgA?si=m0kEYFKZqvdR_XVs",
  "https://www.youtube.com/embed/rxclOvnYKnM?si=z7bM1crXtRq_Pc0T",
  "https://www.youtube.com/embed/WYnEV6rXWLY?si=v0iIogOf4QaucyNQ",
  "https://www.youtube.com/embed/Ou6TyFyCBac?si=zDlXK1wTmIxI1KrT",
  "https://www.youtube.com/embed/7An7GzHydnE?si=EqCTF1eOxr2y0xIs",
  "https://www.youtube.com/embed/xALGYqCN2I8?si=7V9YQWZGagMI3jmy",
  "https://www.youtube.com/embed/ymOUin-xRJE?si=mpt-Qbl36c9n5HIe",
  "https://www.youtube.com/embed/WF_Z7rHrdJY?si=qUJjhnLCKyrvkMnj",
  "https://www.youtube.com/embed/qcQakg9_8qQ?si=_EzJU9dMlknlO3uy"]
const titles = ["Introduction",
  "Input new Data",
  "Input data as CSV",
  "Structure of the CSV file",
  "Test data as demonstration",
  "Prediction goal",
  "Sorting data",
  "Filter data",
  "Filter data II (Time-series filtering)",
  "Customize sensitivity",
  "Investigate details (SHAP values)",
  "Prediction of other classifiers",
  "Local setup"]

const embeddedLinks = computed(() =>
    (videoLinks || []).map(link => link.replace("watch?v=", "embed/"))
);
</script>

<style scoped>
.aspect-w-16 {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9 Aspect Ratio */
}

.aspect-w-16 iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

h1{
  @apply text-lg lg:text-2xl font-semibold mb-2
}

a{
  @apply underline
}
</style>
