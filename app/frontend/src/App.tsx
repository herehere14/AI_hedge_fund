import { Layout } from './components/Layout';
import { Toaster } from './components/ui/sonner';
import { StrategyBuilder } from './components/StrategyBuilder';

export default function App() {
  return (
    <>
      <Layout>
        <StrategyBuilder />
      </Layout>
      <Toaster />
    </>
  );
}