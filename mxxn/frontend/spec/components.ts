/**
  * This module registers the riot file loader
  * and exports a global dom object.
  * @module
  */
import * as register from '@riotjs/ssr/register'
import { domGlobals } from '@riotjs/ssr'

register()

/**
  * A global dom object.
  *
  * For dom creation call dom.create() and
  * dom.clear() for delete
  */
export let dom = domGlobals
