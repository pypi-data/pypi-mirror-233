export type GPTMessage = {
  agent: Agent;
  id: string;
  role: string;
  content: string;
  timestamp: string;
  manuals: Manual[];
  language?: string;
  code?: boolean;
  code_output?: boolean;
};

export type GPTMessageSection = {
  foldable: boolean;
  messages: GPTMessage[];
};

export type GPTMessageGroup = {
  agent: Agent;
  role: string;
  manuals: Manual[];
  sections: GPTMessageSection[];
};

export type Manual = {
  id: string;
  usage: string;
  content: string;
};

export type Agent = {
  id: string;
  name: string;
  usage: string;
  system: string;
};

export type GPTMode = 'QUALITY' | 'FAST';

export type PromptStore = {
  conversationId: string;
  agent?: Agent;
  mode: GPTMode;
  manuals: Manual[];
  messages: GPTMessage[];
  removeMessage: (id: string) => void;
  editMessageContent: (id: string, content: string) => void;

  groupedMessages: () => GPTMessageGroup[];

  usedTokens: number;
  availableTokens: number;

  promptHistory: string[];
  promptIndex: number;

  newConversation: () => void;

  historyUp: () => void;
  historyDown: () => void;
  newPrompt: () => void;
  editPrompt: (prompt: string) => void;
  getPrompt: () => string;
  cancelGenerating: () => void;

  // analysis
  doAnalysis: () => void;
  analysisTimeoutId: number | undefined;
  isAnalysisRunning: boolean;

  doExecute: () => void;
  isExecuteRunning: boolean;
  submitPrompt: (prompt: string) => void;

  // requests aborts
  analysisAbortController: AbortController;
  executeAbortSignal: AbortController;

  saveHistory: () => Promise<Response>;
  getCommandsHistory: () => Promise<string[]>;
  saveCommandToHistory: (command: string) => Promise<string[]>;
  initStore: () => void;
};
