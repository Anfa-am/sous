<template>
  <div class="recipe-grid">
      <div class="action">
          <div @click="close"> <v-icon class="ripple-c" name="arrow-left" /> </div>

          <h4> {{name}} </h4>

          <div class="actions">
              <v-icon name="" class="" @click="false"/>
          </div>
      </div>

      <div class="grid">
        <transition-group name="fade" :css="false" tag="div" appear @before-enter="beforeEnter" @enter="enter" @leave="leave">
          <Recipe v-for="(recipe, i) in recipes" :recipe="recipe" :key="i" :data-key="i" />
        </transition-group>
      </div>
  </div>
</template>

<script>

import Recipe from '@/components/RecipeGridItem.vue'
import smoothReflow from 'vue-smooth-reflow'
import Velocity from 'velocity-animate'

export default {
  name: 'RecipeGrid',

  mixins: [smoothReflow],

  components: {
    Recipe
  },

  props: {
    recipes: {
        type: Array,
        required: true
    },

    name: {
        type: String,
        required: true
    }
  },

  mounted: function(){
      this.$smoothReflow()
  },

  methods: {
    beforeEnter(el) {
      el.style.opacity = 0
    },

    enter(el, done) {
      var delay = el.getAttribute('data-key') * 45
      setTimeout(function() {
        Velocity(el, { opacity: 1 }, { complete: done })
      }, delay)
    },

    leave(el, done) {
      Velocity(el, { opacity: 0 }, { complete: done })
    },

    close: function(){
        this.$parent.open = false
    }
  }

}
</script>

<style scoped lang="sass">

.action
    position: fixed
    top: 0
    left: 0
    display: flex
    z-index: 10
    width: calc(100vw - 19px)
    padding: 10px
    padding-top: 15px
    margin-left: -10px
    background-color: rgba(13, 14, 2, 0.75)
    backdrop-filter: blur(5px)
    border-bottom-left-radius: 20px
    border-bottom-right-radius: 20px
    align-items: center
    .actions
        display: flex
        align-items: center
        color: var(--pink)
    svg
        width: 20px
        padding: 10px
        margin: 0 10px
        color: var(--white)

    .title
        color: var(--white)
        text-transform: capitalize
        line-height: 1.2
        font-weight: bolder
        text-shadow: -1px 2px 10px rgba(13, 14, 2, 0.3)


.recipe-grid
    position: fixed
    z-index: 9
    top: 0px
    left: 0
    width: 100vw
    height: 100vh
    background-color: var(--black)
    overflow-y: scroll

.grid > div
    display: flex
    padding: 20px
    flex-wrap: wrap
    align-items: baseline
    justify-content: space-between
    margin-top: 60px

.full
    .recipe-grid
        overflow: hidden

    .action
        opacity: 0
        pointer-events: none

</style>
