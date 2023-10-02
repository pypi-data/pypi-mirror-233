export function sanitizePrompt(input: string) {
  let prompt = input;
  prompt = prompt.replace(/\bsadistic\b/gi, 'brutal');
  prompt = prompt.replace(/\binfected\b/gi, 'zombie');
  prompt = prompt.replace(/\blust\b/gi, ' desire');
  prompt = prompt.replace(/\bblood\b/gi, 'dark red liquid');
  prompt = prompt.replace(/\binfection\b/gi, 'disease, plague');
  prompt = prompt.replace(/\btorture\b/gi, 'pain');
  prompt = prompt.replace(/\bcorpses\b/gi, 'bodies');
  prompt = prompt.replace(/\bnaked\b/gi, 'showing skin');
  prompt = prompt.replace(/\bbare\b/gi, '');
  prompt = prompt.replace(/\s+/g, ' ').trim(); //Remove extra whitespace
  return prompt;
}
