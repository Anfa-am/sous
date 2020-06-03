<template>
    <div class="exp">
        <div class="action page-el" :class="{searchOpen: searchOpen}">
            <h4> Shopping list </h4>
            <div class="actions">
                <div @click="openSearch"> <v-icon class="ripple-c search-ic" name="shopping-bag" /> </div>
            </div>
        </div>

        <div class="lists" v-if="loaded">
            <ShoppingList :generic="true"/>
            <transition-group name="fade" :css="false" tag="div" appear @before-enter="beforeEnter" @enter="enter" @leave="leave">
                <ShoppingList v-for="(r, i) in lists" :generic="false" :recipe="r" :key="i" :data-key="i" />
            </transition-group>
        </div>

        <transition name="fade">
            <Search  v-if="searchOpen"/>
        </transition >
    </div>
</template>

<script>

import ShoppingList from '@/components/ShoppingList.vue'
import Search from '@/components/IngSearch.vue'
import smoothReflow from 'vue-smooth-reflow'
import Velocity from 'velocity-animate'
export default {

  mixins: [smoothReflow],
  name: 'shoppingList',

  components: {
    ShoppingList,
      Search
  },

  computed: {

  },

  data: function(){
    return {
        searchOpen: false,
        groceries: [],
        loaded: false,
        lists: [],
    }
  },

  mounted: function(){
      if(!window.localStorage.getItem('id')){ window.location = '/#/' }

      this.$smoothReflow()
      this.axios.post('http://192.168.0.16:4040/api/user/getLists', {
        id: window.localStorage.getItem('id')
      }).then((res) => {
          this.groceries = res.data.groceries

          this.axios.post('http://192.168.0.16:4040/api/recipes/group', {
            id: window.localStorage.getItem('id'),
            ids: res.data.lists
          }).then((r) => {
              this.lists = r.data
              this.lists.forEach(l => {
                  if(!window.localStorage.getItem('lists')){
                    window.localStorage.setItem('lists', JSON.stringify({})) 
                  }

                  if(!JSON.parse(window.localStorage.getItem('lists'))[l._id]){
                    let newO = JSON.parse(window.localStorage.getItem('lists'))
                    newO[l._id] = []
                    window.localStorage.setItem('lists', JSON.stringify(newO)) 
                  }
              })
              this.loaded = true
          })
      })
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

    openSearch: function(){
        if(this.searchOpen){
            this.searchOpen = false
        }else{
            this.searchOpen = true
        }
    },
  }
}
</script>

<style lang="sass" scoped>

.exp
    position: relative
    width: 100vw
    height: 100vh
    top: 0
    left: 0

.action
    position: absolute
    top: 0
    z-index: 2
    width: calc(100vw - 40px)
    display: flex
    padding: 20px
    background-color: rgba(13, 14, 2, 0.75)
    backdrop-filter: blur(5px)
    padding-bottom: 10px
    align-items: bottom
    justify-content: space-between
    .actions
        display: flex
    h4
        font-size: 22pt
        align-self: center
    svg
        color: var(--white)
        width: 20px
        padding: 10px
    &.searchOpen
        h4
            opacity: 0
        svg
            opacity: 0

        .search-ic
            transform: translateX(calc(-100vw + 120px))
            opacity: 1


.lists
    position: absolute
    top: 0px
    z-index: 1
    width: 100%
    height: calc(100vh - 80px)
    padding-top: 80px
    overflow-y: scroll
    .list:last-of-type
        margin-bottom: 100px
</style>
