import local from './local'

const store = {}

const modules = {
  local,
}

export default {
  install(app) {
    app.config.globalProperties.$store = store
    store._app = app
    Object.entries(modules).forEach(([name, module]) => {
      store[name] = module({ store, app })
    })
  }
}