<template>
    <div class="welcome" v-if="loaded">
        <div class="blotch-wrapper">
            <navIconZ class="t a"/>
            <navIconO class="t s"/>
        </div>


        <div class="content">
            <img />

            <div class="info">
                <h3> Morning, Chef! </h3>
                <p> Lorem ipsum dolor sit amet, consectetur adipiscing elit.  </p>
            </div>

            <div class="login">
                <div class="social">
                    <a class="ripple goo" href="http://localhost:4040/auth/google"> google </a>
                    <a class="fb ripple" href="http://localhost:4040/auth/facebook"> facebook </a>
                </div>
                <div class="break">or</div>
                <a href="/#/explore"> skip </a>
            </div>
        </div>
    </div>
</template>

<script>

import navIconZ from "@/assets/nav0.svg?inline";
import navIconO from "@/assets/nav1.svg?inline";

export default {
  name: 'Welcome',
  data: function(){
      return {
          loaded: false
      }
  },

  mounted: function(){
      if(this.$route.query.uid){
        window.localStorage.setItem('id', this.$route.query.uid)
        this.routeForward()
      }else if(window.localStorage.getItem('id')){
        this.routeForward()
      } else{
        this.loaded = true
      }
  },

  methods: {
    routeForward: function(){
        this.axios.post('http://192.168.0.16:4040/api/user/getPrefrences', {id: window.localStorage.getItem('id')}).then((res) => {
            if(res.data.prefrences){
                window.location = '/#/explore'
            }else{
                window.location = '/#/prefrences'
            }
    })
  }
  },
  components: {
      navIconZ,
      navIconO,

  }
}
</script>

<style lang="sass" scoped> 
.welcome
    position: absolute
    width: 100vw
    height: 100vh
    top: 0
    left: 0
    z-index: 99
    background-color: var(--black)
    overflow: hidden
    .blotch-wrapper
        position: absolute
        width: 100vw
        height: 100vh
        top: 0
        left: 0
        opacity: 0.5
        z-index: -1
        svg g path
            fill: var(--pink)
        .t
            position: absolute
            &.a
                top: -25vh
                left: -70vw
            &.s 
                bottom: -20vh
                right: -90vw
                transform: rotate(20deg)

.content
    display: flex
    position: relative
    flex-wrap: wrap
    width: 100%
    justify-content: center
    top: 50vh
    transform: translateY(-50%)
    text-align: center
    color: var(--white)
    img, div
        display: block
        width: 100%
        margin: 10px auto
    h3
        font-size: 22pt

    .info p
        margin-top: 50px

.login
    .social
        display: flex
        width: 80%
        .goo
            border-color: rgba(15, 157, 88, 0.5)
            background-color: rgba(15, 157, 88, 0.75)
        .fb
            border-color: rgba(64, 100, 172, 0.5)
            background-color: rgba(64, 100, 172, 0.75)
        a
            width: 45%

    .break
        margin: 25px 0
        font-style: italic
        font-size: 8pt
        color: var(--grey)
    a
        display: block
        color: var(--white)
        text-decoration: none
        border: 1px solid #1d1d1b
        width: 40%
        padding: 10px 0
        border-radius: 5px
        margin: 0 auto

</style>
