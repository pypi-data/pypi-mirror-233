import { usePromptStore } from '../store/PromptStore';

const keyAspects = [
  {
    title: 'Develop Your Personal Assistant',
    description:
      'Construct your own personal AIs, fitted to your bespoke requirements. Spend time on your tool, and watch it grow better and sharper with time.',
    btnText:
      'Guide me through building my personal assistant using AIConsole.',
  },
  {
    title: 'Adaptive Web Interface',
    description:
      'Navigate through our simplified, user-friendly web interface, that makes your tasks easier to understand and more engaging to complete.',
    btnText:
      'I would like to know more about the AIConsole web interface, what are its specific features?',
  },
  {
    title: 'Dynamic AI',
    description:
      "Make your AI tool adapt over time. Add and manage manuals to create a progressively evolving AIConsole that'd serve you even better.",
    btnText: 'How does the AI adapt and improve in AIConsole?',
  },
  {
    title: 'Domain-Specific Tools',
    description:
      'Engineer domain tools for the AIConsole, personalizing it to cater to niche tasks and specifications.',
    btnText: 'How to personalise my AI tools in AIConsole?',
  },
  {
    title: 'Run It Locally',
    description:
      'Execute AIConsole on your local machine rendering a secure and convenient operation.',
    btnText:
      "Can you tell me more about running AIConsole locally and it's security aspects?",
  },
  {
    title: 'Any Task Execution',
    description:
      'Use AIConsole to automate your work, be it managing your schedule or sending emails.',
    btnText: 'Tell me more about how AIConsole executes tasks? what kind of tasks can be executed? what is the spectrum of knowledge AIConsole has access to?',
  },
];

export const Welcome = () => {
  const { submitPrompt } = usePromptStore((state) => state);

  return (
    <div className="flex flex-col items-center justify-center h-full">
      <section className="container mx-auto px-6 py-8 text-center">
        <h2 className="text-4xl font-bold mb-4">Welcome to AIConsole!</h2>
        <p className="text-xl mb-12">
          Empower your projects with our AI-powered assistant.
        </p>

        <div className="grid grid-cols-3 gap-4 mt-8">
          {keyAspects.map((aspect, index) => (
            <div key={index} className="bg-black/20 p-4 rounded-lg flex flex-col gap-4">
              <h3 className="text-lg font-semibold">{aspect.title}</h3>
              <p className="flex-grow">{aspect.description}</p>
              <a
                className=" text-indigo-500 hover:text-indigo-500 font-bold cursor-pointer"
                onClick={() => submitPrompt(aspect.btnText)}
              >
                Read more...
              </a>
            </div>
          ))}
        </div>

        <footer className="text-center mt-12">
          <p>Explore. Adapt. Evolve.</p>
          <p>Welcome, to the future of AI with AIConsole.</p>
        </footer>
      </section>
    </div>
  );
};
