import { GPTMessageGroup } from '../store/types';
import { cn } from '../utils/styles';
import { MessageSection } from './MessageMicroGroup';
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
        'flex flex-row shadow-md border-t border-gray-900/50 p-5',
        group.role === 'user' ? 'bg-transparent' : 'bg-[#FFFFFF10]',
      )}
    >
      <div className="container flex mx-auto gap-4">
        <UserInfo agent={group.agent} manuals={group.manuals} />
        <div className='flex-grow flex flex-col max-w-6xl gap-5'>
          {group.sections.map((microGroup, index) => (
            <MessageSection key={index} messageSection={microGroup} isStreaming={index === group.sections.length - 1 && isStreaming} />
          ))}
        </div>
      </div>
    </div>
  );
}
