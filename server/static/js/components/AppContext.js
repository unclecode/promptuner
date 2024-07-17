const task_sample = `I am designing a chatbot to provide some question, collect answer from audience to help them find a match based on their insights from their favourite movies. These questions catogories are:

- Film Character Identification (FCI)
- Self Identification (SI)
- Film Counter-Character Identification (FCCI)
- Counter-Self Identification  (CSI)
- Values (V)

For each part we provide the starting question, and one sample of conversation, which cha bot should follow exactly that one. 

The goal is to instruct the At bot to follow exactly these questions, collect data and then, the end AI should generate 10 Portrait Values Questionnaire (PVQ). I also provide the example of that 10 questions. 

Now task is to generate a very though details PROMPT for the AI language model to follow, and asl all these questions. `
const variables_sample = 'FCI, SI, FCCI, CSI, V, PVQ';

const AppContext = React.createContext();

const AppProvider = ({ children }) => {
    const [task, setTask] = React.useState(task_sample);
    const [variables, setVariables] = React.useState(variables_sample);
    const [prompt, setPrompt] = React.useState('');
    const [tokenCount, setTokenCount] = React.useState(0);

    const clearAll = () => {
        setTask('');
        setVariables('');
        setPrompt('');
        setTokenCount(0);
        localStorage.clear();
    };

    return (
        <AppContext.Provider value={{
            task, setTask,
            variables, setVariables,
            prompt, setPrompt,
            tokenCount, setTokenCount,
            clearAll
        }}>
            {children}
        </AppContext.Provider>
    );
};