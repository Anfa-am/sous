<template>
    <div class="glide__slide" ref="slide" >
      <div class="glide__container" >
        <img class="bg"   v-touch:tap="openDetails" v-touch:swipe.up="openDetails" v-touch:swipe.down="false"  v-touch:swipe.right="false"  v-touch:swipe.left="false" :src="`http://192.168.0.16:2020/h32/${recipe._id}/0.jpg`" @load="getColor()"  ref="bg" />
        <div class="content" > <h5 :class="namesize"> {{recipe.name}} </h5> </div>
      </div>

        <div class="details" v-if="active">
          <portal-target :name="`bar`" class="lift" />
          <portal-target :name="`cover`" class="cover" />
          <VueBetterScroll
             ref="scroll"
             :wheelItemClass="'wheel-item'"
             :listenScroll= "true"
             :click="false"
             :pullDownRefresh="pullDownRefreshObj"
             :probeType="2"
             :startY="0"
             @pulling-down="onPullingDown"
             @scroll="zoomImg"
             >

            <Details :recipe="recipe"/>
          </VueBetterScroll>
      </div>
  </div>
</template>

<script>
import Details from '@/components/RecipeDetails.vue'
import VueBetterScroll from 'vue2-better-scroll'


export default {
  name: 'Slide',

  props: {
      recipe: {
        type: Object,
        required: true,
      }
  },

  components: {
      VueBetterScroll,
      Details
  },

  mounted(){
      this.observer = new MutationObserver(mutations => {
        for (const m of mutations) {
          const newValue = m.target.getAttribute(m.attributeName);
          this.$nextTick(() => {
            this.onClassChange(newValue, m.oldValue);
          });
        }
      });

      this.observer.observe(this.$refs.slide, {
        attributes: true,
        attributeOldValue : true,
        attributeFilter: ['class'],
      });

  },

  data: function(){
      return {
        scrollbarObj: false,

        active: false,

        pullDownRefreshObj: {
          threshold: 40,
          stop: 40
        },

      }
  },

  computed: {
    namesize: function(){
        if(this.recipe.name.length < 10){ return 'huge' }
        if(this.recipe.name.length < 30){ return 'large' }
        if(this.recipe.name.length < 40){ return 'med' }
        return 'small' 
    }
  },

  methods: {
     getColor: function(){ },

    onClassChange(classAttrValue) {
      this.active = classAttrValue.split(' ').includes('glide__slide--active')
      if(!this.active){
        this.$refs.bg.style.transform = ``
      }
    },

    openDetails: function(){
        let carousel = document.querySelector('#app');

        if(!this.$refs.slide.classList.contains('glide__slide--active')){
            return false
        }

        if (carousel.classList.contains('full')) {
          this.$refs.scroll.scrollTo(0,0,300)
          this.$refs.bg.style.transform = ''
          carousel.classList.remove('full');
        } else {
          carousel.classList.add('full');
        }
    },

    zoomImg(e){
        if (document.querySelector('#app').classList.contains('full')) {
            if(e.y > 110){
                this.openDetails()
            } else {
                if(e.y/5 > 1.2){
                    this.$refs.bg.style.transitionDuration = `0.3s`
                    if(e.y/5 < 1.7){
                        this.$refs.bg.style.transform = `scale(${e.y/5}) translateX(-10%) translateY(-10%)`
                    } else{
                        this.$refs.bg.style.transform = `scale(${1.7}) translateX(-10%) translateY(-10%)`
                    }
                }
            }
        }

    },

    onPullingDown() {
        this.$refs.scroll.forceUpdate(true)
        this.openDetails()
    },

  }
}
</script>

<style scoped lang="sass">

.glide__slide
    height: 70vh!important
    backface-visibility: hidden
    transform: perspective(2000px)
    pointer-events: none
    opacity: 0.25

    .glide__container
      position: relative
      will-change: transform
      pointer-events: none
      margin-top: 12%
      border-radius: 5px
      height: 100%
      transform-style: preserve-3d
      .content
        position: absolute
        pointer-events: none
        width: 115%
        text-align: left
        clip-path: circle(0px)
        height: auto
        top: 40vh
        transform: translateY(-60%)
        max-height: 70vh
        overflow: hidden
        text-overflow: ellipsis
        font-size: 50pt
        right: -30px
        padding: 10px
        z-index: 9
        svg
            //width: 20px
      img
        position: absolute
        width: 100%
        height: 90%
        opacity: 0.9
        border-radius: 5px
        object-fit: cover
        filter: saturate(1.5) brightness(0.7) contrast(1.15)

    &.glide__slide--active
        opacity: 1
        pointer-events: all
        .glide__container
            pointer-events: all
        .content
            clip-path: circle(66%)


.scroll-wrapper
    width: 100vw
    margin-left: -10px

.full .scroll-wrapper
    &::after
        position: absolute
        content: ' '
        background-color: var(--black)
        width: 30vw
        height: 100vh
        right: calc(-30vw - 8px)
        top: 0
    &::before
        position: absolute
        content: ' '
        background-color: var(--black)
        width: 30vw
        height: 100vh
        left: calc(-30vw - 9px)
        top: 0

h5
    text-transform: capitalize
    line-height: 1.2
    font-weight: bolder
    text-shadow: -1px 2px 10px rgba(13, 14, 2, 0.3)


.details
    position: absolute
    width: 120%
    height: 100vh
    top: 0
    left: -10%
    opacity: 0
    transform: translateY(-5vh)
    pointer-events: none
    overflow: visible
    z-index: 9

.full
    .details
        opacity: 1
        pointer-events: all
        transform: translateY(0vh)
        transition-delay: 0.2s


.lift, .cover
    top: 0
    position: fixed

.cover
    right: 10px
    height: 30vh

.lift
    z-index: 9
    left: 0
</style>
