import { GPTMessageGroup } from '../store/PromptStore';
import { cn } from '../utils/styles';
import { Message } from './Message';
import { UserInfo } from './UserInfo';

export function MessageGroup({
  group,
  isStreaming,
}: {
  group: GPTMessageGroup;
  isStreaming: boolean;
}) {
  return (
    <div
      className={cn(
        'flex flex-row gap-4 shadow-md border-t border-gray-900/50 p-5',
        group.role === 'user' ? 'bg-transparent' : 'bg-[#FFFFFF10]',
      )}
    >
        <UserInfo agent={group.agent} manuals={group.manuals} />
      <div
        className={'flex-grow flex flex-col gap-4 max-w-6xl'}
      >
        {group.messages.map((message, index) => (
          <Message key={index} message={message} isStreaming={isStreaming} />
        ))}
      </div>
    </div>
  );
}
