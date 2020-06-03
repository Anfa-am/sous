<template>
    <div class="rec-details" >
    <portal to="bar">
        <div class="action" :class="{closeUp: closeUp}">
            <div @click="closeDetails"> <v-icon class="ripple-c" name="arrow-left" /> </div>

            <div class="actions">
                <div @click="openInfo">
                    <v-icon name="info" class="ripple-c" @click="false"/>
                </div>
                <div @click="addList">
                    <v-icon name="shopping-cart" class="ripple-c" @click="false"/>
                </div>
                <div @click="save">
                    <v-icon name="bookmark" class="ripple-c" :class="{saved: saved}"/>
                </div>
            </div>
        </div>
    </portal>

    <portal to="cover">
        <div class="cover-action">
            <v-icon name="activity" />
        </div>


        <div class="cover-action">
            <v-icon name="coffee" />
        </div>

        <div class="cover-action">
            <v-icon name="zap" />
        </div>

        <div class="cover-action">
            <v-icon name="trending-up" />
        </div>
    </portal>

    <div class="summary-wrapper">

        <transition name="fade">
            <div class="detail-modal" v-if="infoOpen">
                <div class="modal">
                    <div class="img-ct">
                        <img :src="recipe.image"/>
                    </div>
                    <a :href="recipe.src">
                        See the orginal recipe
                    </a>
                </div>
            </div>
        </transition>

        <div class="details" :class="{closeUp: closeUp}">
            <div class="title"> <h5>{{recipe.name}}</h5> </div>

            <div class="time">
                <v-icon name="clock" />
                 <span>{{recipe.time}} mins.</span>

            </div>

            <div class="nutrition-break">
                <div class="item">
                    <div class="value">
                        <p> {{fat.toFixed(0)}}
                            <span> g </span>
                        </p>
                    </div>
                    <b> fat </b>
                </div>

                <div class="item">
                    <div class="value">
                        <p> {{protein.toFixed(0)}}
                            <span> g </span>
                        </p>
                    </div>
                    <b> protien </b>
                </div>

                <div class="item">
                    <div class="value">
                        <p> {{carbs.toFixed(0)}}
                            <span> g </span>
                        </p>
                    </div>
                    <b> carbs </b>
                </div>
            </div>

            <div class="scale">
                <span>
                    Serves
                    <input v-model="scale" type="number" ref="scale" @focus="$refs.scale.select()" @keyup.enter="$refs.scale.blur()"/>
                </span>


                <div class="controls">
                    <button class="ripple" @click="scale--">
                        <v-icon  name="minus"/>
                    </button>

                    <button class="ripple" @click="scale++">
                        <v-icon name="plus"/>
                    </button>
                </div>
            </div>

            <div class="ings">
                <Ingredient v-for="(ing, i) in recipe.ingredients" :key="i" :ingredient="ing" :scale="scale/yeild"/>
            </div>

            <div class="steps" id="hello">
                <Steps v-for="(step, i) in steps" :key="i" :steps="step" :index="i" :scale="scale/yeild"/>
            </div>

        </div>
    </div>
  </div>
</template>

<script>
import Steps from '@/components/RecipeStep.vue'
import Ingredient from '@/components/InlineIngredient.vue'

export default {
  name: 'Details',

  components: {
      Steps,
      Ingredient
  },

  props: {
    recipe: {
      type: Object,
      required: true,
    },

    closeUp: {
      type: Boolean,
      required: false,
      default: function(){
          return false
      }
    }

  },

 data: function(){
     return {
         fat: 0,
         protein: 0,
         carbs: 0,
         infoOpen: false,
         saved: false,
         yeild: parseInt(this.recipe.yeild) || 1,
         scale: parseInt(this.recipe.yeild) || 1,
     }
 },

 mounted: function(){
    (JSON.parse(window.localStorage.getItem('saves')) || []).indexOf(this.recipe._id) > -1
 },

 computed: {
    
    steps: function(){
       let newSteps = []
       this.recipe.steps.forEach((x) => {
           let first = x.text.trim().charAt(0);

            if (first === first.toLowerCase() && first !== first.toUpperCase() || !isNaN(first) && isNaN(x.text)) {
                newSteps[newSteps.length - 1] = newSteps[newSteps.length - 1] + ' ' + x.text
            }else {
                newSteps.push(x.text)
            }

       })
      return newSteps
     }
 },
  methods: {
    openInfo: function(){
        if(this.infoOpen){
            this.infoOpen = false
        }else{
            this.infoOpen = true
        }
    },
    addList: function(){
        this.axios.post('http://192.168.0.16:4040/api/user/addList', {
            id: window.localStorage.getItem('id'),
            index: this.recipe._id,
        }).then((res) => {
            console.log(res)
        })
    },

    save: function(){
        this.axios.post('http://192.168.0.16:4040/api/user/save', {
            id: window.localStorage.getItem('id'),
            index: this.recipe._id
        }).then((res) => {
            this.saved = res.data.saved
            window.localStorage.setItem('saves', JSON.stringify(res.data.saves))
        })
    },
    closeDetails: function(){

        if(this.closeUp){
            this.$parent.toggle()
            return
        }

        let carousel = document.querySelector('#app');

        if (carousel.classList.contains('full')) {
          if(this.$parent.$parent.$refs.bg){ this.$parent.$parent.$refs.bg.style.transform = '' }
          carousel.classList.remove('full');
        } else {
          carousel.classList.add('full');
        }
    },
  }
}
</script>

<style scoped lang="sass">

.action
    position: relative
    display: flex
    width: calc(100vw - 19px)
    padding: 10px
    padding-top: 15px
    margin-left: -10px
    background-color: rgba(13, 14, 2, 0.75)
    backdrop-filter: blur(5px)
    border-bottom-left-radius: 20px
    border-bottom-right-radius: 20px
    justify-content: space-between
    align-items: center
    &.closeUp
        border-radius: 0
    .actions
        display: flex
        align-items: center
        color: var(--pink)
    svg
        width: 20px
        padding: 10px
        color: var(--white)
        opacity: 1
        &.saved
            opacity: 0.2

    .title
        color: var(--white)
        text-transform: capitalize
        line-height: 1.2
        font-weight: bolder
        text-shadow: -1px 2px 10px rgba(13, 14, 2, 0.3)

.cover-action
    position: relative
    top: calc(30vh - 30px)
    float: right
    display: inline
    width: auto
    margin-left: 10px
    padding: 10px
    backdrop-filter: blur(10px)
    background-color: rgba(#ECECEF, 0.2)
    border-radius: 5px
    svg
        width: 20px
        color: var(--white)

.summary-wrapper
    position: relative
    height: auto
    width: 100%
    left: 0%
    overflow-y: scroll
    .detail-modal
        position: fixed
        width: 100vw
        height: 100vh
        backdrop-filter: blur(5px) brightness(0.25)
        z-index: 9
        .modal
            position: relative
            width: 50vw
            height: auto
            margin: 0 auto
            top: 90px
            padding: 30px
            border-radius: 5px
            border: 1px solid #1d1d1b
            padding-bottom: 20px
            background-color: var(--black)
            z-index: 1
            color: var(--white)
            display: flex
            flex-direction: column
            align-items: center
            justify-content: center
            &:after
                position: absolute
                content: ''
                top: -10px
                right: 27.5px
                width: 0
                height: 0
                border-style: solid
                border-width: 0 20px 20px 20px
                border-color: transparent transparent var(--black) transparent
            a
                color: var(--grey)
                font-weight: bolder
                text-align: center
                margin: 20px 0
                svg
                    display: block
                    margin: 20px 0
                    width: 20px

            .img-ct
                width: 100px
                height: 100px
                border: 3px solid #1d1d1b
                background-color: rgba(#1d1d1b, 0.5)
                overflow: hidden
                border-radius: 5px
                padding: 15px
                display: flex
                
                img
                    object-fit cover
                    border-radius: 5px
                    width: 100px
                    height: 100px
                    object-position: center

.details
    color: var(--white)
    margin-top: 35vh
    background-color: var(--black)
    border-radius: 20px
    padding: 30px 15%
    padding-bottom: 0px
    position: relative
    &.closeUp
        margin-top: 65px
        border-radius: 0

    .title h5
        font-size: 18pt
        line-height: 1.5
        width: 110%
        margin-bottom: 25px

    .time
        display: flex
        align-items: center
        margin-bottom: 10px
        svg
            margin-right: 20px
            color: var(--pink)
            width: 20px

    .nutrition-break
        display: flex
        justify-content: space-between
        .item
            padding: 30px 0
            margin-right: 10px
            b
                display: block
                margin-top: 5px
            .value
                p
                    display: inline
                    width: auto
                    position: relative
                    font-size: 18pt
                span
                    top: 0
                    font-size: 9pt
                    right: -20px
                    position: absolute

    .scale
        display: flex
        justify-content: space-between
        align-items: center
        padding: 20px 0px
        padding-bottom: 30px
        span
            font-size: 14pt
            display: flex
            input
                background-color: transparent
                color: var(--white)
                font-size: 14pt
                text-align: center
                border: none
                pointer-events: none
                border-bottom: 1px solid var(--white)
                display: block
                padding-bottom: 5px
                margin-left: 20px
                width: 30px
                outline: none
                &:focus
                    border-bottom: 1px solid var(--pink)


        .controls
            display: flex
            justify-content: space-between
            align-items: center
            button
                padding: 0
                margin: 0
                margin-left: 10px
                border: none
                outline: none

            svg
                width: 20px
                pointer-events: none
                padding: 10px
                color: var(--white)

    .ings
        display: flex
        flex-wrap: wrap

    .steps
        position: relative
        margin-top: 60px
        padding-top: 10px
        width: calc(140% + 5px)
        padding: 10px 10%
        border-radius: 20px
        margin-bottom: 10px
        box-sizing: border-box
        overflow: hidden
        left: calc(-20% - 2px)
        background-color: var(--pink)
        z-index: 1
</style>

