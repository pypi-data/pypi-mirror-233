import { v4 as uuidv4 } from 'uuid';

import { Agent, Manual, GPTMessage } from './types';

export function createMessage({
  agent,
  role,
  content,
  manuals,
  language,
  code,
  code_output,
}: {
  agent: Agent;
  role: string;
  content: string;
  manuals: Manual[];
  language?: string;
  code?: boolean;
  code_output?: boolean;
}): GPTMessage {
  return {
    agent: agent,
    id: uuidv4(),
    role,
    manuals: manuals,
    content,
    language,
    code,
    code_output,
    timestamp: new Date().toISOString(),
  };
}
