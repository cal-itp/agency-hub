import { ReactiveRestApi } from '@unrest/vue-storage'

export default () => {
  const storage = ReactiveRestApi()
  return {
    watch: (agency_id) => {
      return storage.get(`agency-notices/${agency_id}/`)
    }
  }
}