<template>
  <div class="ing">
      <span> {{ measure }} </span>
      <p> {{unit}} </p>
      <b> {{ ing }} </b>
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

    scale: {
      type: Number,
      required: true,
    }
  },

  computed: {
      ing: function(){
        return this.info.ingredient.replace(this.ingredient.products.measure, '').replace(this.info.unit || this.ingredient.products.unit, '') 
      },

      unit: function(){
        return this.info.unit || this.ingredient.products.unit
      },
      measure: function(){
          let parse = parseFloat(this.ingredient.products.measure)
          if(isNaN(parse)){
            return this.ingredient.products.measure
          }else{
              return ( parse * this.scale ).toFixed(1)
          }
      }
  },
  methods: {
      contribToTotal: function(){
          let ing = this.ingredient.products.name.replace(this.ingredient.products.measure, '').replace(this.info.unit || this.ingredient.products.unit, '') 
          this.axios.post('http://192.168.0.16:4040/api/nutrition/calculate', { ingredient: ing }).then((res) => {
          let factor = 10
          if(this.unit == 'g'){
              factor = this.measure / 100
           }
          if(res.data[0].fat && res.data[0].fat[0]){ this.$parent.fat = this.$parent.fat + (res.data[0].fat[0].fat/factor) }
          if(res.data[0].protein && res.data[0].protein[0]){ this.$parent.protein = this.$parent.protein + (res.data[0].protein[0].protein/factor) }
          if(res.data[0].carbs && res.data[0].carbs[0]){ this.$parent.carbs = this.$parent.carbs + (res.data[0].carbs[0].carbs/factor) }
          })
        }
  },

  mounted: function(){
      this.contribToTotal()
  },

  data: function() {
      return {
        info: Ingreedy.parse(this.ingredient.description)
      }
  }
    
}
</script>

<style scoped lang="sass">

div
    padding-bottom: 20px

.ing
    width: 80%
    margin-left: 20%
    padding: 10px 0
    border-bottom: 1px solid var(--grey)
    box-sizing: border-box
    position: relative
    min-height: 75px
    span 
        position: absolute
        top: 20px 
        left: -25% 
        font-size: 18pt
    p
        color: var(--pink)
        text-transform: lowercase
    b
        text-transform: capitalize

</style>
