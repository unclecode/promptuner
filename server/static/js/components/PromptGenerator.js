const PromptGenerator = () => {
    const { task, setTask, variables, setVariables, prompt, setPrompt, tokenCount, setTokenCount } =
        React.useContext(AppContext);

    const generatePrompt = async () => {
        const modelName = localStorage.getItem("modelName");
        const apiToken = localStorage.getItem("apiToken");
        const storedDecorators = JSON.parse(localStorage.getItem("decorators") || "[]");

        const decorators = storedDecorators
            .filter(dec => dec.enabled)
            .map(dec => ({ name: dec.name, params: dec.params }));

        const response = await fetch("/api/generate_prompt", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                task,
                variables: variables.split(",").map((v) => v.trim().toUpperCase()),
                decorators,
                modelName,
                apiToken,
            }),
        });

        if (response.ok) {
            const data = await response.json();
            setPrompt(data.prompt);
            setTokenCount(data.token_count);
            localStorage.setItem("generatedPrompt", data.prompt);
        } else {
            console.error("Failed to generate prompt");
        }
    };

    return (
        <div className="flex h-full">
            <div className="flex-1 pr-4 flex flex-col">
                <div className="mb-4 flex-1 flex flex-col">
                    <label htmlFor="task" className="block mb-2">
                        Task
                    </label>
                    <textarea
                        id="task"
                        className="w-full p-2 bg-gray-800 rounded flex-1"
                        rows="4"
                        value={task}
                        onChange={(e) => setTask(e.target.value)}
                    ></textarea>
                </div>
                <div className="mb-4">
                    <label htmlFor="variables" className="block mb-2">
                        Variables (comma-separated)
                    </label>
                    <input
                        type="text"
                        id="variables"
                        className="w-full p-2 bg-gray-800 rounded"
                        value={variables}
                        onChange={(e) => setVariables(e.target.value)}
                    />
                </div>
                <button
                    className="mt-2 primary text-white font-bold py-2 px-4 rounded"
                    onClick={generatePrompt}
                >
                    Generate Prompt
                </button>
            </div>
            <div className="flex-1 pl-4 flex flex-col">
                <div className="flex justify-between">
                    <label htmlFor="prompt-result" className="block mb-2">
                        Generated Prompt
                    </label>
                    <div id="token-count" className="text-right text-sm text-gray-400">
                        Token count: {tokenCount}
                    </div>
                </div>

                <pre id="prompt-result" className="w-full p-2 bg-gray-800 rounded flex-1 overflow-auto border-none">
                    <code className="language-markdown h-full text-sm bg-gray-900 text-white p-2">{prompt}</code>
                </pre>
            </div>
        </div>
    );
};