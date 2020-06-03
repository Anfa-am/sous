<template>
    <div class="option" @click="select" :class="{selected: selected}">
      <img v-if="option.name.indexOf('.png') > -1" :src="option.name" />
      <p v-else> {{option.name}} </p>
  </div>
</template>

<script>
export default {
  name: 'option',
  components: {
  },

  props: {
    option: {
        type: Object,
        required: true
    }
  },

  data: function(){
      return {
          selected: ( this.$parent.$parent.selected.indexOf(this.option.value) > -1 )
      }
  },

  mounted: function(){

  },

  methods: {
      select: function(){
        if(this.selected){
            this.selected = false
            this.$parent.selected.splice(this.option.value)
        }else{
            this.selected = true
            this.$parent.selected.push(this.option.value)
        }
      }
  }

}
</script>

<style scoped lang="sass">
img
    width: 30px
    padding: 10px
    margin: 10px
    border: 1px solid #1d1d1b
    border-radius: 5px
p
    color: var(--white)
    padding: 10px 15px
    margin: 10px
    border-radius: 5px
    border: 1px solid #1d1d1b

.option
    &.selected
        img, p
            background-color: #1d1d1b
</style>
