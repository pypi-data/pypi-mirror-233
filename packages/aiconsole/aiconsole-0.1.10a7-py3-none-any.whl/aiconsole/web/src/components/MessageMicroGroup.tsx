import { useState } from 'react';
import { GPTMessageSection } from '../store/types';
import { Message } from './Message';
import { Spinner } from './Spinner';
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/24/solid';

interface MessageProps {
  messageSection: GPTMessageSection;
  isStreaming: boolean;
}

export function MessageSection({ messageSection, isStreaming }: MessageProps) {
  const [folded, setFolded] = useState(messageSection.foldable);

  const messageComponents = messageSection.messages.map((message, index) => (
    <Message
      key={index}
      message={message}
      isStreaming={index === messageSection.messages.length - 1 && isStreaming}
    />
  ));

  if (messageSection.foldable) {
    return (
      <div className="bg-gray-600 p-5 rounded-md flex flex-col gap-5">
        <div
          className="cursor-pointer"
          onClick={() => setFolded((folded) => !folded)}
        >
          <div className="flex flex-row gap-2">
            {isStreaming ? (
              <div className="flex-grow flex flex-row gap-3 items-center">
                Working ... <Spinner />
              </div>
            ) : (
              <div className="flex-grow">Executed code</div>
            )}
            {folded && <ChevronUpIcon className="h-5 w-5" />}
            {!folded && <ChevronDownIcon className="h-5 w-5" />}
          </div>
        </div>
        {!folded && messageComponents}
      </div>
    );
  } else {
    return messageComponents;
  }
}
