<template>
    <div class="grid-item" :class="{open:open}">
    <div class="img" @click="toggle">
        <img class="bg" :src="`http://192.168.0.16:2020/h32/${recipe._id}/0.jpg`" />
    </div>

    <div class="details">
        <h5> {{recipe.name}} </h5>
        <span> {{recipe.time}} mins </span>
    </div>


    <div class="rec-wrapper" v-if="open">
        <portal-target :name="`bar`" class="lift" />
        <portal-target :name="`cover`" class="cover" />

        <Details :recipe="recipe" :closeUp="true"/>
      </div>
  </div>
</template>

<script>
import Details from "@/components/RecipeDetails.vue"

export default {
  name: '',

  components: {
      Details,
  },

  props: {
      recipe: {
        type: Object,
        required: true
      }
  },

  data: function(){
    return {
        open: false
    }
  },
  methods: {

    toggle: function(){
        let carousel = document.querySelector('#app');

        if (carousel.classList.contains('full')) {
          carousel.classList.remove('full');
        } else {
          carousel.classList.add('full');
        }

       this.open = !this.open
    },

  }
}
</script>

<style scoped lang="sass">
.grid-item
    margin-bottom: 10px
    width: calc(50% - 10px)

.img
    width: 100%
    height: auto
    overflow: hidden
    border-radius: 5px
    img
        position: relative
        min-width: 100%
        height: 30vh
        border-radius: 5px
        box-sizing: object-fit
        filter: saturate(1.5) brightness(0.7) contrast(1.15)

.details
    h5
        font-size: 9pt
        margin-top: 15px
        margin-bottom: 5px
        line-height: 1.2
    span
        font-size: 8pt
        color: var(--white)

.rec-details
    position: fixed
    top: 0
    left: 0px
    height: 100vh
    width: 100vw
    overflow-y: scroll
    z-index: 15

.lift, .cover
    top: 0
    position: fixed

.cover
    right: 10px
    height: 30vh

.lift
    z-index: 20
    left: 10px

.full
    .grid-item:not(.open)
        opacity: 0
        pointer-events: none

.open
    .img
        position: fixed
        width: 100vw
        height: auto
        left: 0
        top: 0
        transform: translateY(-10px) scale(1.3)
        z-index: 8
        ::before 
          content: ''
          display: block
</style>
