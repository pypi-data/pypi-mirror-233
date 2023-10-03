import { ChangeEvent, useMemo, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import TextareaAutosize from 'react-textarea-autosize';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { darcula } from 'react-syntax-highlighter/dist/cjs/styles/hljs';

import { GPTMessage } from '../store/types';
import { usePromptStore } from '../store/PromptStore';
import { MessageControls } from './MessageControls';

interface MessageProps {
  message: GPTMessage;
  isStreaming: boolean;
}

export function Message({ message, isStreaming }: MessageProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [content, setContent] = useState(message.content);
  const removeMessage = usePromptStore((state) => state.removeMessage);
  const updateMessage = usePromptStore((state) => state.editMessageContent);

  const handleEditClick = () => {
    if (isStreaming) {
      return;
    }
    setContent(message.content);
    setIsEditing(true);
  };

  const handleRemoveClick = () => removeMessage(message.id);

  const handleCancelEditClick = () => setIsEditing(false);

  const handleOnChange = (e: ChangeEvent<HTMLTextAreaElement>) =>
    setContent(e.target.value);

  const handleSaveClick = () => {
    updateMessage(message.id, content);
    setIsEditing(false);
  };

  

  const messageContent = useMemo(() => {
    const handleBlur = () => {
      // setTimeout with 0ms to delay the handleSaveClick call, this will ensure the
      // onClick event has priority over the onBlur event.
      setTimeout(handleSaveClick, 0);
    };

    if (isEditing) {
      return (
        <div className="bg-[#00000080] rounded-md w-[660px]">
          <TextareaAutosize
            className="resize-none border-0 bg-transparent w-full outline-none h-96 p-4"
            defaultValue={content}
            onChange={handleOnChange}
            onBlur={handleBlur} // added onBlur event here
          />
        </div>
      );
    }

    return (
      <>
        {message.code && (
          <div className="flex flex-row">
            <span className="w-20 flex-none">Code:</span>
            <SyntaxHighlighter
              style={darcula}
              children={message.content}
              language={message.language}
              className="not-prose"
            />
          </div>
        )}

        {message.code_output && (
          <div className="flex flex-row">
            <span className="w-20 flex-none">Output:</span>
            <SyntaxHighlighter
              style={darcula}
              children={message.content}
              language={'text'}
              className="not-prose"
            />
          </div>
        )}

        {!message.code && !message.code_output && (
          <ReactMarkdown
            components={{
              code(props) {
                // eslint-disable-next-line @typescript-eslint/no-unused-vars
                const { children, className, inline, node, ...rest } = props;
                const match = /language-(\w+)/.exec(className || '');
                return !inline && match ? (
                  <SyntaxHighlighter
                    {...rest}
                    style={darcula}
                    children={String(children).replace(/\n$/, '')}
                    language={match[1]}
                    PreTag="div"
                  />
                ) : (
                  <code {...rest} className={className}>
                    {children}
                  </code>
                );
              },
            }}
          >
            {message.content}
          </ReactMarkdown>
        )}
      </>
    );
  }, [
    isEditing,
    content,
    message.content,
    message.code,
    message.code_output,
    message.language,
  ]);

  return (
    <div className="flex justify-between items-center relative">
      <div className="prose prose-stone dark:prose-invert max-w-full pr-16">
        {messageContent}
      </div>
      {!isStreaming && <MessageControls
        isEditing={isEditing}
        onCancelClick={handleCancelEditClick}
        onEditClick={handleEditClick}
        onSaveClick={handleSaveClick}
        onRemoveClick={handleRemoveClick}
      />}
    </div>
  );
}
