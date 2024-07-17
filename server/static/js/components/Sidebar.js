const {useContext, useState, useEffect} = React;

const defaultDecorators = [
  { name: "Thinking", enabled: true, params: {} },
  { name: "ResultWrapper", enabled: true, params: { tag: "result" } },
  { name: "JsonResponse", enabled: false, params: {} }
];

const Sidebar = () => {
  const { clearAll } = useContext(AppContext);
  const [modelName, setModelName] = useState(localStorage.getItem("modelName") || "");
  const [apiToken, setApiToken] = useState(localStorage.getItem("apiToken") || "");
  const [decorators, setDecorators] = useState(() => {
    const storedDecorators = localStorage.getItem("decorators");
    return storedDecorators ? JSON.parse(storedDecorators) : defaultDecorators;
  });

  useEffect(() => {
    localStorage.setItem("modelName", modelName);
    localStorage.setItem("apiToken", apiToken);
    localStorage.setItem("decorators", JSON.stringify(decorators));
  }, [modelName, apiToken, decorators]);

  const handleExport = () => {
    const prompt = localStorage.getItem("generatedPrompt");
    if (!prompt) {
      alert("No prompt generated yet.");
      return;
    }

    const blob = new Blob([prompt], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "generated_prompt.md";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleClear = () => {
    setModelName("");
    setApiToken("");
    setDecorators(defaultDecorators);
    clearAll();
  };

  const toggleDecorator = (index) => {
    setDecorators(prevDecorators => 
      prevDecorators.map((dec, i) => 
        i === index ? { ...dec, enabled: !dec.enabled } : dec
      )
    );
  };

  return (
    <div className="w-1/6 pr-4 flex flex-col">
      <h1 className="text-2xl font-bold mb-4 mt-0 pt-0">promptuner</h1>
      <div className="flex-1 flex flex-col">
        <div className="mb-4">
          <label htmlFor="model-name" className="block mb-2">
            Model Name
          </label>
          <input
            type="text"
            id="model-name"
            className="w-full p-2 bg-gray-800 rounded"
            value={modelName}
            onChange={(e) => setModelName(e.target.value)}
          />
        </div>
        <div className="mb-4">
          <label htmlFor="api-token" className="block mb-2">
            API Token
          </label>
          <input
            type="password"
            id="api-token"
            className="w-full p-2 bg-gray-800 rounded"
            value={apiToken}
            onChange={(e) => setApiToken(e.target.value)}
          />
        </div>
        <div className="mb-4">
          <h2 className="text-xl mb-2">Decorators</h2>
          {decorators.map((decorator, index) => (
            <label key={decorator.name} className="block">
              <input
                type="checkbox"
                checked={decorator.enabled}
                onChange={() => toggleDecorator(index)}
              />{" "}
              {decorator.name}
            </label>
          ))}
        </div>
      </div>
      <button onClick={handleExport} className="w-full p-2 primary rounded mb-2">
        <i className="fas fa-file-export mr-2"></i>Export
      </button>
      <button onClick={handleClear} className="w-full p-2 secondary rounded align-bottom">
        <i className="fas fa-trash-alt mr-2"></i>Clear
      </button>
    </div>
  );
};
