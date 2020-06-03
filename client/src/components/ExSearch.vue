<template>
    <div class="ex-search">
        <div class="closeSearch" @click="$parent.openSearch"> 
            <v-icon name="search" class="ripple-c" @click="false"/>
        </div>
        <div class="input">
            <input class="hmn" v-model="query" type="text" placeholder="find recipes..." ref="in"/>
        </div>

        <div class="results">
            <transition-group name="fade" :css="false" tag="div" appear @before-enter="beforeEnter" @enter="enter" @leave="leave">
                <RecipeListItem v-for="(r, i) in results" :recipe="r" :key="i" :data-key="i" />
            </transition-group>
        </div>
    </div>
</template>

<script>
import RecipeListItem from '@/components/RecipeListItem.vue'
import smoothReflow from 'vue-smooth-reflow'
import Velocity from 'velocity-animate'
export default {
  name: 'ExSearch',

  mixins: [smoothReflow],
  components: {
    RecipeListItem
  },

  props: {
    endpoint: {
        type: String,
        required: true
    }
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

 },
  data: function(){
      return {
          query: '',
          results: [],
          ingsTitles: [],
          ings: []
      }
  },

  mounted: function(){
      this.$smoothReflow()
      this.$nextTick(() => {
        this.$refs.in.focus()
      })
  },

  watch: {
    query: function(){
        this.axios.post('http://192.168.0.16:4040/api/recipes/exsearch', { query: this.query }).then((res) => {
          this.results = res.data
        })
    }
  }
}
</script>

<style scoped lang="sass">
.ex-search
    position: fixed
    width: 100vw
    height: 100vh
    top: 0
    left: 0
    z-index: 9
    width: calc(100% - 40px)
    padding: 20px

    .closeSearch
        position: absolute
        top: 14px
        width: 40px
        height: 40px
        z-index: 9
        svg
            margin-top: 20px
            margin-left: 10px
            color: var(--white)
            width: 20px

    .input
        position: relative
        width: 100%
        padding-top: 5px
        top: 0
        left: 0
        z-index: 2
        &::before
            position: absolute
            content: ''
            width: 100vw
            height: 100px
            top: -20px
            left: -20px
            background-color: rgba(13, 14, 2, 0.75)
            backdrop-filter: blur(5px)
            z-index: -1
        &::after
            position: absolute
            content: ''
            bottom: -5px 
            right: 0
            width: calc(100% - 60px)

    .hmn
        position: absolute
        width: calc(100% - 60px)
        height: 100%
        top: -5px
        left: 60px
        font-size: 12pt
        border: none
        border-bottom: 1px solid var(--white)
        background-color: transparent
        padding: 20px 0
        color: var(--white)
        &::placeholder
            font-size: 12pt
            color: var(--grey)
            opacity: 0.3

    .results
        position: absolute
        width: 100vw
        height: calc(100vh - 80px)
        padding-top: 80px
        top: 00px
        z-index: -1
        left: 0
        overflow-y: scroll
        background-color: var(--black)
</style>
