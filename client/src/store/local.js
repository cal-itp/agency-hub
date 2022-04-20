import { reactive } from 'vue'
import ls from 'local-storage-json'

const LS_KEY = 'GLOBAL_STORE'

export default ({ app }) => {
  const state = reactive(ls.get(LS_KEY) || {})
  const update = (data) => {
    Object.assign(state, data)
    ls.set(LS_KEY, state)
  }
  const getActiveAgency = () =>{
    const { user } = app.config.globalProperties.$auth
    if (!user) {
      return null
    }
    const { selected_agency_id } = state
    const { agencies } = user
    return agencies.find(a => a.id === selected_agency_id) || agencies[0]
  }
  const setActiveAgency = (agency) => update({ selected_agency_id: agency.id })

  return { update, getActiveAgency, setActiveAgency }
}
