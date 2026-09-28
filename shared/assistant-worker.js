import { WebWorkerMLCEngineHandler, MLCEngine } from "https://esm.run/@mlc-ai/web-llm@0.2.85";

const engine = new MLCEngine();
const handler = new WebWorkerMLCEngineHandler(engine);

self.onmessage = (msg) => {
  handler.onmessage(msg);
};
