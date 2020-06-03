<template>
    <div class="list groceries" v-if="generic" ref="list" :class="{collapse: collapse}">
        <img src="@/assets/static.jpg" v-touch:tap="toggle" />

        <h5> Your Groceries </h5>

        <div class="items" v-if="collapse">
            <div v-for="(g, i) in groceries" :key="i" class="list-item ing" :data-item="g"> 
              <span> {{ g }} </span>
              <v-icon name="minus" class="grab"/>
            </div>

            <div class="add"> 
                <transition name="fade">
                    <div class="make" @click="toggleAdd" v-if="!adding">
                        <v-icon class="ripple-c" name="shopping-cart"/>
                        <p> Add to list </p>

                        <div style="margin-left: calc(35% + 10px)">
                            <v-icon class="ripple-c" name="arrow-right"/>
                        </div>
                    </div>

                    <div class="active" v-if="adding">
                        <input v-model="grocery" type="text" ref="add" @blur="entered" />
                        <div class="actions" @click="entered">
                            <div class="action" > <v-icon class="ripple-c" name="corner-down-right"/> </div>
                        </div>
                    </div>

                </transition >
            </div>

        </div>
    </div>

    <div  v-else>
        <div class="list meal" v-if="!archived" ref="list" :class="{collapse: collapse}">
            <img :src="`http://192.168.0.16:2020/h32/${recipe._id}/0.jpg`" v-touch:tap="toggle" />

            <h5> {{recipe.name}} </h5>

            <div class="archive" @click="archive" v-if="collapse"> <v-icon name="archive" /> </div>

            <transition name="fade">
                <div class="items" v-if="collapse">
                    <Item v-for="(g, i) in recipe.ingredients" :key="i" :ingredient="g" :rid="recipe._id" class="list-item" />
                </div>
            </transition>
        </div>
    </div>
</template>

<script>

import Swiped from '@/swiped.js'
import Item from '@/components/ShoppingListIngredient.vue'
import debounce from 'debounce'
import smoothReflow from 'vue-smooth-reflow'
import Velocity from 'velocity-animate'

export default {
  name: 'shoppingList',

  components: {
      Item
  },

  props: {

    generic: {
        type: Boolean,
        required: true
    },

    recipe: {
        type: Object,
        required: false
    }

  },

  data: function(){
    return {
        archived: false,
        groceries: this.$parent.groceries,
        adding: false,
        grocery: '',
        collapse: this.generic
    }
  },

  mixins: [smoothReflow],

  mounted: function(){
    this.$smoothReflow()
    this.initSwipes()
    window.g = this
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

    archive: function(){
        this.axios.post('http://192.168.0.16:4040/api/user/addList', {
            id: window.localStorage.getItem('id'),
            index: this.recipe._id,
        }).then((res) => {
            console.log(res)
            this.archived = true
            let newO = JSON.parse(window.localStorage.getItem('lists'))
            delete newO[this.recipe._id]
            console.log(newO)
            window.localStorage.setItem('lists', JSON.stringify(newO)) 
        })
    },

    scrollAdd: function(){
        document.querySelector('.lists').scrollTo({ top: this.$refs.list.clientHeight - 160,  behavior: 'smooth' })
    },

    entered: function() {
        if (this.grocery){

            this.groceries.push(this.grocery)

            this.axios.post('http://192.168.0.16:4040/api/user/updateGroceries',{
                id: window.localStorage.getItem('id'),
                groceries: this.groceries
            })

            this.$refs.add.focus()
            this.$nextTick(() => { 
                this.grocery = ''
                this.scrollAdd()
                this.initSwipes() 
            })

        }else{
            this.grocery = ''
            let nav = document.querySelector('#nav.listPage');
            this.adding = false
            nav.classList.remove('goneo');

            this.$nextTick(() => {
                document.querySelector('.lists').scrollTo({ top: 0,  behavior: 'smooth' })
            })
        }
    },

    toggleAdd: function(){
        let nav = document.querySelector('#nav.listPage');

        if(this.adding){
            this.adding = false
            nav.classList.remove('goneo');
        }else{
            nav.classList.add('goneo');
            this.adding = true
            this.$nextTick(() => {
                this.grocery = ''
                this.scrollAdd()
                this.$refs.add.focus()
            })
        }
    },

    initSwipes: function(){
        this.$nextTick(() => {
        Swiped.init({
            query: '.ing',
            right: 400,
            left: 400,
            onOpen: debounce( function() { if(this.elem.parentNode){ 
                this.destroy(true) 
                if(window.g.groceries.indexOf(this.elem.dataset.item) > -1 && this.generic){
                    window.g.groceries.splice(window.g.groceries.indexOf(this.elem.dataset.item), 1)
                    window.g.axios.post('http://192.168.0.16:4040/api/user/updateGroceries',{
                       id: window.localStorage.getItem('id'),
                       groceries: window.g.groceries
                    })
                }
                if(!this.generic){
                    let newO = JSON.parse(window.localStorage.getItem('lists'))
                    newO[window.g.recipe._id].push(this.elem.dataset.item) 
                    window.localStorage.setItem('lists', JSON.stringify(newO)) 
                }
            } }, 10)
        });
      })
    },

    toggle: function(){
        this.collapse =  !this.collapse
        if(this.collapse){
            document.querySelector('.lists').scrollTo({ top: this.$refs.list.offsetTop - 80,  behavior: 'smooth' })
            this.initSwipes()
        }

        return
    }
  }
}
</script>

<style scoped lang="sass">

.list
    position: sticky
    top: 20px
    padding: 20px
    border-radius: 5px
    margin: 20px
    position: relative
    overflow: hidden
    min-height: 90px
    margin-bottom: 40px
    border: 1px solid var(--black)
    &.collapse
        border-color: #1d1d1b

    .list-item
        position: relative
    .add
        position: relative
        background-color: var(--pink)
        min-height: 50px
        top: 20px
        left: -20px
        width: calc(100% + 40px)
        padding-bottom: 0
        color: var(--white)
        input
            border: none
            border-bottom: 1px solid var(--white)
            background-color: transparent
            color: var(--white)
        svg
            width: 20px
        .make
            display: flex
            align-items: center
            svg
                padding: 0 20px

        .active
            display: flex
            align-items: center
            padding-top: 10px
            input 
                margin: 0 20px
            svg
                margin-left: 25vw
                padding-top: 5px

    h5
        position: absolute
        line-height: 1.2
        min-height: 90px
        max-height: 110px
        overflow: hidden
        pointer-events: none
        text-overflow: ellipsis
        display: flex
        width: 90%
        align-items: center
        vertical-align: middle
        font-size: 22pt

    img
        position: absolute
        width: 80vw
        max-height: 185px
        filter: saturate(1.5) brightness(0.7) contrast(1.15)
        height: auto
        top: -50px
        left: -50px
        object-fit: cover
        mask-image: -webkit-gradient(linear, left top, right bottom,
        color-stop(0.00,  rgba(0,0,0,1)),
        color-stop(0.35,  rgba(0,0,0,1)),
        color-stop(0.40,  rgba(0,0,0,1)),
        color-stop(0.65,  rgba(0,0,0,0)),
        color-stop(1.00,  rgba(0,0,0,0)))

.items
    margin-top: 140px
    .list-item:last-of-type
        margin-bottom: 0px
        border-bottom: 0
.list
    position: relative
    .archive
        top: 120px
        right: 25px
        position: absolute
        color: var(--white)
        svg
            width: 20px
</style>
