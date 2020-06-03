<template>
    <div class="ing" :data-item="ingredient.products.name" v-if="list.indexOf(ingredient.products.name) == -1">
      <b> {{ measure }} {{info.unit || ingredient.products.unit}}</b>
      <span> {{ info.ingredient.replace(ingredient.products.measure, '').replace(info.unit || ingredient.products.unit, '') }} </span>
      <v-icon name="minus" class="grab"/>
  </div>
</template>

<script>
import Ingreedy from 'ingredients-parser'

export default {
  name: 'ingredients',


  props: {
    ingredient: {
      type: Object,
      required: true,
    },
    rid: {
      type: String,
      required: true,
    },

  },

  computed: {
      measure: function(){
          let parse = parseFloat(this.ingredient.products.measure)
          if(isNaN(parse)){
            return this.ingredient.products.measure
          }else{
              return parse.toFixed(1)
          }
      }
  },

  data: function() {
      return {
        list: JSON.parse(window.localStorage.getItem('lists'))[this.rid],
        info: Ingreedy.parse(this.ingredient.description)
      }
  },

  methods: {}
}
</script>

<style lang="sass">
.list-item
    display: block
    color: var(--white)
    border-bottom: 1px solid #1d1d1b
    margin-bottom: 20px
    padding-bottom: 20px
    text-transform: lowercase
    position: relative
    .grab
        color: #1d1d1b
        top: calc(50% - 25px)
        right: 0
        width: 30px
        position: absolute

    span, b
        display: block
        width: 80%
    span
        font-size: 12pt
    b
        font-size: 8pt
        color: var(--pink)
        padding-bottom: 5px

</style>
