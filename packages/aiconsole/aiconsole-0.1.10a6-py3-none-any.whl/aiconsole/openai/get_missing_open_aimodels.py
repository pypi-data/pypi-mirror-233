import requests

from aiconsole.settings import settings

OPENAI_API_URL = "https://api.openai.com/v1/models"


def get_missing_openai_models():
    missing_models = [
        "davinci",
        "curie",
        "babbage",
        "ada",
    ]  # These are OpenAI's GPT-3 models

    try:
        response = requests.get(
            OPENAI_API_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.openai_api_key}",
            },
        )

        # Make sure the response is in JSON format
        response_data = response.json()

        if response_data and "data" in response_data:
            available_models = [model["id"] for model in response_data["data"]]
            missing_models = list(
                filter(lambda model: model not in available_models, missing_models)
            )

        else:
            print("No data received from OpenAI models API.")
    except Exception as error:
        print(f"Error occurred while checking models: {error}")

    return missing_models


"""import { GPTModel, MODEL_DATA, ModelsResponseData } from './types';
import fetch from 'node-fetch';

/**
 * Function to check the availability of all models in OpenAI.
 */
export async function getMissingOpenAIModels(openAIApiKey: string): Promise<GPTModel[]> {
  const missingModels: GPTModel[] = Object.keys(MODEL_DATA) as GPTModel[];

  try {
    const response = await fetch('https://api.openai.com/v1/models', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${openAIApiKey}`,
      },
    });

    const responseData = (await response.json()) as ModelsResponseData;
    if (!responseData || !responseData.data) {
      console.error('No data received from OpenAI models API.');
      return missingModels;
    }

    const availableModels = responseData.data.map((model) => model.id);

    return missingModels.filter((model) => !availableModels.includes(model));
  } catch (error) {
    console.error(`Error occurred while checking models: ${error}`);
    return missingModels;
  }
}
"""
