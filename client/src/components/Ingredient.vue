<template>
  <div class="result">
    <div class="details" >
        <span>{{r.name}} </span>
        <p>
            {{r.foodGroup}}, {{r.foodSubGroup}}
        </p>
    </div>

    <div class="action">
        <div @click="false"> <v-icon class="ripple" name="shopping-cart" /> </div>
        <div @click="openDetail"> <v-icon class="ripple" name="external-link" /> </div>
    </div>

    <Detail v-if="open" :ing="r" />
  </div>
</template>

<script>
import Detail from '@/components/IngredientDetail.vue'

export default {
  name: 'listItem',
  components: {
      Detail
  },

  props: {
    r: {
        type: Object,
        required: true
    }
  },

  data: function(){
      return {
          open: false,
      }
  },

  methods: {

    openDetail: function(){
        if(this.open){
            this.open = false
        }else{
            this.open = true
        }
    },

    toggle: function(){
        let carousel = document.querySelector('#app');

        if (carousel.classList.contains('full')) {
          carousel.classList.remove('full');
        } else {
          carousel.classList.add('full');
          this.$parent.drawn = true
        }

       this.open = !this.open
    },

  }

}
</script>

<style scoped lang="sass">
    
.result
    display: flex
    margin: 20px
    display: flex
    align-items: center
    justify-content: space-between
    .action
        width: 20%
        display: flex
        align-items: center
        justify-content: center
        svg
            color: var(--white)
            width: 20px
            padding: 10px

    .details
        width: 80%
        margin: 20px
        color: var(--white)

</style>
