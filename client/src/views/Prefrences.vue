<template>
    <div class="prefs">
        <transition name="fade" appear>
        <div class="action" v-if="!end">
            <div @click="back" v-if="$route.query.ex"> <v-icon class="ripple-c" name="arrow-left" /> </div>
            <div v-else/>

            <div class="actions">
                <a @click="next"> skip </a>
            </div>
        </div>

        </transition>

        <div v-if="loaded">
            <div v-if="!end">
                <div v-for="(q, i) in steps" :key="i">
                    <transition name="fade" appear>
                        <Question  v-if="i == step" ref="question" :question="q" :choices="choices[i]"/>
                    </transition>
                </div>
            </div>
        </div>

        <transition name="fade" appear>
            <div class="foot" v-if="!end">
                <div class="progress">
                    {{step + 1}} / {{steps.length}}
                </div>

                <button @click="next"> Next 
                    <v-icon class="ripple-c" name="arrow-right" /> 
                </button>
            </div>
        </transition>

        <transition name="fade" appear>
            <div class="fin" v-if="end">
                <div class="text">
                    <h4>You're all set!</h4>
                    <p>
                        your reccomendations have been fine tuned to your picks blah bla
                     </p>
                </div>
                <button @click="next">  Done
                    <v-icon class="ripple-c" name="check" /> 
                </button>

            </div>
        </transition>
    </div>
</template>

<script>
import Question from '@/components/Question.vue'
import smoothReflow from 'vue-smooth-reflow'
export default {
  name: 'Prefs',

  mixins: [smoothReflow],

  computed: {
    start: function(){
        return this.step == 0
    },
    end: function(){
        return this.step == this.steps.length 
    }
  },

  data: function(){
      return {
          step: 0,
          steps: [
              {
                  question: 'Which cusines do you enjoy?',
                  options: [
                      {
                          name: 'https://www.countryflags.io/us/flat/64.png',
                          value: 'US',
                      }, {
                          name: 'https://www.countryflags.io/ar/flat/64.png',
                          value: 'AR',
                      },{
                          name:'https://www.countryflags.io/br/flat/64.png',
                          value: 'BR'
                      },{
                          name:'https://www.countryflags.io/ch/flat/64.png',
                          value: 'CH'
                      },{
                          name:'https://www.countryflags.io/cn/flat/64.png',
                          value: 'CN'
                      },{
                          name:'https://www.countryflags.io/de/flat/64.png',
                          value: 'DE'
                      } ,{
                          name: 'https://www.countryflags.io/es/flat/64.png',
                          value: 'ES'
                      } ,{
                          name:'https://www.countryflags.io/fr/flat/64.png',
                          value: 'FR'
                      } ,{
                          name:'https://www.countryflags.io/gr/flat/64.png',
                          value: 'GR'
                      },{
                          name:'https://www.countryflags.io/in/flat/64.png',
                          value: 'IN'
                      },{
                          name:'https://www.countryflags.io/ir/flat/64.png',
                          value: 'IR'
                      },{
                          name:'https://www.countryflags.io/it/flat/64.png',
                          value: 'IT'
                      },{
                          name:'https://www.countryflags.io/jp/flat/64.png',
                          value: 'JP'
                      },{
                          name:'https://www.countryflags.io/kr/flat/64.png',
                          value: 'KR'
                      },{
                          name:'https://www.countryflags.io/mx/flat/64.png',
                          value: 'MX'
                      },{
                          name:'https://www.countryflags.io/ph/flat/64.png',
                          value: 'PH'
                      },{
                          name:'https://www.countryflags.io/th/flat/64.png',
                          value: 'TH'
                      },{
                          name:'https://www.countryflags.io/tr/flat/64.png',
                          value: 'TR'
                      }
                  ]
              },

              {
                  question: 'Do you have any dietary restrictions?',
                  options: [
                      {
                          name: 'Gluten Free',
                          value: 'GF'
                      },{
                          name: 'Halal',
                          value: 'HL'
                      },{
                          name: 'Vegan',
                          value: 'VE'
                      },{
                          name: 'Kosher',
                          value: 'KO'
                      },{
                          name: 'Vegiterian',
                          value: 'VG'
                      },{
                          name: 'Ketio',
                          value: 'KE'
                      },{
                          name: 'Carb Free',
                          value: 'CF'
                      }
                  ]
              }, 

              {
                  question: 'Do you have any allergies or inteolerances?',
                  options: [
                      {
                          name: 'Peanut',
                          value: 'peanut'
                      },{
                          name: 'Shell fish',
                          value: 'shell-fish'
                      },{
                          name: 'Egg',
                          value: 'egg'
                      },{
                          name: 'Fish',
                          value: 'fish'
                      },{
                          name: 'Milk, dairy & lactose',
                          value: 'dairy'
                      },{
                          name: 'Sesame',
                          value: 'sesame'
                      },{
                          name: 'Soy',
                          value: 'soy'
                      },{
                          name: 'Tree Nuts',
                          value: 'nuts'
                      },{
                          name: 'Wheat',
                          value: 'wheat'
                      }
                  ]
              },

          ],

          choices: [ [],[],[] ],

          loaded: false
      }
  },

  methods: {
    back: function(){
        if(this.step == 0 ){
            window.location = '/#/explore'
        }else{
            this.step = this.step - 1
        }
    },

    next: function(){
        if(this.end){
            this.axios.post('http://192.168.0.16:4040/api/user/prefrences', {
                id: window.localStorage.getItem('id'),
                prefrences: this.choices
            }).then(() => {
                window.location = '/#/explore'
            })
        }else{
            this.choices[this.step] = this.$refs.question[0].selected
            this.step = this.step + 1
        }
    },

    

  },

  mounted: function(){
    this.$smoothReflow()
    this.axios.post('http://192.168.0.16:4040/api/user/getPrefrences', {id: window.localStorage.getItem('id')}).then((res) => {
        if(res.data.prefrences){
            this.choices = res.data.prefrences
        }
        this.loaded = true
    })

  },

  components: {
    Question
  }
}
</script>

<style lang="sass" scoped> 
.action
    position: relative
    display: flex
    width: calc(100vw - 40px)
    padding: 10px 20px
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
.foot
    position: absolute
    z-index: 10
    padding: 20px
    box-sizing: border-box
    bottom: 0
    left: 0
    width: 100vw
    display: flex 
    align-items: center
    justify-content: space-between

    .progress
        color: #1d1d1b
        font-weight: 900
        font-size: 40pt

button
    background-color: var(--black)
    border: 1px solid #1d1d1b
    color: var(--white)
    border-radius: 5px
    padding: 5px 15px
    padding-right: 10px
    vertical-align: middle

    svg
        width: 20px
        padding: 5px
        padding-right: 0
        vertical-align: middle
        color: var(--white)
.fin
    display: flex
    flex-direction: column
    justify-content: center
    .text
        margin: 30vh 0
        margin-bottom: 10vh
    p
        color: var(--white)
        font-size: 12pt
        margin: 40px
        text-align: center
    h4
        font-size: 22pt
        text-align: center
    button
        width: 30vw 
        margin: 0 auto
</style>
