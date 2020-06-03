<template>
    <div class="exp">

        <div class="action page-el" :class="{searchOpen: searchOpen}">
            <h4> Your Coobook </h4>
            <div class="actions">
                <div @click="toggleImport"> <v-icon class="ripple" name="share" /> </div>
                <div @click="openSearch"> <v-icon class="ripple search-ic" name="search" /> </div>
            </div>
        </div>

        <div class="book-wrapper">
                <div class="books" v-if="cloaded">
                    <transition-group name="fade" :css="false" tag="div" appear @before-enter="beforeEnter" @enter="enter" @leave="leave">
                        <Book v-for="(r,i) in books" :recipes="r.data" :name="r.name" :key="i"  :data-key="i" > </Book>
                    </transition-group>
                </div>

            <transition name="fade">
                <div class="book-overlay" v-touch:swipe="pullUp" :class="{drawn: drawn}" v-if="rloaded">
                    <div class="lip"> </div>
                      <div class="recipe-list" ref="ovl">
                        <RecipeListItem v-for="(r, i) in saved" :recipe="r" :key="i"/>
                        <div v-if="saved.length == 0" class="no-save">
                            <span> No recipes saved press
                                <v-icon name="bookmark" class="ripple-c" :class="{saved: saved}"/>
                                to add to your collection
                            </span>
                        </div>
                    </div>
                </div>
            </transition>
        </div>

        <transition name="fade">
            <Search :endpoint="'my'"  v-if="searchOpen"/>
        </transition>

        <transition name="fade">
            <ImportModal v-if="importOpen"/>
        </transition>
    </div>
</template>

<script>

import Book from '@/components/CookBook.vue'
import ImportModal from '@/components/Import.vue'
import RecipeListItem from '@/components/RecipeListItem.vue'
import Search from '@/components/ExSearch.vue'
import smoothReflow from 'vue-smooth-reflow'
import Velocity from 'velocity-animate'
export default {

  mixins: [smoothReflow],
  name: 'Cookbook',

  components: {
    ImportModal,
    Book,
    Search,
    RecipeListItem
  },

  computed: {
    timeIndex: function(){
        let today = new Date()
        let hours = today.getHours()
        let day = today.getDay()

        if(day == 7 && hours > 8 && hours < 14){
            return 0
        }

        if(hours > 4 && hours < 12){
            return 1
        }

        if(hours > 11 && hours < 16){
            return 2
        }

        if(hours > 15 && hours < 17){
            return 3
        }

        if(hours > 16 && hours < 21){
            return 4
        }

        if(hours > 16 && hours < 25){
            return 5
        }

        return 5
    }
  },

  data: function(){
    return {
        pullDownRefreshObj: {
          threshold: 40,
          stop: 40
        },

        importOpen: false,
        searchOpen: false,

        timeBooks: [ {
                name: 'Sunday Brunch',
                query: {$or: [{"classification.course": "breakfast"}, { name: {$regex : ".*eggs.*"} }, { name: {$regex : ".*bacon.*"} }, { name: {$regex : ".*pancakes.*"} }, { name: {$regex : ".*waffles.*"} }, { name: {$regex : ".*oat.*"} }, { name: {$regex : ".*mimosas.*"} }, { name: {$regex : ".*coffee.*"} }, { name: {$regex : ".*latte.*"} }] }
            },{
                name: 'Breakfast',
                query: {$or: [{"classification.course": "breakfast"}, { name: {$regex : ".*eggs.*"} }, { name: {$regex : ".*bacon.*"} }, { name: {$regex : ".*pancakes.*"} }, { name: {$regex : ".*waffles.*"} }, { name: {$regex : ".*oat.*"} }, { name: {$regex : ".*coffee.*"} }, { name: {$regex : ".*smoothie.*"} }, { name: {$regex : ".*latte.*"} }] }
            }, {
                name: 'Lunch',
                query: {$or: [{"classification.course": "main"}, { name: {$regex : ".*sandwich.*"} }, { name: {$regex : ".*wrap.*"} }, { name: {$regex : ".*salad.*"} } ] }
            }, {
                name: 'Happy hour',
                query: {$or: [{"classification.course": "drink"}, { name: {$regex : ".*cocktail.*"} }, { name: {$regex : ".*bite.*"} }, { name: {$regex : ".*bar.*"} }, { name: {$regex : ".*finger.*"} } ] }
            }, {
                name: 'Dinner',
                query: {$or: [{"classification.course": "main"} ] }
            }, {
                name: 'Midnight snack',
                query: {$or: [{"classification.course": "side"} ] }
            },
        ],

        vibeBooks: [ {
                name: 'Healthy',
                query: {$or: [{ name: {$regex : ".*health.*"} }, { name: {$regex : ".*kale.*"} }, { name: {$regex : ".*salad.*"} }, { name: {$regex : ".*smoothie.*"} }, { name: {$regex : ".*gluten.*"} }, { name: {$regex : ".*keito.*"} } ] }
            },{
                name: 'For Your Sweet tooth',
                query: {$or: [{"classification.course": "dessert"}, { name: {$regex : ".*cookie.*"} }, { name: {$regex : ".*pie.*"} }, { name: {$regex : ".*cake.*"} }, { name: {$regex : ".*tart.*"} }, { name: {$regex : ".*shake.*"} }, { name: {$regex : ".*brownie.*"} } ] }
            }, {
                name: 'Party Perfect',
                query: {$or: [{"classification.course": "side"}, { name: {$regex : ".*nachos.*"} }, { name: {$regex : ".*platter.*"} }, { name: {$regex : ".*charcuterie.*"} }, { name: {$regex : ".*party.*"} }, { name: {$regex : ".*snacks.*"} } ] }
            }, {
                name: 'Something Spicy',
                query: {$or: [{ name: {$regex : ".*spicy.*"} }, { name: {$regex : ".*jalapeno.*"} }, { name: {$regex : ".*heat.*"} }, { name: {$regex : ".*hot.*"} }, { name: {$regex : ".*siciliana.*"} },  { name: {$regex : ".*pepper.*"}  }  ] }
            }, {
                name: 'Cheat Day',
                query: {$or: [ {"classification.course": "dessert"}, {"classification.course": "main"}, {"classification.cusine": "american"} ] }
            }, {
                name: 'I\'m feeling lucky',
                query: ''
            },{
                name: 'Quick & easy',
                query: {$and: [{"time": {$lte:30}}], $or: [ {"classification.course": "main"}, {"classification.course": "side"} ] }
            },{
                name: 'All about presentation',
                query: {$and: [{"time": {gte:30}},{"classification.type": "modern"}], $or: [ {"classification.course": "main"}, {"classification.course": "side"} ] }
            },{
                name: 'Classics & Favourites',
                query: {$and: [{"classification.type": "traditional"}], $or: [ {"classification.course": "main"}, {"classification.course": "side"} ] }
            },{
                name: 'Authentic',
                query: {$and: [{"classification.type": "traditional"}], $or: [ {"classification.cusine": "mediterranean"}, {"classification.cusine": "eastAsian"} , {"classification.cusine": "soutAsian"}, {"classification.cusine": "latin"}] }
            }
        ],


        books: [],
        saved: [],
        rloaded: false,
        cloaded: false,
        drawn: false
    }
  },

  mounted: function(){
      if(!window.localStorage.getItem('id')){ window.location='/#/' }

      this.$smoothReflow()
      this.loadSaves()

      this.axios.post('http://192.168.0.16:4040/api/recipes/specialTab', {query: this.timeBooks[this.timeIndex].query}).then((res) => {
          this.books.push({
              name: this.timeBooks[this.timeIndex].name,
              data: res.data
          })

          this.cloaded = true
      })

      this.getRandom(this.vibeBooks, 3).forEach(x => {
        this.axios.post('http://192.168.0.16:4040/api/recipes/specialTab', {query: x.query}).then((res) => {
            this.books.push({
                name: x.name,
                data: res.data
            })

        })
      })

      this.cloaded = true
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

    loadSaves: function(){
        this.rloaded = false

        this.axios.post('http://192.168.0.16:4040/api/recipes/group', {
            id: window.localStorage.getItem('id'),
            ids: JSON.parse(window.localStorage.getItem('saves'))
          }).then((r) => {
              this.saved = r.data
              this.rloaded = true
          })

    },
    toggleImport: function(){
        if(this.importOpen){
            this.importOpen = false
        }else{
            this.importOpen = true
        }
    },

    getRandom: function (arr, n) {
        var result = new Array(n),
            len = arr.length,
            taken = new Array(len);
        if (n > len)
            throw new RangeError("getRandom: more elements taken than available");
        while (n--) {
            var x = Math.floor(Math.random() * len);
            result[n] = arr[x in taken ? taken[x] : x];
            taken[x] = --len in taken ? taken[len] : len;
        }
        return result;
    },

     pullUp: function(d){
          let carousel = document.querySelector('#app');
          if(!d || d == 'top'){
              this.drawn = true
          }else if(d == 'bottom' && this.$refs.ovl.scrollTop < 10 && !carousel.classList.contains('full')){
              this.drawn = false
          }
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
    position: absolute
    width: 100vw
    height: 100vh
    top: 0
    left: 0

.action
    width: calc(100vw - 40px)
    display: flex
    padding: 20px
    background-color: rgba(13, 14, 2, 0.75)
    backdrop-filter: blur(5px)
    padding-bottom: 10px
    align-items: bottom
    justify-content: space-between
    &.searchOpen
        h4
            opacity: 0
        svg
            opacity: 0

        .search-ic
            transform: translateX(calc(-100vw + 120px))
            opacity: 1

    .actions
        display: flex
    h4
        font-size: 22pt
        align-self: center
    svg
        color: var(--white)
        width: 20px
        padding: 10px

.book-wrapper
    width: 100vw
    height: calc(100vh - 60px)
    overflow-y: scroll
    .books
        position: absolute
        width: 100vw
        height: auto
        padding-top: 5vh

    .book-overlay
        position: absolute
        background-color: rgba(#151515, 0.9)
        backdrop-filter: blur(5px)
        border-radius: 20px
        width: 100vw
        overflow: hidden
        height: auto
        top: 65vh
        .recipe-list
            height: calc(100vh - 150px)
            .item:first-of-type
                padding-top: calc(5vh - 10px)
                padding-bottom: 15vh
        &.drawn
            top: 80px
            .recipe-list
                overflow-y: scroll

                .item:first-of-type
                    padding-top: 10px
                    padding-bottom: 10px

        .lip
            position: absolute
            width: 30px
            height: 5px
            background-color: var(--black)
            border-radius: 10px
            left: calc(50% - 15px)
            top: 10px

        .no-save
            padding-top: calc(7vh - 10px)
            span
                display: block
                width: 80%
                margin: 20px auto
                text-align: center
                line-height: 1.5
            span, i
                vertical-align: middle
                color: var(--white)
            svg
                position: relative
                top: 10px
                width: 20px
                margin: 5px 10px

        &.drawn
            .no-save
                padding-top: calc(25vh - 10px)

.books > div
    position: relative
    overflow-x: scroll
    scroll-snap-type: x mandatory
    display: flex
    flex-wrap: nowrap
    scroll-padding: 50%

    .book:first-of-type
        margin-left: 20px

    .book:last-of-type
        padding-right: 20px

    > div
        scroll-snap-align: start
.full
    .action
        opacity: 0

    .book-wrapper
        .book-overlay.drawn
            overflow: hidden
            z-index: 9
            height: 100vh
            top: 0
            border-radius: 0
</style>
