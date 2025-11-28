import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "./openapi.json", // Path to your backend OpenAPI JSON
  output: "./src/client", // Where the SDK + types will be generated

  plugins: [
    {
      name: "@hey-api/sdk",
      asClass: true, // generate services as classes
      operationId: true, // rely on operationId from FastAPI
      classNameBuilder: "{{name}}Service",
      methodNameBuilder: (operation) => {
        // fallback if operation.name is missing
        let name: string = operation.name ?? "unnamed";
        const service: string = operation.service;

        if (service && name.toLowerCase().startsWith(service.toLowerCase())) {
          name = name.slice(service.length);
        }

        return name.charAt(0).toLowerCase() + name.slice(1);
      },
    },
    {
      name: "@hey-api/schemas",
      type: "json", // generate types in JSON-compatible format
    },
  ],
});
