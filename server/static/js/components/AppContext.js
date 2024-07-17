const task_sample = `Analyze the given email content and perform the following:
    1. Classify the email into one of the provided class labels.
    2. Score the email's importance on a scale of 1 to 10.
    3. Provide a one-sentence summary of the email.
    4. Extract the sender's email address.
    Return the results in a JSON format.`
const variables_sample = 'EMAIL_CONTENT, CLASS_LABELS';

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