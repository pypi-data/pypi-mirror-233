import ky from 'ky';

import { URLS } from './urls';

// TODO: Better types for method parameters

const execute = (body: object, signal?: AbortSignal) =>
  ky.post(URLS.EXECUTE, { json: { ...body }, signal });

const getCommandHistory = () => ky.get(URLS.COMMAND_HISTORY);

const saveCommandToHistory = (body: object) =>
  ky.post(URLS.COMMAND_HISTORY, { json: { ...body } });

const saveHistory = (body: object) =>
  ky.post(URLS.CHAT_HISTORY, { json: { ...body } });

const analyse = (body: object, signal?: AbortSignal) =>
  ky.post(URLS.ANALYSE, { json: { ...body }, signal });

export const Api = {
  execute,
  analyse,
  getCommandHistory,
  saveCommandToHistory,
  saveHistory,
};
