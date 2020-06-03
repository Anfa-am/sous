<template>
    <div class="exp">

        <div class="action page-el" :class="{searchOpen: searchOpen}">
            <h4> Explore </h4>
            <div class="actions main">
                <div @click="openSearch" >
                    <v-icon class="ripple search-ic" name="search" />
                </div>
                <div @click="openPrefs" v-if="loggedIn">
                    <v-icon name="sliders" class="ripple" @click="false"/>
                </div>
                <div @click="login" v-else>
                    <v-icon name="user" class="ripple" @click="false"/>
                </div>
            </div>
        </div>

        <div class="tab-wrapper page-el">
            <transition name="fade">
                <div class="tabs" v-if="loaded">
                    <div class="tab" v-for="(t, i) in tabs" :key="i">
                        <navIconZ v-if="i == activeTab" class="act-svg"/>

                        <span @click="changeTab(i)">{{t.name}}</span>
                        <div @click="deleteTab(i)">
                            <v-icon v-if="t.type" class='' name="x"/>
                        </div>
                    </div>

                    <div class="tab activity" @click="toggleTab"> <v-icon class="ripple" name="folder-plus"/>
                    </div>
                </div>
            </transition>

            <transition name="fade">
                <div class="tab-create" v-if="tabSearchOpen">
                    <input v-model="tabQuery" ref="tab" type="text" @keypress.enter.prevent="addTab" />
                    <div class="actions">
                        <div class="action" @click="toggleTab"> <v-icon class="ripple" name="x"/> </div>
                        <div class="action" @click="addTab"> <v-icon class="ripple" name="arrow-right"/> </div>
                    </div>
                </div>
            </transition>

            <transition name="fade">
                <div class="cover" v-if="tabSearchOpen">
                    <v-icon name="folder-plus"/>
                    <span> Search for something like 'basil' </span>
                </div>
            </transition>

            <div class="faout"/>
        </div>

        <transition name="fade">
            <div class="tab-view" v-if="!searchOpen">
                <div class="glide">
                  <div class="glide__track" data-glide-el="track">
                    <div class="glide__slides">
                            <Slide v-for="(r, i) in recipes" :recipe="r" :key="i" />
                    </div>
                  </div>
                </div>
            </div>
        </transition>

        <transition name="fade">
            <Search  :endpoint="'all'" v-if="searchOpen"/>
        </transition>
    </div>
</template>

<script>
import Glide from '@glidejs/glide'
import Slide from '@/components/RecipeSlideItem.vue'
import Search from '@/components/ExSearch.vue'
import navIconZ from "@/assets/nav0.svg?inline";
import smoothReflow from 'vue-smooth-reflow'
import Velocity from 'velocity-animate'

export default {

  name: 'Explore',

  mixins: [smoothReflow],

  components: {
      Slide,
      Search,
      navIconZ
  },

  computed: {
      loggedIn: function(){
          return window.localStorage.getItem('id')
      },

      seasonIndex: function(){
        let today = new Date()
        let month = today.getMonth()
        if( month == 12 || month == 1 || month == 2){ return 0 }
        else if(month == 3 || month == 4 || month == 5){ return 1 }
        else if(month == 6 || month == 7 || month == 8) { return 2 }
        return 3
      },

      recipes: function(){
          if(this.tabs && this.tabs[this.activeTab]){
            return this.tabs[this.activeTab].recipes
          }else{
              return []
          }
      }
  },

  data: function(){
    return {
        activeTab: 0,
        searchOpen: false,
        tabQuery: '',
        tabSearchOpen: false,
        loaded: false,

        tabOptions: [
            {
                name: 'Spotltight',
                index: 'any',
                filters: [
                    {
                        name: ' - herbs',
                        query: {$or: [{ name: {$regex : ".*basil.*"} }, { name: {$regex : ".*oregano.*"} }, { name: {$regex : ".*thyme.*"} }, { name: {$regex : ".*rosemary.*"} }, { name: {$regex : ".*mint.*"} }, { name: {$regex : ".*parsley.*"} }, { name: {$regex : ".*cilantro.*"} }] }
                    },
                    {
                        name: ' - seafood',
                        query: {$or: [{ name: {$regex : ".*fish.*"} }, { name: {$regex : ".*shrimp.*"} }, { name: {$regex : ".*salmon.*"} }, { name: {$regex : ".*lobster.*"} }, { name: {$regex : ".*tuna.*"} }, { name: {$regex : ".*tilapia.*"} }] }

                    },{
                        name: ' - the pantry',
                        query: {$or: [{ name: {$regex : ".*pasta.*"} }, { name: {$regex : ".*risotto.*"} }, { name: {$regex : ".*orzo.*"} }, { name: {$regex : ".*linguine.*"} }] }

                    },{
                        name: ' - the garden',
                        query: {$or: [{ name: {$regex : ".*spinach.*"} }, { name: {$regex : ".*kale.*"} }, { name: {$regex : ".*tomato.*"} }, { name: {$regex : ".*mushroom.*"} },  {name: {$regex : ".*arugula.*"}}, { name: {$regex : ".*potato.*"} }, { name: {$regex : ".*onion.*"} }] }

                    },{
                        name: ' - friuts',
                        query: {$or: [{ name: {$regex : ".*apple.*"} }, { name: {$regex : ".*berry.*"} }, { name: {$regex : ".*orange.*"} }, { name: {$regex : ".*mango.*"} },  {name: {$regex : ".*passion.*"}}, { name: {$regex : ".*friut.*"} }, { name: {$regex : ".*bannana.*"} }, { name: {$regex : ".*melon.*"} }] }

                    },{
                        name: ' - eggs',
                        query: { name: {$regex : ".*eggs.*"} }

                    }
                ]
            }, {
                name: 'In Season',
                index: 'si',
                filters: [ {
                        name: ' - winter',
                        query: {$or: [{ name: {$regex : ".*winter.*"} }, { name: {$regex : ".*soup.*"} }, { name: {$regex : ".*orange.*"} }, { name: {$regex : ".*mango.*"} },  {name: {$regex : ".*passion.*"}}, { name: {$regex : ".*friut.*"} }, { name: {$regex : ".*bannana.*"} }, { name: {$regex : ".*melon.*"} }] }
                    },{
                        name: ' - spring',
                        query: {$or: [{ name: {$regex : ".*carrot.*"} }, { name: {$regex : ".*pea.*"} }, { name: {$regex : ".*spring.*"} }, { name: {$regex : ".*mint.*"} },  {name: {$regex : ".*salad.*"}}, { name: {$regex : ".*pesto.*"} } ] }
                    },{
                        name: ' - summer',
                        query: {$or: [{ name: {$regex : ".*berry.*"} }, { name: {$regex : ".*melon.*"} }, { name: {$regex : ".*summer.*"} }, { name: {$regex : ".*bbq.*"} },  {name: {$regex : ".*lemonade.*"}}, { name: {$regex : ".*roll.*"} }, { name: {$regex : ".*grill.*"} } ] }
                    },{
                        name: ' - fall',
                        query: {$or: [{ name: {$regex : ".*pumpkin.*"} }, { name: {$regex : ".*soup.*"} }, { name: {$regex : ".*squash.*"} }, { name: {$regex : ".*potato.*"} },  {name: {$regex : ".*turkey.*"}}, { name: {$regex : ".*pomme.*"} }, { name: {$regex : ".*cranberry.*"} }] }
                    }
                ]
            }
        ],

        tabs: [ ]
    }
  },

  mounted: function(){
      this.$smoothReflow()
      let hasCache = JSON.parse(window.localStorage.getItem('tabs'))
      if(hasCache){
          this.tabs = hasCache
          this.initSlider()
      }else{
          this.axios.get('http://192.168.0.16:4040/api/recipes/explore').then((res) => {
              this.tabs.push({
                  name: 'Popular',
                  recipes: res.data
              })
              this.initSlider()
          })

          this.getStubTab()
      }
      this.getUser()
      this.loaded = true

      //this.cacheTabs()
  },

  watch: {
      searchOpen: function(){
          if (!this.searchOpen){
              this.$nextTick(() => {
                  this.initSlider()
              })
          }
      }
  },

  methods: {
     beforeEnter(el) {
      el.style.opacity = 0
    },

    enter(el, done) {
      var delay = el.getAttribute('data-key') * 5
      setTimeout(function() {
        Velocity(el, { opacity: 1 }, { complete: done })
      }, delay)
    },

    leave(el, done) {
      Velocity(el, { opacity: 0 }, { complete: done })
    },

    cacheTabs: function(){
        window.localStorage.setItem('tabs', JSON.stringify(this.tabs))
    },

    getUser: function(){
        let id = window.localStorage.getItem('id')
        if(id){
            this.axios.post('http://192.168.0.16:4040/api/user/getSaves', { id: id }).then(x => {
                window.localStorage.setItem('saves', JSON.stringify(x.data.saved))
            })
        }
    },

    getStubTab: function(){
        let item = this.tabOptions[Math.floor(Math.random() * this.tabOptions.length)];
        let choice = {}
        if(item.index == 'any'){
            choice = item.filters[Math.floor(Math.random() * item.filters.length)];
        }
        if(item.index ==  'si'){
            choice = item.filters[this.seasonIndex];
        }
        
        this.axios.post('http://192.168.0.16:4040/api/recipes/specialTab', {query: choice.query}).then((res) => {
            this.tabs.push( { recipes: res.data, name: item.name + choice.name  })
        })
    },

    login: function(){
        window.location = '/#/'
    },
    deleteTab: function(i){
        this.changeTab(i - 1)
        this.tabs.splice(i, 1)
    },

    changeTab: function(i){
        this.activeTab = i
        this.initSlider()
        this.scrollFocusTab()
    },

    scrollFocusTab(){
        this.$nextTick(() => {
            let test = document.querySelectorAll('.tab-wrapper .tab')[this.activeTab]
            document.querySelector('.tab-wrapper .tabs').scrollTo({ left: test.offsetLeft,  behavior: 'smooth' })
        })
    },

    addTab: function(){

        if(this.tabQuery == '') { return false }

        this.tabs.push({
            name: this.tabQuery,
            type: 'added',
            recipes: []
        })

        this.activeTab = this.tabs.length - 1

        this.scrollFocusTab()

        this.axios.post('http://192.168.0.16:4040/api/recipes/getTab',{
            query: this.tabQuery
        }).then((res) => {
            this.tabs[this.activeTab].recipes = res.data
            this.initSlider()
            this.cacheTabs()
        })

        this.toggleTab()
        this.tabQuery = ''
        return
    },

    toggleTab(){
        if(this.tabSearchOpen){
            this.tabSearchOpen = false
            this.tabQuery = ""
        }else{
            this.tabSearchOpen = true
            this.$nextTick(() => {
                this.$refs.tab.focus()
            })
        }
    },

    openPrefs: function(){
        window.location = '/#/prefrences?ex=true'
    },

    openSearch: function(){
        if(this.searchOpen){
            this.searchOpen = false
        }else{
            this.searchOpen = true
        }
    },

    initSlider: function(){
        this.$nextTick(() => {
            var glide = new Glide('.glide', {
              focusAt: 'center',
                //cache tab position
              startAt: 0,
              perTouch: false,
              throttle: 0,
              animationDuration: 130,
              swipeThreshold: 250/4,
              touchRatio: 0.2,
              rewind: false,
              gap: -35,
              perView: 1.3
            })
            const tiltableElement = '.glide__container';
            glide.mount({
              Coverflow: (Glide, Components, Events) => {
                const Plugin = {
                  tilt (element) {
                    element.querySelector(tiltableElement).style.transform = "scale(1) perspective(1700px) rotateY(0deg)";
                    this.tiltPrevElements();
                    this.tiltNextElements();
                  },
                  tiltPrevElements () {
                    const activeSlide = Components.Html.slides[Glide.index];

                    const previousElements = [];
                    const getPrevious = (element) => {
                      const e = element.previousElementSibling;
                      if (e) {
                        previousElements.push(e.querySelector(tiltableElement));
                        getPrevious(e);
                      }
                    };

                    getPrevious(activeSlide);

                    previousElements.forEach((item, index) => {
                      item.style.transformOrigin = "50% 0%";
                      item.style.transform = `scale(0.8) perspective(1700px) rotateY(${20 * Math.max(index, 2)}deg)`
                    })

                  },

                  tiltNextElements () {
                    const activeSlide = Components.Html.slides[Glide.index];

                    const nextElements = [];

                    const getNext = (element) => {
                      const e = element.nextElementSibling;
                      if (e) {
                        nextElements.push(e.querySelector(tiltableElement));
                        getNext(e);
                      }
                    };
                    getNext(activeSlide);

                    nextElements.forEach((item, index) => {
                      item.style.transformOrigin = "50% 0%";
                      item.style.transform = `scale(0.8) perspective(1700px) rotateY(${-20 * Math.max(index, 2)}deg)`
                    })
                  }
                }

                Events.on(['mount.after', 'run'], () => { Plugin.tilt(Components.Html.slides[Glide.index]);
                });

                return Plugin;
              }
            });
        })

    }
  }
}
</script>

<style lang="sass" scoped>
@import "node_modules/@glidejs/glide/src/assets/sass/glide.core";

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

.tab-wrapper
    position: relative
    .faout
        position: absolute
        width: 10%
        height: 40px
        right: 0
        top: 5px
        content: ''
        background: linear-gradient(to right, rgba(255, 255, 255, 0), var(--black))
        pointer-events: none

.tabs-wrapper
    postion: relative

.cover
    position: fixed
    width: 100vw
    height: 100vh
    background-color: var(--black)
    z-index: 29
    top: 130px
    display: flex
    align-items: center
    flex-direction: column
    color: #1d1d1b
    padding-top: 20px

    span
        font-size: 18pt
        width: 80%
        text-align: center

    svg
        width: 30vw
        margin: 40px 0


.tab-create
    position: absolute
    z-index: 5
    top: 0
    left: 0
    width: 100%
    background-color: var(--black)
    display: flex
    .actions
        width: 10%
        display: flex
        .action
            padding: 0

        .action svg
            padding: 5px


    input
        width: calc(80% - 20px)
        margin-left: 20px
        padding: 20px 0
        color: var(--white)
        border: none
        border-bottom: 1px solid var(--white)
        background-color: var(--black)

.tabs
    display: flex
    position: relative
    overflow-x: scroll
    overflow-y: hidden
    width: calc(100vw - 20px)
    padding: 10px

    .tab
        display: flex
        align-items: center
        position: relative


        .act-svg
            position: absolute
            left: 0%
            margin-top: 20px
            opacity: 0.5
        span
            display: block
            white-space: nowrap
            padding: 0 12px
            color: var(--white)
        svg
            width: 12px
            margin-top: 2px
            margin-left: 5px
            margin-right: 10px
            color: var(--white)

        &.activity
            padding-right: 10px
            padding-left: 20px
            color: var(--pink)
            svg
                position: relative
                color: var(--pink)
                padding: 5px
                width: 25px
.glide
    width: 100vw

    .glide__track
        width: 100vw
        height: 100vh

        .glide__slides
            margin: 0
            overflow: visible
            transform-style: preserve-3d
</style>

<style lang="sass">
#app.full
    .page-el
        pointer-events: none
        opacity: 0

    .tab-view
        position: absolute
        //fix me
        transform: translateY(calc(-15vh - 10px))
        .glide__slide
            opacity: 0
            pointer-events: none

        .glide__slide--active
            opacity: 1

            .content
                clip-path: circle(0)

            img
                width: 100vw
                height: 40vh
                transform: scale(1.2) translateX(-10%) translateY(-10%)
                transform-origin: center
                z-index: 9
                opacity: 1


.scroll-content > div
    pointer-events: none!important

.full
    .details
        .scroll-content > div
            pointer-events: all!important


.pulldown-wrapper
    display: none!important

</style>
