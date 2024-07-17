const App = () => {
    return (
        <AppProvider>
            <div className="container-fluid mx-auto p-4 flex h-screen">
                <Sidebar />
                <MainContent />
            </div>
        </AppProvider>
    );
};