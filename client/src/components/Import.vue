<template>
    <div class="modal">
        <div class="backdrop"/>
        <div class="input" v-if="!importing" :class="{error: error}">
            <div class="catch" @click="close"/>
            <input class="hmn" v-model="query" type="text" placeholder="enter url" ref="in"/>

            <div @click="importApi">
                <v-icon name="corner-down-right" class="ripple-c" />
            </div>
        </div>

        <div class="loading" v-else>
            <v-icon name="loader"/>
        </div>
    </div>
</template>

<script>

export default {
  name: 'Import',

  components: {
  },


  data: function(){
      return {
          query: '',
          error: false,
          importing: false,
      }
  },

  computed: { },

  mounted: function(){
      this.$nextTick(() => {
        this.$refs.in.focus()
      })
  },

  methods: {
      close: function(){
          this.$parent.toggleImport()
      },

    importApi: function(){ 
        if(!this.query){ return }
        this.importing = true
        fetch('http://127.0.0.1:5000/oneshot', {method: 'POST', mode: 'cors', 
            headers: new Headers({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ id: window.localStorage.getItem('id'), url: this.query }) }).then((response) => response.json()).then((res) => {
            if(res && res.id){
                this.axios.post('http://192.168.0.16:4040/api/user/save', {
                    id: window.localStorage.getItem('id'),
                    index: res.id
                }).then((re) => {
                    window.localStorage.setItem('saves', JSON.stringify(re.data.saves))
                    this.$parent.loadSaves()
                    this.close()
                })
            }else{
                this.importing = false
                this.error = true
            }

        })
    },
  }
}
</script>

<style scoped lang="sass">
.modal
    position: fixed
    width: 100vw
    height: 100vh
    backdrop-filter: blur(5px)
    top: 0
    left: 0
    z-index: 9
    width: calc(100% - 40px)
    padding: 20px
    .catch
        position:  absolute
        z-index: -1
        top: -225px
        left: -40px
        width: 100vw
        height: 100vh

    .loading
        svg
            position: relative
            top: calc(50vh - 30px)
            left: calc(50vw - 60px)
            width: 40px
            padding: 20px
            color: var(--white)
    .input
        position: relative
        width: calc(80vw - 50px)
        padding: 105px 25px
        top: 25vh
        left: 25px 
        z-index: 2
        background-color: var(--black)
        border-radius: 5px
        border: 1px solid #1d1d1b
        display: flex
        align-items: center
        &.error
            &::before
                position: absolute
                content: 'an error occoured, please try again'
                bottom: 40px
                color: var(--pink)
                font-size: 9pt
                font-weight: 900
        &::after
            position: absolute
            content: 'Import a recipe'
            top: 40px
            color: var(--white)
            font-weight: 900
        svg
            width: 20px
            padding: 5px
            margin-left: 20px
            color: var(--white)

    .hmn
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

</style>
