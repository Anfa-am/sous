<template>
    <div class="item" :class="{open: open}">
    <div class="bg" @click="toggle" :class="{open: open}">
        <img :src="`http://192.168.0.16:2020/h32/${recipe._id}/0.jpg`" />
    </div>

    <div class="desc" @click="toggle">
        <h4> {{recipe.name}} </h4>
        <span>  {{recipe.classification.type}}, {{recipe.classification.course}} </span>
    </div>

    <div class="rec-details" v-if="open">
        <portal-target :name="`bar`" class="lift" />
        <portal-target :name="`cover`" class="cover" />

        <Details :recipe="recipe" :closeUp="true"/>
    </div>

  </div>
</template>

<script>
import Details from "@/components/RecipeDetails.vue"

export default {
  name: 'listItem',
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
          this.$parent.drawn = true
        }

       this.open = !this.open
    },

  }

}
</script>

<style scoped lang="sass">
.item
    display: flex
    margin: 20px
    align-items: center
    

.desc
    width: 100%
    margin: 20px
    font-size: 11pt
        
.bg
    width: 190px
    height: 100px
    overflow: hidden
    margin: 10px
    border-radius: 5px
    img
        width: 100%
        height: 100%
        object-fit: cover
        filter: saturate(1.5) brightness(0.8) contrast(1.15)

.open
    .bg
        position: fixed
        width: 100%
        top: -20px 
        transform: scale(1.2)
h4
    line-height: 1.2

span
    display: inline-block
    color: var(--white)
    vertical-align: middle
    padding-top: 15px
    font-size: 8pt

svg
    width: 15px
    padding-right: 10px
    vertical-align: middle

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
    .bg:not(.open), .desc
        opacity: 0
    
</style>

<style lang="sass">
.full
    .ex-search
        .closeSearch, .input
            opacity: 0
            pointer-events: none
</style>
