import { SystemCommandController, defaultSystemCommandController, executeSystemCommand } from '../../System/src/executeSystemCommand';
import { extractArrayOfAnswersFromGPTResponse } from '../../System/src/extractArrayOfAnswersFromGPTResponse';

export async function createMidjourneyPrompts({
  prompt,
  controller = defaultSystemCommandController(),
}: {
  prompt: string;
  controller: SystemCommandController;
}): Promise<string[]> {
  let responseText = await executeSystemCommand({
    command: `Create midjourey prompt(s) given this user query: ${prompt}`,
    controller,
  });

  return extractArrayOfAnswersFromGPTResponse(responseText);
}
