export type ImaginePayload = {
  type: 'IMAGINE';
  prompt: string;
};

export type UpscalePayload = {
  type: 'UPSCALE';
  messageURL: string;
  gridIndex: number;
};

export type VariationsPayload = {
  type: 'VARIATIONS';
  messageURL: string;
  variationSourceUpscaledOrIndex: 'UPSCALED' | number;
};

export type RequestPayload = ImaginePayload | UpscalePayload | VariationsPayload;
