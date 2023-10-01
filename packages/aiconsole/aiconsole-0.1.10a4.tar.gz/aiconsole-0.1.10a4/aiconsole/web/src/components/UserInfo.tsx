import { Agent, Manual } from '../store/PromptStore';

export function UserInfo({ agent, manuals }: { agent: Agent; manuals: Manual[]; }) {
  return (
    <div className="flex-none items-center flex flex-col">
      {agent && (
        <img
          title={agent.id}
          src={`http://${window.location.hostname}:8000/profile/${agent.id}.jpg`}
          className="w-12 h-12 rounded-xl" />
      )}
      <div
        className="text-xs font-bold w-16 text-center overflow-ellipsis overflow-hidden whitespace-nowrap"
        title={`${agent?.id} - ${agent?.usage}`}
      >
        {agent?.name || agent?.id}
      </div>
      {manuals.length > 0 && <div className="text-xs text-center">+</div>}
      {manuals.map((manual) => (
        <div
          key={manual.id}
          className=" font-bold w-16 text-xs text-center overflow-ellipsis overflow-hidden whitespace-nowrap"
          title={`id: ${manual.id}\nusage: ${manual.usage}\ncontent: ${manual.content.length > 100
              ? manual.content.substring(0, 100) + '...'
              : manual.content}`}
        >
          {manual.id}
        </div>
      ))}
    </div>
  );
}
