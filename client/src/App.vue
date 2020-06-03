<template>
  <div id="app">
    <transition name="fade">
        <router-view/>
    </transition>
    <transition name="fade" appear>
    <div class="nav-wrapper page-el">
        <div id="nav" :class="{listPage:listPage, prefPage:prefPage}">
          <router-link to="/explore">
              <navIconZ class="texture"/>
              <v-icon class="ico" name="compass"></v-icon>
          </router-link>
          <router-link to="/cookbook">
              <navIconO class="texture book"/>
              <v-icon  class="ico" name="book-open"></v-icon>
          </router-link>
          <router-link to="/shopping">
              <navIconT class="texture cart"/>
              <v-icon  class="ico" name="shopping-cart"></v-icon>
          </router-link>
        </div>
    </div>
    </transition>

  </div>
</template>

<script>
import navIconZ from "@/assets/nav0.svg?inline";
import navIconO from "@/assets/nav1.svg?inline";
import navIconT from "@/assets/nav2.svg?inline";

export default {
    name: 'menu',

    mounted: function(){
    },

    computed: {
        listPage: function(){
            return this.$route.name == 'Shopping'
        },
        prefPage: function(){
            return this.$route.name == 'Prefrences'
        }
    },

    components: {
      navIconZ,
      navIconO,
      navIconT,
    }
}
</script>

<style>
:root {
  --black: #0D0E02;
  --grey: #D2CCD7;
  --pink: #C39A94;
  --white: #ECECEF;
}

.fade-enter-active, .fade-leave-active {
    transition: all 500ms cubic-bezier(0.770, 0.000, 0.175, 1.000); /* easeInOutQuart */
}
.fade-enter, .fade-leave-to {
  opacity: 0;
    transition: all 500ms cubic-bezier(0.770, 0.000, 0.175, 1.000); /* easeInOutQuart */
}

@font-face {
    font-family: 'Graphik';
    src: url('assets/graphik.woff2') format('woff2'),
        url('assets/graphik.woff') format('woff'),
        url('assets/graphik.svg#false') format('svg');
    font-weight: normal;
    font-style: normal;
}

.v-icon{
    wdith: 20px;
}

.ripple {
  background-position: center;
  background: var(--black) radial-gradient(circle, transparent 1%, var(--black) 1%) center/15000%;
  border-radius: 50%;
}

.ripple:active {
  background-color: rgba(195, 154, 148, 0.3);
  background-size: 100%;
  transition: background 0s;
}

.ripple-c {
  background-position: center;
  background: transparent radial-gradient(circle, transparent 1%, transparent 1%) center/15000%;
  border-radius: 50%;
}

.ripple-c:active {
  background-color: rgba(195, 154, 148, 0.3);
  background-size: 100%;
  transition: background 0s;
}

    .fade-enter-active, .fade-leave-active {
      transition: opacity .4s;
    }
    .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
      opacity: 0;
    }
* {
    font-family: 'Graphik';
    transition: all 500ms cubic-bezier(0.770, 0.000, 0.175, 1.000); /* easeInOutQuart */
    transition-timing-function: cubic-bezier(0.770, 0.000, 0.175, 1.000); /* easeInOutQuart */
    -webkit-tap-highlight-color:  rgba(0, 0, 0, 0);
    -webkit-tap-highlight-color: transparent;
}
*::-webkit-scrollbar{
    display: none;
}

h1, h2, h3, h4, h5, h6{
    margin: 0;
    padding: 0;
    color: var(--white);
}
input{
    outline: none;
}
</style>

<style lang="sass">

html, body, #app
    width: 100vw
    height: 100vh
    margin: 0
    padding: 0
    background-color: var(--black)
    overflow: hidden

.nav-wrapper
    position: absolute
    height: 100px
    bottom: 0
    overflow: hidden
    z-index: 1
    width: 100%

#nav
    display: flex
    width: 100vw
    justify-content: center
    bottom: 0
    align-items: center
    padding: 20px 0
    position: absolute
    &.prefPage
        opacity: 0
        pointer-events: none
    &.listPage
        backdrop-filter: blur(5px)
        background-color: rgba(13, 14, 2, 0.75)
        opacity: 1
        pointer-events: all
        &.goneo
            opacity: 0
            pointer-events: none
    a
        position: relative
        width: 33%

        .texture
            position: absolute
            top: -50px
            left: 0
            width: 100%
            height: auto
            z-index: 0
            transform: scale(1.5)
            opacity: 0
            pointer-events: none

            &.cart
                top: -50px
                left: 10px
                transform: rotate(-165deg) scale(1.5)

            &.book
                top: -30px
                transform: rotate(23deg) scale(1.5)
                left: -10px

            g path
                clip-path: circle(40px)
                fill: var(--pink)

        .ico
            position: relative
            width: 20px
            display: block
            z-index: 5
            margin: 0 auto
            color: var(--pink)
            transform: scale(0.8)

        &.router-link-active
            .ico
                color: var(--white)
                transform: scale(1.1)

            .texture
                opacity: 1
                g path
                    clip-path: circle(250px)
</style>
