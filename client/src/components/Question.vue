<template>
  <div class="question">
      <h3>
        {{question.question}}
      </h3>
      <p> (select all that apply) </p>

      <div class="options">
        <transition-group name="fade" :css="false" tag="div" appear @before-enter="beforeEnter" @enter="enter" @leave="leave">
            <Opt v-for="(o, i) in question.options" :option="o" :key="i" :data-key="i" />
        </transition-group>
      </div>
  </div>
</template>

<script>
import Opt from '@/components/Option.vue'
import smoothReflow from 'vue-smooth-reflow'
import Velocity from 'velocity-animate'

export default {
  name: 'question',

  components: {
    Opt 
  },

  props: {
    question: {
        type: Object,
        required: true
    },
    choices: {
        type: Array,
        required: true
    }

  },

  data: function(){
      return {
        selected: this.choices 
      }
  },

  mixins: [smoothReflow],

  mounted: function(){
    this.$smoothReflow()
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
    
  }
}
</script>

<style scoped lang="sass">
.question
    position: relative
    padding: 5% 20px

h3
    font-size: 22pt
    line-height: 1.4

p
    color: var(--white)
    margin-top: 25px
    font-size: 8pt

.options > div
    display: flex
    flex-wrap: wrap
    margin-top: 5vh
</style>
