import { useState, useRef, useEffect } from 'react';
import { CommandInput } from './components/CommandInput';
import { Pill } from './components/Pill';
import { usePromptStore } from './store/PromptStore';
import { MessageGroup } from './components/MessageGroup';
import { Spinner } from './components/Spinner';
import { Welcome } from './components/Welcome';

function App() {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [scrolling, setScrolling] = useState<boolean>(false);
  const timerIdRef = useRef<number | null>(null);
  const {
    groupedMessages: calculateGroupedMessages,
    isAnalysisRunning,
    isExecuteRunning,
    messages,
    availableTokens,
    usedTokens,
  } = usePromptStore((state) => state);

  useEffect(() => {
    const { current } = messagesEndRef;
    if (!current) return;

    const handleScroll = () => {
      if (timerIdRef.current) {
        clearTimeout(timerIdRef.current);
      }
      setScrolling(true);
      timerIdRef.current = setTimeout(() => setScrolling(false), 1000); // Reset scrolling after 1 second.
    };

    current.addEventListener('scroll', handleScroll);
    return () => {
      current.removeEventListener('scroll', handleScroll);
      // It's important to also clear the timer when the component unmounts.
      if (timerIdRef.current) {
        clearTimeout(timerIdRef.current);
      }
    };
  }, []);

  const lastContent = messages[messages.length - 1]
    ? messages[messages.length - 1].content
    : undefined;
  useEffect(() => {
    const { current } = messagesEndRef;
    if (!current || scrolling) return;

    if (
      Math.abs(
        current.scrollTop - (current.scrollHeight - current.clientHeight),
      ) < 250
    ) {
      const newValue = Math.max(current.scrollHeight - current.clientHeight, 0);
      current.scrollTop = newValue;
    }
    // scrolling intentionally ommited
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    messages.length,
    lastContent,
    isExecuteRunning,
    isAnalysisRunning,
    prompt,
  ]);

  const groupedMessages = calculateGroupedMessages();

  return (
    <div className="App flex flex-col fixed top-0 left-0 bottom-0 right-0 justify-between bg-gray-800 dark: text-slate-200">
      <div
        className="flex-grow overflow-y-auto flex flex-col"
        ref={messagesEndRef}
      >
        {messages.length === 0 ? (
          <Welcome />
        ) : (
          <>
            <div>
              {groupedMessages.map((group, index) => (
                <MessageGroup
                  group={group}
                  key={index}
                  isStreaming={
                    isExecuteRunning && index === groupedMessages.length - 1
                  }
                />
              ))}
            </div>
            <div className="flex-none h-20">
              {availableTokens > 0 && (
                <div>
                  Memory:
                  <Pill
                    color="green"
                    title={`Analysis:\nMax tokens: ${availableTokens}\nUsed tokens: ${usedTokens}\n\nExecution:\nMax tokens: ?\nUsed tokens: ? `}
                  >
                    {(
                      (100 * (availableTokens - usedTokens)) /
                      availableTokens
                    ).toFixed(1)}
                    %
                  </Pill>
                </div>
              )}

              {isAnalysisRunning && (
                <div className=" container mx-auto flex flex-row gap-1 py-5 items-center">
                  <Spinner />
                  Selecting an agent ...
                </div>
              )}
            </div>
          </>
        )}
      </div>

      <div className="">
        <CommandInput />
      </div>
    </div>
  );
}

export default App;
