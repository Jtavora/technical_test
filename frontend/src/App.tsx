import { AppLayout } from "./components/AppLayout";
import { TestClassifyPage } from "./pages/TestClassifyPage";
import { EmailListPage } from "./pages/EmailListPage";

function App() {
  return (
    <AppLayout
      classifyPage={<TestClassifyPage />}
      listPage={<EmailListPage />}
    />
  );
}

export default App;