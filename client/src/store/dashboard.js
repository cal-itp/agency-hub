import { RestStorage } from '@unrest/vue-storage'

export default () => {
  const slug = 'schema/dashboard'
  const storage = RestStorage(slug, { collection_slug: slug })
  storage.getAll = () => storage.getPage({query: { per_page: 1e6 }})?.items
  return storage
}