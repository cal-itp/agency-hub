import { reactive } from 'vue'
import ls from 'local-storage-json'

const LS_KEY = 'GLOBAL_STORE'

export default ({ app }) => {
  const state = reactive(ls.get(LS_KEY) || {})
  const update = (data) => {
    Object.assign(state, data)
    ls.set(LS_KEY, state)
  }

  return {
    get agency() {
      const { user } = app.config.globalProperties.$auth
      if (!user) {
        return null
      }
      const { selected_agency_id } = state
      const { agencies } = user
      return agencies.find(a => a.id === selected_agency_id) || agencies[0]
    },
    set agency(agency) {
      update({
        selected_agency_id: agency.id,
        url_number: 0,
      })
    },
    get dashboard() {
      const dashboards = app.config.globalProperties.$store.dashboard.getAll()
      if (!dashboards) {
        return null
      }
      const { selected_dashboard_id } = state
      return dashboards.find(d => d.id === selected_dashboard_id) || dashboards[0]
    },
    set dashboard(dashboard) {
      update({ selected_dashboard_id: dashboard.id })
    },
    get url_number() {
      return state.selected_url_number || 0
    },
    set url_number(url_number) {
      update({ selected_url_number: url_number })
    },
  }
}
