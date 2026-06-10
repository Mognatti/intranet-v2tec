import type { ConfigType } from '@plone/registry';

import climaData from 'volto-v2tec-intranet/reducers/climaData';

export default function install(config: ConfigType) {
  config.addonReducers = {
    ...config.addonReducers,
    climaData,
  };
  return config;
}
