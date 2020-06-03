<template>
  <div class="book">
    <div class="visual" @click="toggle">
        <img class="bg o" :src="`http://192.168.0.16:2020/h32/${recipes[2]._id}/0.jpg`" />
        <img class="bg t" :src="`http://192.168.0.16:2020/h32/${recipes[1]._id}/0.jpg`" />
        <img class="bg th" :src="`http://192.168.0.16:2020/h32/${recipes[0]._id}/0.jpg`" />
    </div>

    <div class="desc">
        <h4 class="title"> {{name}} </h4>
        <span> {{recipes.length}} recipes </span>
    </div>

    <transition name="fade">
        <RecipeGrid :name="name" :recipes="recipes" v-if="open"/>
    </transition>
  </div>
</template>

<script>
import RecipeGrid  from "@/components/RecipeGrid.vue"
export default {
  name: 'Cookbook',

  components: {
    RecipeGrid
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

  data: function(){
      return {
          open: false
      }
  },

  methods: {
    toggle: function(){
        this.open = !this.open
    }
  }

}
</script>

<style scoped lang="sass">

.book
    position: relative
    margin-right: 20px
    border-radius: 10px

.desc
    margin-top: 20px
    bottom: 0
    left: 0
    span
        font-size: 8pt
        color: var(--grey)
    h4
        font-size: 16pt
        width: 90%

.visual
    width: 55vw
    height: 35vh
    overflow: hidden
    position: relative
    border-radius: 5px

    img
        position: absolute
        width: 100%
        height: 100%
        object-fit: cover
        object-position: right
        border-radius: 5px
        top: 0vh
        left: 0
        box-shadow: -2px 2px 7px 3px rgba(black, 0.8)
        box-sizing: content-box
    .o
        left: 0%
        filter: saturate(1.5) brightness(0.6) contrast(1.35) blur(1px)

    .t
        left: 15%
        filter: saturate(1.5) brightness(0.7) contrast(1.15)

    .th
        left: 35%
        filter: saturate(1.5) brightness(0.7) contrast(1.15)

</style>
