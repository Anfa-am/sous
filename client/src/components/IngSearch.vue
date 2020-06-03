<template>
    <div class="ing-search">
        <portal-target :name="`id`"> </portal-target>
        <div class="closeSearch" @click="$parent.openSearch"> 
            <v-icon name="shopping-bag" class="ripple-c" @click="false"/>
        </div>
        <div class="input">
            <input class="hmn" v-model="query" type="text" placeholder="find ingredients..." ref="in"/>
        </div>

        <div class="results">
            <Ingredient class="result" v-for="(r, i) in results" :r="r" :key="i" />
        </div>
    </div>
</template>

<script>

import Ingredient from '@/components/Ingredient.vue'
export default {
  name: 'ExSearch',

  components: {
      Ingredient
  },


  data: function(){
      return {
          query: '',
          results: [],
      }
  },

  computed: { },

  mounted: function(){
      this.$nextTick(() => {
        this.$refs.in.focus()
      })
  },

  watch: {
    query: function(){
        this.axios.post('http://192.168.0.16:4040/api/ingredients/ingsearch', { query: this.query }).then((res) => {
          this.results = res.data
        })
    }
  }
}
</script>

<style scoped lang="sass">
.ing-search
    position: fixed
    width: 100vw
    height: 100vh
    top: 0
    left: 0
    z-index: 9
    width: calc(100% - 40px)
    padding: 20px

    .closeSearch
        position: absolute
        top: 14px
        width: 40px
        height: 40px
        z-index: 9
        svg
            margin-top: 20px
            margin-left: 10px
            color: var(--white)
            width: 20px

    .input
        position: relative
        width: 100%
        padding-top: 5px
        top: 0
        left: 0
        z-index: 2
        &::before
            position: absolute
            content: ''
            width: 100vw
            height: 100px
            top: -20px
            left: -20px
            background-color: rgba(13, 14, 2, 0.75)
            backdrop-filter: blur(5px)
            z-index: -1
        &::after
            position: absolute
            content: ''
            bottom: -5px 
            right: 0
            width: calc(100% - 60px)

    .hmn
        position: absolute
        width: calc(100% - 60px)
        height: 100%
        top: -5px
        left: 60px
        font-size: 12pt
        border: none
        border-bottom: 1px solid var(--white)
        background-color: transparent
        padding: 20px 0
        color: var(--white)
        &::placeholder
            font-size: 12pt
            color: var(--grey)
            opacity: 0.3

    .results
        position: absolute
        width: 100vw
        height: calc(100vh - 80px)
        padding-top: 80px
        top: 00px
        z-index: -1
        left: 0
        overflow-y: scroll
        background-color: var(--black)
        
</style>
