<template>

<portal to="id"> 
<div class="ing-details">
      <div class="action" >
            <div @click="back"> <v-icon class="ripple-c" name="arrow-left" /> </div>
      </div>

      <div class="content">
          <h2>
              {{ing.name}}
              <i>
                  {{ing.scientificName}}
              </i>
          </h2>

          <span>
            {{ing.foodGroup}}, {{ing.foodSubGroup}}
          </span>
          <p>
              {{ing.description}}
          </p>
          <button @click="false"> 
            Add to list 
             <v-icon class="ripple-c" name="shopping-cart" /> 
          </button>
      </div>
  </div>
 </portal>
</template>


<script>
export default {
  name: 'ingDetails',

  props: {
    ing: {
        type: Object,
        required: true
    }
  },

  data: function(){
      return {
      }
  },

  methods: {
    back: function(){
        this.$parent.openDetail()
    }
  }
}
</script>

<style scoped lang="sass">
.ing-details
    position: fixed
    top: 0px 
    left: 0
    width: 100vw
    height: 100vh
    overflow-y: scroll
    background-color: var(--black)
    z-index: 29 

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

.content
    margin: 20px
    span
        font-size: 9pt
        color: var(--white)
        padding-top: 10px
    p
        color: var(--white)
        padding-top: 20px
        font-size: 12pt
        text-align: justify
        line-height: 1.3
    i
        font-size: 9pt

button
    background-color: var(--black)
    border: 1px solid #1d1d1b
    margin: 40px 0
    float: right
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

</style>
