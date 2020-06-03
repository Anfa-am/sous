<template>
  <div class="step" v-if="isNaN(steps)">
      <p> {{steps.replace(/ 0 /g, ' ').replace(/6666666666666666/g, '⅔').replace(/3333333333333333/g, '⅓') }} </p>
  </div>
</template>

<script>

export default {
  name: 'Steps',

  components: { },

  props: {
    steps: {
      type: String,
      required: true,
    },
    index: {
      type: Number,
      required: true,
    }


  }
}
</script>

<style scoped lang="sass">

.step
    margin: 50px 0
    margin-right: 0px
    line-height: 1.3
    font-size: 14pt
    font-weight: bolder


</style>
