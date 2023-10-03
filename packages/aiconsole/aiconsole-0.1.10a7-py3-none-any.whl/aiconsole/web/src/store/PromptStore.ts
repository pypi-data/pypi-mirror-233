import { useDebouncedValue } from '@mantine/hooks';
import { create } from 'zustand';
import { v4 as uuidv4 } from 'uuid';

import { Agent, Manual, GPTMessageGroup, PromptStore } from './types';
import { createMessage } from './utils';
import { Api } from '../api';

export const usePromptStore = create<PromptStore>((set, get) => ({
  // declarations
  conversationId: uuidv4(),
  agent: undefined,
  mode: 'QUALITY',
  manuals: [],
  messages: [],
  isAnalysisRunning: false,
  isExecuteRunning: false,
  analysisAbortController: new AbortController(), // Initialize fetchAbortController as undefined
  executeAbortSignal: new AbortController(),
  analysisTimeoutId: undefined,
  usedTokens: 0,
  availableTokens: 0,
  promptHistory: [''],
  promptIndex: 0,

  newConversation: () => {
    set(() => ({
      conversationId: uuidv4(),
    }));
  },

  saveHistory: async () => {
    return await Api.saveHistory({
      conversation_id: get().conversationId,
      messages: get().messages,
    });
  },

  saveCommandToHistory: async (command: string) => {
    return (await Api.saveCommandToHistory({ command })).json();
  },

  getCommandsHistory: async () => {
    return (await Api.getCommandHistory()).json();
  },

  groupedMessages: () => {
    const groups: GPTMessageGroup[] = [];

    //Group messages by agent, role and manuals
    for (const message of get().messages) {
      if (
        groups.length === 0 ||
        groups[groups.length - 1].role !== message.role ||
        groups[groups.length - 1].agent !== message.agent ||
        groups[groups.length - 1].manuals.map((m) => m.id).join('|') !==
          message.manuals.map((m) => m.id).join('|')
      ) {
        groups.push({
          agent: message.agent,
          role: message.role,
          manuals: message.manuals,
          sections: [{foldable: false, messages: [message]}],
        });
      } else {
        groups[groups.length - 1].sections.push({foldable: false, messages: [message]});
      }
    }

    //Make all code and code_output messages foldable
    for (const group of groups) {
      for (const microGroup of group.sections) {
        if (microGroup.messages[0].code || microGroup.messages[0].code_output) {
          microGroup.foldable = true;
        }
      }
    }

    //Join all microGroups that have foldable messages together
    for (const group of groups) {
      let i = 0;
      while (i < group.sections.length - 1) {
        if (group.sections[i].foldable && group.sections[i + 1].foldable) {
          group.sections[i].messages = [
            ...group.sections[i].messages,
            ...group.sections[i + 1].messages,
          ];
          group.sections.splice(i + 1, 1);
        } else {
          i++;
        }
      }
    }

    return groups;
  },

  removeMessage: (id: string) =>
    set((state) => ({
      messages: state.messages.filter((message) => message.id !== id),
    })),

  editMessageContent: (id: string, content: string) =>
    set((state) => ({
      messages: state.messages.map((message) =>
        message.id === id ? { ...message, content } : message,
      ),
    })),

  doExecute: async () => {
    set(() => ({
      executeAbortSignal: new AbortController(),
      isExecuteRunning: true,
    }));

    try {
      const response = await Api.execute(
        {
          conversation_id: get().conversationId,
          messages: get().messages,
          relevant_manuals: get().manuals,
          agent: get().agent?.id,
          mode: get().mode,
        },
        get().executeAbortSignal.signal,
      );

      const reader = response.body?.getReader();
      const decoder = new TextDecoder('utf-8');

      let messageDone = true;
      while (true) {
        // this is temporary
        try {
          const { value, done } = (await reader?.read()) || {
            value: undefined,
            done: true,
          };

          const messages = get().messages;

          const TOKEN_PROCESSORS = [
            ...[
              'python',
              'bash',
              'shell',
              'javascript',
              'html',
              'applescript',
              'r',
            ].map((language) => ({
              token: `<<<< START CODE (${language}) >>>>`,
              processor: () => {
                messages.push(
                  createMessage({
                    agent: get().agent!,
                    role: 'assistant',
                    content: '',
                    manuals: get().manuals,
                    language: language,
                    code: true,
                  }),
                );

                messageDone = false;
              },
            })),
            {
              token: '<<<< END CODE >>>>',
              processor: () => {
                if (messageDone) throw new Error('Invalid chunk');
                messageDone = true;
              },
            },
            {
              token: '<<<< START CODE OUTPUT >>>>',
              processor: () => {
                messages.push(
                  createMessage({
                    agent: get().agent!,
                    role: 'assistant',
                    manuals: get().manuals,
                    content: '',
                    code_output: true,
                  }),
                );
                messageDone = false;
              },
            },
            {
              token: '<<<< END CODE OUTPUT >>>>',
              processor: () => {
                if (messageDone) throw new Error('Invalid chunk');
                messageDone = true;
              },
            },
            {
              token: '<<<< CLEAR >>>>',
              processor: () => {
                if (!messageDone) {
                  messages.push(
                    createMessage({
                      agent: get().agent!,
                      manuals: get().manuals,
                      role: 'assistant',
                      content: '',
                    }),
                  );
                  messageDone = false;
                }
                messages[messages.length - 1].content = '';
              },
            },
          ];

          const textChunk = decoder.decode(value);

          const escapeRegExp = (string: string) =>
            string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
          const tokens = TOKEN_PROCESSORS.map((processor) => processor.token);
          const regexPattern = new RegExp(
            `(${tokens.map(escapeRegExp).join('|')})`,
            'g',
          );
          const splitText = textChunk
            .split(regexPattern)
            .filter((text) => text !== '');

          for (const text of splitText) {
            let consumed = false;
            TOKEN_PROCESSORS.forEach((tokenProcessor) => {
              if (text === tokenProcessor.token) {
                tokenProcessor.processor();
                consumed = true;
              }
            });

            if (!consumed) {
              if (messageDone) {
                messages.push(
                  createMessage({
                    agent: get().agent!,
                    manuals: get().manuals,
                    role: 'assistant',
                    content: '',
                  }),
                );
                messageDone = false;
              }
              messages[messages.length - 1].content += text;
            }
          }

          set(() => ({
            messages: messages.slice(),
          }));

          if (done) {
            break;
          }
        } catch (err) {
          if ((err as Error).name === 'AbortError') {
            console.log('Execution operation aborted');
            return;
          } else {
            throw err;
          }
        }
      }
    } finally {
      get().saveHistory();

      set(() => ({
        isExecuteRunning: false,
      }));
    }
  },

  cancelGenerating: () => {
    get().executeAbortSignal.abort();
  },

  getPrompt: () => {
    return get().promptHistory[get().promptIndex];
  },

  initStore: async () => {
    const history = await get().getCommandsHistory();

    set(() => ({
      promptHistory: [...history, ''],
      promptIndex: history.length,
    }));
  },

  doAnalysis: async () => {
    if (get().analysisTimeoutId) {
      clearTimeout(get().analysisTimeoutId);
    }

    set(() => ({
      analysisTimeoutId: undefined,
    }));

    if (get().analysisAbortController.signal.aborted) {
      // If the existing fetch operation has been aborted, stop proceeding
      return;
    }

    try {
      set(() => ({
        isAnalysisRunning: true,
      }));
      const response = await Api.analyse(
        {
          conversation_id: get().conversationId,
          messages: [
            ...get().messages,
            createMessage({
              agent: { id: 'user', name: 'User', usage: '', system: '' },
              manuals: [],
              role: 'user',
              content: get().getPrompt(),
            }),
          ],
          mode: get().mode,
        },
        get().analysisAbortController.signal,
      );

      const data = await response.json<{
        agent: Agent;
        manuals: Manual[];
        usedTokens: number;
        availableTokens: number;
      }>();

      if (get().analysisAbortController.signal.aborted) {
        // If existing fetch operation has been aborted, stop proceeding
        return;
      }

      set(() => ({
        agent: data.agent,
        manuals: data.manuals,
        usedTokens: data.usedTokens,
        availableTokens: data.availableTokens,
      }));

      get().doExecute();
    } catch (err) {
      if ((err as Error).name === 'AbortError') {
        console.log('Analysis aborted');
        return;
      } else {
        throw err;
      }
    } finally {
      set(() => ({
        isAnalysisRunning: false,
      }));
    }
  },

  historyDown: () => {
    set((state) => ({
      promptIndex: Math.min(
        state.promptHistory.length - 1,
        state.promptIndex + 1,
      ),
    }));
  },

  historyUp: () => {
    set((state) => ({ promptIndex: Math.max(0, state.promptIndex - 1) }));
  },

  editPrompt: (prompt) => {
    set((state) => ({
      promptHistory: [
        ...state.promptHistory.slice(0, state.promptIndex),
        prompt,
        ...state.promptHistory.slice(
          state.promptIndex + 1,
          state.promptHistory.length,
        ),
      ],
    }));
  },

  newPrompt: () =>
    set((state) => ({
      promptHistory: [...state.promptHistory, ''],
      promptIndex: state.promptHistory.length,
    })),

  submitPrompt: async (prompt: string) => {
    if (prompt.trim() !== '') {
      set(() => ({
        messages: [
          ...get().messages,
          createMessage({
            agent: { id: 'user', name: 'User', usage: '', system: '' },
            manuals: [],
            role: 'user',
            content: prompt,
          }),
        ],
      }));

      const history = await get().saveCommandToHistory(prompt);
      set(() => ({
        promptHistory: [...history, ''],
        promptIndex: history.length,
      }));
      get().saveHistory();
    }

    get().doAnalysis();
  },
}));

export function useDebouncedPrompt() {
  const prompt = usePromptStore(
    (state) => state.promptHistory[state.promptIndex],
  ).trim();
  const [debouncedPrompt] = useDebouncedValue(prompt, 150, { leading: true });

  return debouncedPrompt;
}

